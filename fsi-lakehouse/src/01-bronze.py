# -- ----------------------------------
# -- Bronze Layer: Raw Data Ingestion
# -- FSI Lakehouse - Fraud Detection Pipeline
# -- ----------------------------------
# -- MANDATORY: All tables use Auto Loader (cloudFiles) per Constitution #3
# -- ----------------------------------

from pyspark import pipelines as dp

# -- ----------------------------------
# -- bronze_transactions
# -- Ingest raw transaction data (JSON format)
# -- Auto Loader with schema inference and evolution
# -- ----------------------------------
@dp.table(
    name="bronze_transactions",
    comment="Historical banking transactions for fraud detection training"
)
def bronze_transactions():
    return (
        spark.readStream
            .format("cloudFiles")
            .option("cloudFiles.format", "json")
            .option("cloudFiles.inferColumnTypes", "true")
            .option("cloudFiles.schemaEvolutionMode", "addNewColumns")
            .option("cloudFiles.maxFilesPerTrigger", "1")
            .load("/Volumes/main__build/dbdemos_fsi_fraud_detection/fraud_raw_data/transactions")
    )


# -- ----------------------------------
# -- banking_customers
# -- Ingest customer data (CSV format)
# -- Auto Loader with schema validation expectation
# -- ----------------------------------
@dp.table(
    name="banking_customers",
    comment="Customer data with Auto Loader schema inference and evolution support"
)
@dp.expect("correct_schema", "_rescued_data IS NULL")
def banking_customers():
    return (
        spark.readStream
            .format("cloudFiles")
            .option("cloudFiles.format", "csv")
            .option("cloudFiles.inferColumnTypes", "true")
            .option("cloudFiles.schemaEvolutionMode", "addNewColumns")
            .option("multiLine", "true")
            .load("/Volumes/main__build/dbdemos_fsi_fraud_detection/fraud_raw_data/customers")
    )


# -- ----------------------------------
# -- country_coordinates
# -- Ingest country reference data (CSV format)
# -- Auto Loader for geographic coordinate lookups
# -- ----------------------------------
@dp.table(
    name="country_coordinates",
    comment="Country codes with geographic coordinates for transaction enrichment"
)
def country_coordinates():
    return (
        spark.readStream
            .format("cloudFiles")
            .option("cloudFiles.format", "csv")
            .option("cloudFiles.inferColumnTypes", "true")
            .option("cloudFiles.schemaEvolutionMode", "addNewColumns")
            .load("/Volumes/main__build/dbdemos_fsi_fraud_detection/fraud_raw_data/country_code")
    )


# -- ----------------------------------
# -- fraud_reports
# -- Ingest fraud report labels (CSV format)
# -- Auto Loader for ML training labels
# -- ----------------------------------
@dp.table(
    name="fraud_reports",
    comment="Known fraud cases used as labels for ML model training"
)
def fraud_reports():
    return (
        spark.readStream
            .format("cloudFiles")
            .option("cloudFiles.format", "csv")
            .option("cloudFiles.inferColumnTypes", "true")
            .option("cloudFiles.schemaEvolutionMode", "addNewColumns")
            .load("/Volumes/main__build/dbdemos_fsi_fraud_detection/fraud_raw_data/fraud_report")
    )
