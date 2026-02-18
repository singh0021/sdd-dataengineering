# Research: Technology Decisions

## 1. Ingestion Strategy

### Options Evaluated

| Option | Pros | Cons |
|--------|------|------|
| Auto Loader | Schema inference, incremental, checkpointing | Databricks-specific |
| Spark Structured Streaming | Portable, flexible | Manual schema management |
| Batch with COPY INTO | Simple, one-time loads | No incremental, no schema evolution |

### Decision: Auto Loader
- Native Databricks integration
- Automatic schema inference and evolution
- Built-in checkpointing for exactly-once
- `_rescued_data` column for bad records
- Rate limiting with `maxFilesPerTrigger`

---

## 2. Pipeline Framework

### Options Evaluated

| Option | Pros | Cons |
|--------|------|------|
| Databricks Pipelines (DLT) | Declarative, expectations, lineage | Databricks-specific |
| Apache Airflow + Spark | Portable, mature | More infrastructure |
| dbt + Spark | SQL-first, testing | Limited streaming support |

### Decision: Databricks Pipelines
- Declarative table definitions with decorators
- Built-in data quality expectations
- Automatic dependency management
- Unity Catalog integration for lineage
- Managed infrastructure (no cluster management)

---

## 3. Join Strategies

### Bronze → Silver (fraud_reports)
**LEFT JOIN** because:
- Not all transactions have fraud labels
- Labels arrive separately from transactions
- Need to preserve all transactions for analysis
- NULL `is_fraud` handled in gold layer

### Silver → Gold (country_coordinates, customers)
**INNER JOIN** because:
- Invalid country codes should be excluded from ML
- Transactions without customer data are incomplete
- ML models require complete feature vectors
- Data quality is prioritized over completeness

---

## 4. Data Quality Approach

### Framework: DLT Expectations
Using `@dp.expect` decorator for declarative quality rules:

```python
@dp.expect("rule_name", "SQL expression")
```

### Expectation Types
| Type | Behavior | Use Case |
|------|----------|----------|
| expect | Warn, continue | Non-critical rules |
| expect_or_drop | Drop bad rows | Schema validation |
| expect_or_fail | Fail pipeline | Critical data quality |

### Applied Rules
- `correct_schema`: Drop rows with rescued data (schema mismatch)
- `correct_data`: Fail on NULL transaction IDs
- `correct_customer_id`: Fail on NULL customer IDs
- `amount_decent`: Warn on low-value transactions

---

## 5. Storage Format

### Decision: Delta Lake
- ACID transactions for reliability
- Time travel for debugging/recovery
- Schema enforcement and evolution
- Optimized for both batch and streaming
- Z-ordering for query performance
- Unity Catalog native format

---

## 6. Streaming vs Batch

| Layer | Mode | Rationale |
|-------|------|-----------|
| Bronze | Streaming | Continuous ingestion, low latency |
| Silver | Streaming | Near real-time cleansing |
| Gold | Materialized View | Read-optimized, periodic refresh |

### Backpressure Control
- `maxFilesPerTrigger: 1` for bronze transactions
- Prevents memory issues with large batches
- Ensures consistent checkpoint intervals
