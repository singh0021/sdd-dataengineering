# Technical Plan: Fraud Detection Pipeline

## Technology Stack

| Component | Technology | Rationale |
|-----------|------------|-----------|
| Compute | Databricks | Unified analytics, managed Spark |
| Storage | Delta Lake | ACID, time travel, schema evolution |
| Ingestion | Auto Loader | Incremental, schema inference |
| Pipeline | Databricks Pipelines | Declarative DLT, expectations |
| Governance | Unity Catalog | RBAC, lineage, audit |
| Deployment | DAB | IaC for Databricks assets |
| Language | PySpark | Native Spark integration |

---

## Architecture Decisions

### AD-1: Medallion Architecture
**Decision:** Use Bronze/Silver/Gold layering
**Rationale:** Industry standard for lakehouse, clear separation of concerns, supports incremental refinement
**Trade-offs:** Additional storage cost vs. data quality and flexibility

### AD-2: Auto Loader for All Bronze Ingestion (MANDATORY)
**Decision:** Use `spark.readStream.format("cloudFiles")` for ALL Bronze tables
**Rationale:**
- Near real-time processing with automatic checkpoint management
- Schema inference and evolution without manual intervention
- Exactly-once processing guarantees
- Scalable to millions of files
- Backpressure handling via `maxFilesPerTrigger`

**Required Configuration:**
```python
spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "<json|csv|parquet>")
    .option("cloudFiles.inferColumnTypes", "true")
    .option("cloudFiles.schemaEvolutionMode", "addNewColumns")
    .option("cloudFiles.maxFilesPerTrigger", "1")
    .load("<source_path>")
```

**Trade-offs:** Databricks-specific vs. portability; acceptable for lakehouse commitment

### AD-3: Materialized View for Gold
**Decision:** Use `@dp.materialized_view` for gold layer
**Rationale:** Optimized for read-heavy ML workloads, automatic refresh
**Trade-offs:** Higher compute cost vs. query performance

### AD-4: Left Join for Fraud Labels
**Decision:** LEFT JOIN transactions with fraud_reports
**Rationale:** Not all transactions have fraud labels; preserve all transactions
**Trade-offs:** NULL handling required in gold layer

### AD-5: Inner Joins for Gold Enrichment
**Decision:** INNER JOIN for country coordinates and customers
**Rationale:** Only valid transactions with complete data for ML training
**Trade-offs:** Data loss for invalid references; acceptable for ML quality

---

## Pipeline Components

### Bronze Layer (01-bronze.py) - Auto Loader MANDATORY

All Bronze tables MUST use Auto Loader (`cloudFiles` format) per constitution principle #3.

| Table | Source | Format | Auto Loader Options |
|-------|--------|--------|---------------------|
| bronze_transactions | transactions/ | JSON | `cloudFiles.format=json`, `inferColumnTypes=true`, `maxFilesPerTrigger=1` |
| banking_customers | customers/ | CSV | `cloudFiles.format=csv`, `inferColumnTypes=true`, `multiLine=true` |
| country_coordinates | country_code/ | CSV | `cloudFiles.format=csv`, `inferColumnTypes=true` |
| fraud_reports | fraud_report/ | CSV | `cloudFiles.format=csv`, `inferColumnTypes=true` |

**Bronze Layer Code Pattern:**
```python
@dp.table(name="<table_name>", comment="<description>")
def <table_name>():
    return (
        spark.readStream
            .format("cloudFiles")
            .option("cloudFiles.format", "<json|csv>")
            .option("cloudFiles.inferColumnTypes", "true")
            .option("cloudFiles.schemaEvolutionMode", "addNewColumns")
            .load("<volume_path>")
    )
```

### Silver Layer (02-silver.py)

| Table | Sources | Transformations |
|-------|---------|-----------------|
| silver_transactions | bronze_transactions (stream), fraud_reports (batch) | Clean country codes, calculate balance diffs, join fraud labels |

### Gold Layer (03-gold.py)

| Table | Sources | Transformations |
|-------|---------|-----------------|
| gold_transactions | silver_transactions, country_coordinates (2x), banking_customers | Geo-enrichment, customer join, fraud flag coalesce |

---

## Data Quality Strategy

| Layer | Table | Expectation | Action |
|-------|-------|-------------|--------|
| Bronze | banking_customers | `_rescued_data IS NULL` | Drop bad schema |
| Silver | silver_transactions | `id IS NOT NULL` | Fail pipeline |
| Silver | silver_transactions | `customer_id IS NOT NULL` | Fail pipeline |
| Gold | gold_transactions | `amount > 10` | Warn (allow) |

---

## Deployment Environments

| Environment | Catalog | Mode | Cluster |
|-------------|---------|------|---------|
| dev | dev_fsi | development | Single node |
| staging | stg_fsi | development | 2-4 workers |
| prod | prd_fsi | production | Auto-scale 2-8 |

---

## File Structure

```
fsi-lakehouse/
├── databricks.yml              # DAB configuration
├── resources/
│   └── pipeline.yml            # DLT pipeline definition
├── src/
│   ├── 01-bronze.py           # Bronze layer
│   ├── 02-silver.py           # Silver layer
│   └── 03-gold.py             # Gold layer
├── tests/
│   ├── contract/              # Schema validation
│   ├── unit/                  # Transform logic
│   ├── integration/           # Connection tests
│   └── e2e/                   # Pipeline tests
└── .specify/                  # SDD artifacts
```
