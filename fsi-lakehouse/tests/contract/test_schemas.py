"""
Contract Tests: Schema Validation
FSI Lakehouse - Fraud Detection Pipeline

Validates source data schemas match expected contracts.
"""

import pytest
import json
from pathlib import Path


# Load schema contracts
CONTRACTS_PATH = Path(__file__).parent.parent.parent / ".specify/specs/001-fraud-detection-pipeline/contracts/schemas"


def load_contract(name: str) -> dict:
    """Load JSON schema contract by name."""
    with open(CONTRACTS_PATH / f"{name}.json") as f:
        return json.load(f)


class TestTransactionsSchema:
    """Contract tests for transactions JSON schema."""

    @pytest.fixture
    def schema(self):
        return load_contract("transactions")

    def test_has_required_id_field(self, schema):
        assert "id" in schema["required"]

    def test_id_is_string_type(self, schema):
        assert schema["properties"]["id"]["type"] == "string"

    def test_amount_is_number_type(self, schema):
        assert schema["properties"]["amount"]["type"] == "number"

    def test_has_country_fields(self, schema):
        assert "countryOrig" in schema["properties"]
        assert "countryDest" in schema["properties"]


class TestCustomersSchema:
    """Contract tests for customers CSV schema."""

    @pytest.fixture
    def schema(self):
        return load_contract("customers")

    def test_has_required_id_field(self, schema):
        assert "id" in schema["required"]

    def test_allows_additional_properties(self, schema):
        assert schema.get("additionalProperties", False) is True


class TestCountryCoordinatesSchema:
    """Contract tests for country_coordinates CSV schema."""

    @pytest.fixture
    def schema(self):
        return load_contract("country_coordinates")

    def test_has_required_alpha3_code(self, schema):
        assert "alpha3_code" in schema["required"]

    def test_alpha3_code_pattern(self, schema):
        assert schema["properties"]["alpha3_code"]["pattern"] == "^[A-Z]{3}$"

    def test_lat_avg_has_valid_range(self, schema):
        lat = schema["properties"]["lat_avg"]
        assert lat["minimum"] == -90
        assert lat["maximum"] == 90


class TestFraudReportsSchema:
    """Contract tests for fraud_reports CSV schema."""

    @pytest.fixture
    def schema(self):
        return load_contract("fraud_reports")

    def test_has_required_fields(self, schema):
        assert "id" in schema["required"]
        assert "is_fraud" in schema["required"]

    def test_is_fraud_enum_values(self, schema):
        assert schema["properties"]["is_fraud"]["enum"] == [0, 1]
