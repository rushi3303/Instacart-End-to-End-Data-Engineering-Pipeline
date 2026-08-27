# =====================================================
# Product Demand Prediction - Basic
# =====================================================

import pandas as pd


# =====================================================
# File Path
# =====================================================

TRAIN_PATH = (
    "data/source/csv/order_products__train.csv"
)


# =====================================================
# Product Demand Analysis
# =====================================================

def predict_product_demand(product_id):
    """
    Classifies product demand using historical
    product order frequency.

    Demand is based only on actual order data.
    """

    df = pd.read_csv(
        TRAIN_PATH,
        usecols=[
            "product_id"
        ]
    )

    # Count orders for each product
    product_counts = (
        df["product_id"]
        .value_counts()
    )

    # Check product
    if product_id not in product_counts.index:

        return {
            "product_id": product_id,
            "demand_level": "Unknown",
            "historical_orders": 0,
            "message": (
                "Product was not found in "
                "the available training data."
            )
        }

    order_count = int(
        product_counts[product_id]
    )

    # =================================================
    # Basic Demand Classification
    # =================================================

    if order_count >= 500:

        demand_level = "High"

    elif order_count >= 100:

        demand_level = "Medium"

    else:

        demand_level = "Low"

    return {
        "product_id": product_id,
        "historical_orders": order_count,
        "demand_level": demand_level
    }