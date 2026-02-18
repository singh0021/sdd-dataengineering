# Constitution: FSI Lakehouse - Fraud Detection Pipeline

## Project Principles

### 1. Data Quality First
All transformations must validate input/output schemas. Data quality expectations are enforced at each layer boundary using DLT expectations (`@dp.expect`).

### 2. Medallion Architecture
Strict adherence to Bronze → Silver → Gold layering:
- **Bronze**: Raw ingestion using **Auto Loader only**, schema inference, no transformations
- **Silver**: Cleansed, validated, business logic applied
- **Gold**: Aggregated, ML-ready, consumption-optimized

### 3. Auto Loader for Bronze Ingestion (MANDATORY)
All Bronze layer tables MUST use Auto Loader (`cloudFiles` format) for ingestion:
- Use `spark.readStream.format("cloudFiles")` for all source files
- Enable `cloudFiles.inferColumnTypes` for automatic schema detection
- Enable `cloudFiles.schemaEvolutionMode` for schema evolution support
- Use `cloudFiles.maxFilesPerTrigger` for backpressure control
- Capture schema mismatches in `_rescued_data` column
- Supported formats: JSON, CSV, Parquet, Avro, ORC, Text, Binary

**Auto Loader Configuration Template:**
```python
spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "<json|csv|parquet>")
    .option("cloudFiles.inferColumnTypes", "true")
    .option("cloudFiles.schemaLocation", "<checkpoint_path>")
    .load("<source_path>")
```

**Benefits:**
- Exactly-once processing with checkpointing
- Automatic file discovery and tracking
- Schema inference and evolution
- Scalable to millions of files

### 4. Idempotent Pipelines
Running the same pipeline twice produces the same result. Use Delta Lake ACID transactions and checkpoint-based streaming for exactly-once semantics.

### 5. Schema Evolution Support
Use Auto Loader with `inferColumnTypes` and `_rescued_data` columns to handle schema changes without pipeline failures. Configure `schemaEvolutionMode` as needed (addNewColumns, rescue, failOnNewColumns).

### 6. Incremental Processing
Prefer streaming tables over batch where possible. Use `readStream` for continuous ingestion with backpressure control (`maxFilesPerTrigger`).

### 7. Test at Boundaries
- Contract tests for source schemas
- Integration tests for source/sink connections
- Unit tests for transformation logic
- E2E tests for full pipeline validation

### 8. Observability
- Structured logging for all operations
- DLT expectations for data quality metrics
- Pipeline lineage tracked via Unity Catalog

### 9. Separation of Concerns
Each pipeline file handles exactly one layer. No cross-layer logic within a single file.

### 10. Declarative Over Imperative
Use Databricks Pipelines decorators (`@dp.table`, `@dp.materialized_view`) for declarative table definitions.

### 11. Fail Fast on Critical Data
Use `@dp.expect` to enforce critical data quality rules. Quarantine bad records rather than silently dropping them.

---

## Technology Standards

| Component | Standard |
|-----------|----------|
| Storage | Delta Lake |
| Ingestion | Auto Loader (cloudFiles) |
| Orchestration | Databricks Pipelines (DLT) |
| Governance | Unity Catalog |
| Language | PySpark |
| Deployment | Databricks Asset Bundles (DAB) |

---

## Code Standards

- All tables must have `comment` describing purpose
- All expectations must have descriptive `name`
- No hardcoded paths - use variables/parameters
- Column exclusions must be explicit (not SELECT *)
- Joins must use explicit aliases
