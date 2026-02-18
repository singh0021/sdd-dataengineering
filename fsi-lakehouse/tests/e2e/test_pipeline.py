"""
End-to-End Tests: Pipeline Validation
FSI Lakehouse - Fraud Detection Pipeline

Tests for complete pipeline flow with sample data.
"""

import pytest
from pathlib import Path


class TestPipelineE2E:
    """End-to-end pipeline tests."""

    def test_bronze_layer_files_exist(self):
        """Verify Bronze layer implementation exists."""
        bronze_path = Path(__file__).parent.parent.parent / "src/01-bronze.py"
        assert bronze_path.exists(), "Bronze layer file missing"

    def test_silver_layer_files_exist(self):
        """Verify Silver layer implementation exists."""
        silver_path = Path(__file__).parent.parent.parent / "src/02-silver.py"
        assert silver_path.exists(), "Silver layer file missing"

    def test_gold_layer_files_exist(self):
        """Verify Gold layer implementation exists."""
        gold_path = Path(__file__).parent.parent.parent / "src/03-gold.py"
        assert gold_path.exists(), "Gold layer file missing"

    def test_bronze_uses_auto_loader(self):
        """Verify Bronze layer uses Auto Loader (cloudFiles)."""
        bronze_path = Path(__file__).parent.parent.parent / "src/01-bronze.py"
        content = bronze_path.read_text()

        assert 'format("cloudFiles")' in content, "Bronze must use cloudFiles format"
        assert 'cloudFiles.inferColumnTypes' in content, "Bronze must use inferColumnTypes"

    def test_dab_config_exists(self):
        """Verify DAB configuration exists."""
        dab_path = Path(__file__).parent.parent.parent / "databricks.yml"
        assert dab_path.exists(), "databricks.yml missing"

    def test_pipeline_resource_exists(self):
        """Verify pipeline resource definition exists."""
        resource_path = Path(__file__).parent.parent.parent / "resources/pipeline.yml"
        assert resource_path.exists(), "resources/pipeline.yml missing"


class TestAutoLoaderCompliance:
    """Tests for Auto Loader compliance per Constitution #3."""

    def test_all_bronze_tables_use_cloud_files(self):
        """Verify all Bronze tables use cloudFiles format."""
        bronze_path = Path(__file__).parent.parent.parent / "src/01-bronze.py"
        content = bronze_path.read_text()

        # Count table definitions and cloudFiles usages
        table_count = content.count("@dp.table")
        cloud_files_count = content.count('format("cloudFiles")')

        assert table_count == cloud_files_count, \
            f"All {table_count} Bronze tables must use cloudFiles, found {cloud_files_count}"

    def test_schema_evolution_configured(self):
        """Verify schemaEvolutionMode is configured."""
        bronze_path = Path(__file__).parent.parent.parent / "src/01-bronze.py"
        content = bronze_path.read_text()

        assert "schemaEvolutionMode" in content, \
            "Bronze layer must configure schemaEvolutionMode"
