# -- ----------------------------------
# -- Gold Layer: ML-Ready Feature Engineering
# -- FSI Lakehouse - Fraud Detection Pipeline
# -- ----------------------------------
# -- Enriches transactions with geographic and customer data
# -- Produces ML-ready dataset per Plan AD-3 (Materialized View)
# -- ----------------------------------

from pyspark import pipelines as dp
from pyspark.sql import functions as F


@dp.materialized_view(
    name="gold_transactions",
    comment="ML-ready transactions for Data Scientists - geo-enriched with customer features"
)
@dp.expect("amount_decent", "amount > 10")
def gold_transactions():
    # Read silver transactions
    t = spark.read.table("silver_transactions").alias("t")

    # Read country coordinates twice for origin and destination lookups
    o = spark.read.table("country_coordinates").alias("o")
    d = spark.read.table("country_coordinates").alias("d")

    # Read customer data
    c = spark.read.table("banking_customers").alias("c")

    # INNER JOINs ensure only complete data for ML training
    # Per Plan AD-5: Inner Joins for Gold Enrichment
    joined = (
        t.join(o, F.col("t.countryOrig") == F.col("o.alpha3_code"), "inner")
         .join(d, F.col("t.countryDest") == F.col("d.alpha3_code"), "inner")
         .join(c, F.col("c.id") == F.col("t.customer_id"), "inner")
    )

    # Select transaction columns EXCEPT countryOrig, countryDest, is_fraud
    t_cols = [
        F.col(f"t.`{col}`")
        for col in t.columns
        if col not in ["countryOrig", "countryDest", "is_fraud"]
    ]

    # Select customer columns EXCEPT id, _rescued_data
    c_cols = [
        F.col(f"c.`{col}`")
        for col in c.columns
        if col not in ["id", "_rescued_data"]
    ]

    return joined.select(
        *t_cols,
        *c_cols,
        # Coalesce fraud flag: NULL -> 0 -> boolean
        F.coalesce(F.col("t.is_fraud"), F.lit(0)).cast("boolean").alias("is_fraud"),
        # Origin country enrichment
        F.col("o.alpha3_code").alias("countryOrig"),
        F.col("o.country").alias("countryOrig_name"),
        F.col("o.long_avg").alias("countryLongOrig_long"),
        F.col("o.lat_avg").alias("countryLatOrig_lat"),
        # Destination country enrichment
        F.col("d.alpha3_code").alias("countryDest"),
        F.col("d.country").alias("countryDest_name"),
        F.col("d.long_avg").alias("countryLongDest_long"),
        F.col("d.lat_avg").alias("countryLatDest_lat"),
    )
