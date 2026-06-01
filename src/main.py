from src.extract import extract
from src.transform import transform
from src.load import load

from config.logger import logger


def run_pipeline():

    try:

        logger.info("ETL pipeline started")

        extract()

        transform()

        load()

        logger.info("ETL pipeline completed successfully")

    except Exception as e:

        logger.error(f"Pipeline failed: {e}")

        raise


if __name__ == "__main__":
    run_pipeline()