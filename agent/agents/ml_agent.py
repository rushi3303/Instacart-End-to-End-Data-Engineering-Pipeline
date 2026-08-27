# =====================================================
# ML Agent - Order & Customer Behavior
# =====================================================

import os
import pickle
import re

import pandas as pd

from ml.product_demand import predict_product_demand


# =====================================================
# Model Path
# =====================================================

MODEL_PATH = os.path.join(
    "ml",
    "models",
    "reorder_model.pkl"
)


# =====================================================
# Load Reorder Model
# =====================================================

def load_reorder_model():
    """
    Loads the trained Customer Reorder Prediction model.
    """

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Reorder model not found: {MODEL_PATH}"
        )

    with open(
        MODEL_PATH,
        "rb"
    ) as file:

        model = pickle.load(file)

    return model


# =====================================================
# Customer Reorder Prediction
# =====================================================

def predict_reorder(
    order_number,
    order_dow,
    order_hour_of_day,
    days_since_prior_order,
    add_to_cart_order
):
    """
    Predicts whether a product is likely to be reordered.

    Features must match the training model.
    """

    model = load_reorder_model()

    # Create input dataframe
    input_data = pd.DataFrame(
        [[
            order_number,
            order_dow,
            order_hour_of_day,
            days_since_prior_order,
            add_to_cart_order
        ]],
        columns=[
            "order_number",
            "order_dow",
            "order_hour_of_day",
            "days_since_prior_order",
            "add_to_cart_order"
        ]
    )

    # Handle missing value
    input_data["days_since_prior_order"] = (
        input_data["days_since_prior_order"].fillna(0)
    )

    # Prediction
    prediction = model.predict(
        input_data
    )[0]

    # Prediction probability
    probability = model.predict_proba(
        input_data
    )[0][1]

    # Convert prediction into readable result
    if prediction == 1:

        result = "Likely to Reorder"

    else:

        result = "Unlikely to Reorder"

    return {
        "prediction": int(prediction),
        "result": result,
        "reorder_probability": round(
            float(probability) * 100,
            2
        )
    }


# =====================================================
# Extract Reorder Prediction Inputs
# =====================================================

def extract_reorder_inputs(query):
    """
    Extracts the five model features from
    the user query.
    """

    patterns = {
        "order_number":
            r"order_number\s*=\s*(\d+)",

        "order_dow":
            r"order_dow\s*=\s*(\d+)",

        "order_hour_of_day":
            r"order_hour_of_day\s*=\s*(\d+)",

        "days_since_prior_order":
            r"days_since_prior_order\s*=\s*(\d+(?:\.\d+)?)",

        "add_to_cart_order":
            r"add_to_cart_order\s*=\s*(\d+)"
    }

    values = {}

    for key, pattern in patterns.items():

        match = re.search(
            pattern,
            query.lower()
        )

        if not match:
            return None

        values[key] = float(
            match.group(1)
        )

    # Convert integer features
    values["order_number"] = int(
        values["order_number"]
    )

    values["order_dow"] = int(
        values["order_dow"]
    )

    values["order_hour_of_day"] = int(
        values["order_hour_of_day"]
    )

    values["add_to_cart_order"] = int(
        values["add_to_cart_order"]
    )

    return values


# =====================================================
# Extract Product ID
# =====================================================

def extract_product_id(query):
    """
    Extracts product ID from the user question.
    """

    patterns = [
        r"product[_\s]?id\s*[:=]?\s*(\d+)",
        r"product\s+(\d+)",
        r"\b(\d{4,6})\b"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            query.lower()
        )

        if match:

            return int(
                match.group(1)
            )

    return None


# =====================================================
# MAIN ML AGENT
# =====================================================

def ml_agent(query):
    """
    Handles Machine Learning related questions.

    Supported capabilities:

    1. Customer Reorder Prediction
    2. Product Demand Analysis
    """

    q = query.lower()

    # =================================================
    # CUSTOMER REORDER PREDICTION
    # =================================================

    if (
        "reorder" in q
        or "reordered" in q
        or "will order again" in q
        or "order again" in q
    ):

        # Extract model inputs
        inputs = extract_reorder_inputs(
            query
        )

        # Check required inputs
        if inputs is None:

            return {
                "agent": "ML Agent",
                "type": "customer_reorder_prediction",
                "data": None,
                "message": (
                    "Please provide these five values:\n"
                    "order_number, "
                    "order_dow, "
                    "order_hour_of_day, "
                    "days_since_prior_order, "
                    "add_to_cart_order."
                )
            }

        # Run actual ML model
        result = predict_reorder(
            order_number=inputs[
                "order_number"
            ],

            order_dow=inputs[
                "order_dow"
            ],

            order_hour_of_day=inputs[
                "order_hour_of_day"
            ],

            days_since_prior_order=inputs[
                "days_since_prior_order"
            ],

            add_to_cart_order=inputs[
                "add_to_cart_order"
            ]
        )

        return {
            "agent": "ML Agent",
            "type": "customer_reorder_prediction",
            "data": result,
            "message": (
                "Customer reorder prediction "
                "generated successfully."
            )
        }

    # =================================================
    # PRODUCT DEMAND
    # =================================================

    elif (
        "demand" in q
        or "product demand" in q
        or "high demand" in q
        or "future demand" in q
    ):

        # Extract product ID
        product_id = extract_product_id(
            query
        )

        # Check product ID
        if product_id is None:

            return {
                "agent": "ML Agent",
                "type": "product_demand_prediction",
                "data": None,
                "message": (
                    "Please provide a product ID. "
                    "Example: "
                    "Show demand for product 24852."
                )
            }

        # Run actual product demand analysis
        result = predict_product_demand(
            product_id
        )

        return {
            "agent": "ML Agent",
            "type": "product_demand_prediction",
            "data": result,
            "message": (
                "Product demand analysis "
                "generated successfully."
            )
        }

    # =================================================
    # GENERAL ML QUERY
    # =================================================

    elif (
        "machine learning" in q
        or " ml " in f" {q} "
        or "model" in q
        or "prediction" in q
    ):

        return {
            "agent": "ML Agent",
            "type": "ml_analysis",
            "data": {
                "status": "ready",
                "message": (
                    "The ML Agent currently supports "
                    "customer reorder prediction and "
                    "product demand analysis."
                )
            },
            "message": (
                "Machine Learning analysis "
                "request received."
            )
        }

    # =================================================
    # UNKNOWN ML REQUEST
    # =================================================

    return {
        "agent": "ML Agent",
        "type": "unknown",
        "data": None,
        "message": (
            "Sorry, I could not understand "
            "the Machine Learning request."
        )
    }