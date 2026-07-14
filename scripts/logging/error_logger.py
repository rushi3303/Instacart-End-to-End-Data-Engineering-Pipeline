import logging

logging.basicConfig(
    filename="etl_errors.log",
    level=logging.ERROR,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

try:

    result = 10 / 0

except Exception as e:

    logging.error(e)

    print("Error Logged Successfully")