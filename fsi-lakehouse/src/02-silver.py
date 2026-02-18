# -- ----------------------------------
# -- Silver Layer: Data Cleansing & Enrichment
# -- FSI Lakehouse - Fraud Detection Pipeline
# -- ----------------------------------
# -- Cleanses raw data and joins with fraud labels
# -- Enforces data quality expectations per Constitution #1
# -- ----------------------------------

from pyspark import pipelines as dp
from pyspark.sql import functions as F


@dp.table(
    name="silver_transactions",
    comment="Cleansed and enriched transactions for Data Analysts"
)
@dp.expect("correct_data", "id IS NOT NULL")
@dp.expect("correct_customer_id", "customer_id IS NOT NULL")
def silver_transactions():
    # Read bronze transactions as streaming source
    t = spark.readStream.table("bronze_transactions").alias("t")

    # Read fraud reports as batch (labels for ML)
    f = spark.read.table("fraud_reports").alias("f")

    # LEFT JOIN to preserve all transactions (not all have fraud labels)
    # Per Plan AD-4: Left Join for Fraud Labels
    joined = t.join(f, on="id", how="left")

    # Select transaction columns EXCEPT countryOrig, countryDest, _rescued_data
    t_cols = [
        F.col(f"t.`{c}`")
        for c in t.columns
        if c not in ["countryOrig", "countryDest", "_rescued_data"]
    ]

    # Select fraud report columns EXCEPT id, _rescued_data
    f_cols = [
        F.col(f"f.`{c}`")
        for c in f.columns
        if c not in ["id", "_rescued_data"]
    ]

    return joined.select(
        *t_cols,
        *f_cols,
        # Clean country codes by removing "--" prefix
        F.regexp_replace(F.col("t.countryOrig"), "--", "").alias("countryOrig"),
        F.regexp_replace(F.col("t.countryDest"), "--", "").alias("countryDest"),
        # Calculate balance differences for feature engineering
        (F.col("t.newBalanceOrig") - F.col("t.oldBalanceOrig")).alias("diffOrig"),
        (F.col("t.newBalanceDest") - F.col("t.oldBalanceDest")).alias("diffDest"),
    )
