# CLAUDE.md - FSI Lakehouse Project Context

## Project Overview

**Name:** fsi-lakehouse
**Purpose:** Fraud detection data pipeline using Databricks Lakehouse medallion architecture
**Domain:** Financial Services Industry (FSI)
**Status:** Implemented via SDD (Spec-Driven Development)

## Architecture

```
Bronze (Raw) → Silver (Cleansed) → Gold (ML-Ready)
```

### Tables
| Layer | Table | Type |
|-------|-------|------|
| Bronze | bronze_transactions | Streaming Table |
| Bronze | banking_customers | Streaming Table |
| Bronze | country_coordinates | Streaming Table |
| Bronze | fraud_reports | Streaming Table |
| Silver | silver_transactions | Streaming Table |
| Gold | gold_transactions | Materialized View |

## Technology Stack

- **Platform:** Databricks
- **Storage:** Delta Lake
- **Ingestion:** Auto Loader (cloudFiles)
- **Pipeline:** Databricks Pipelines (DLT)
- **Governance:** Unity Catalog
- **Deployment:** Databricks Asset Bundles (DAB)
- **Language:** PySpark

## Key Files

```
src/
├── 01-bronze.py    # Raw ingestion (4 tables)
├── 02-silver.py    # Cleansing & enrichment
└── 03-gold.py      # Feature engineering
```

## Data Quality Expectations

| Table | Rule | Expression |
|-------|------|------------|
| banking_customers | correct_schema | `_rescued_data IS NULL` |
| silver_transactions | correct_data | `id IS NOT NULL` |
| silver_transactions | correct_customer_id | `customer_id IS NOT NULL` |
| gold_transactions | amount_decent | `amount > 10` |

## Key Transformations

### Silver Layer
- LEFT JOIN transactions with fraud_reports
- Clean country codes: `regexp_replace(country, '--', '')`
- Calculate balance diffs: `newBalance - oldBalance`

### Gold Layer
- INNER JOIN with country_coordinates (origin & destination)
- INNER JOIN with banking_customers
- Coalesce fraud flag: `coalesce(is_fraud, 0)::boolean`

## SDD Artifacts

See `.specify/` directory:
- `memory/constitution.md` - Project principles
- `specs/001-fraud-detection-pipeline/`
  - `spec.md` - Feature specification
  - `plan.md` - Technical plan
  - `research.md` - Technology decisions
  - `data-model.md` - Schema definitions
  - `quickstart.md` - Validation scenarios
  - `tasks.md` - Task breakdown
  - `checklists/` - Quality checklists
  - `contracts/schemas/` - JSON schema contracts

## Commands

```bash
# Deploy to dev
databricks bundle deploy -t dev

# Run pipeline
databricks bundle run fsi_fraud_detection_pipeline -t dev

# Validate configuration
databricks bundle validate -t dev
```

## Source Data Locations

```
/Volumes/main__build/dbdemos_fsi_fraud_detection/fraud_raw_data/
├── transactions/    (JSON)
├── customers/       (CSV)
├── country_code/    (CSV)
└── fraud_report/    (CSV)
```
