"""
Unit Tests: Transformation Logic
FSI Lakehouse - Fraud Detection Pipeline

Tests for Silver and Gold layer transformation functions.
"""

import pytest
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType


@pytest.fixture(scope="module")
def spark():
    """Create a SparkSession for testing."""
    return (
        SparkSession.builder
        .master("local[*]")
        .appName("fsi-lakehouse-tests")
        .getOrCreate()
    )


class TestCountryCodeCleaning:
    """Tests for country code cleaning logic (Silver layer)."""

    def test_removes_double_dash_prefix(self, spark):
        df = spark.createDataFrame([("--USA",)], ["countryOrig"])
        result = df.withColumn(
            "cleaned",
            F.regexp_replace(F.col("countryOrig"), "--", "")
        )
        assert result.collect()[0]["cleaned"] == "USA"

    def test_preserves_valid_country_code(self, spark):
        df = spark.createDataFrame([("GBR",)], ["countryOrig"])
        result = df.withColumn(
            "cleaned",
            F.regexp_replace(F.col("countryOrig"), "--", "")
        )
        assert result.collect()[0]["cleaned"] == "GBR"

    def test_handles_null_country_code(self, spark):
        df = spark.createDataFrame([(None,)], ["countryOrig"])
        result = df.withColumn(
            "cleaned",
            F.regexp_replace(F.col("countryOrig"), "--", "")
        )
        assert result.collect()[0]["cleaned"] is None


class TestBalanceDiffCalculation:
    """Tests for balance difference calculation (Silver layer)."""

    def test_calculates_positive_diff(self, spark):
        df = spark.createDataFrame([(100.0, 150.0)], ["oldBalance", "newBalance"])
        result = df.withColumn(
            "diff",
            F.col("newBalance") - F.col("oldBalance")
        )
        assert result.collect()[0]["diff"] == 50.0

    def test_calculates_negative_diff(self, spark):
        df = spark.createDataFrame([(200.0, 150.0)], ["oldBalance", "newBalance"])
        result = df.withColumn(
            "diff",
            F.col("newBalance") - F.col("oldBalance")
        )
        assert result.collect()[0]["diff"] == -50.0

    def test_handles_null_values(self, spark):
        df = spark.createDataFrame([(None, 150.0)], ["oldBalance", "newBalance"])
        result = df.withColumn(
            "diff",
            F.col("newBalance") - F.col("oldBalance")
        )
        assert result.collect()[0]["diff"] is None


class TestFraudFlagCoalesce:
    """Tests for fraud flag coalesce logic (Gold layer)."""

    def test_coalesces_null_to_false(self, spark):
        df = spark.createDataFrame([(None,)], schema=["is_fraud"])
        result = df.withColumn(
            "is_fraud_clean",
            F.coalesce(F.col("is_fraud"), F.lit(0)).cast("boolean")
        )
        assert result.collect()[0]["is_fraud_clean"] is False

    def test_preserves_fraud_true(self, spark):
        df = spark.createDataFrame([(1,)], ["is_fraud"])
        result = df.withColumn(
            "is_fraud_clean",
            F.coalesce(F.col("is_fraud"), F.lit(0)).cast("boolean")
        )
        assert result.collect()[0]["is_fraud_clean"] is True

    def test_preserves_fraud_false(self, spark):
        df = spark.createDataFrame([(0,)], ["is_fraud"])
        result = df.withColumn(
            "is_fraud_clean",
            F.coalesce(F.col("is_fraud"), F.lit(0)).cast("boolean")
        )
        assert result.collect()[0]["is_fraud_clean"] is False
