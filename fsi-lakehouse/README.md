# FSI Lakehouse - Fraud Detection Pipeline

A Databricks Lakehouse data pipeline for fraud detection, built using **Spec-Driven Development (SDD)** methodology.

## Overview

| Attribute | Value |
|-----------|-------|
| **Project** | fsi-lakehouse |
| **Domain** | Financial Services Industry |
| **Use Case** | Fraud Detection |
| **Architecture** | Medallion (Bronze → Silver → Gold) |
| **Platform** | Databricks with Delta Lake |

## Quick Start

```bash
# Deploy to dev
./scripts/deploy.sh dev

# Run pipeline
./scripts/run_pipeline.sh dev

# Run tests
pytest tests/
```

---

## Project Structure

```
fsi-lakehouse/
├── databricks.yml                 # DAB configuration
├── README.md                      # This file
├── CLAUDE.md                      # AI context file
│
├── src/                           # Pipeline source code
│   ├── 01-bronze.py              # Raw ingestion (Auto Loader)
│   ├── 02-silver.py              # Data cleansing
│   └── 03-gold.py                # ML feature engineering
│
├── resources/                     # Deployment resources
│   └── pipeline.yml              # DLT pipeline definition
│
├── scripts/                       # Automation scripts
│   ├── deploy.sh                 # Deploy to environment
│   ├── run_pipeline.sh           # Trigger pipeline
│   └── destroy.sh                # Tear down deployment
│
├── tests/                         # Test suites
│   ├── contract/                 # Schema contract tests
│   ├── unit/                     # Transformation tests
│   ├── integration/              # Connection tests
│   └── e2e/                      # End-to-end tests
│
└── .specify/                      # SDD artifacts
    ├── memory/
    │   └── constitution.md       # Project principles
    └── specs/001-fraud-detection-pipeline/
        ├── spec.md               # Feature specification
        ├── plan.md               # Technical plan
        ├── research.md           # Technology decisions
        ├── data-model.md         # Schema definitions
        ├── quickstart.md         # Validation scenarios
        ├── tasks.md              # Implementation tasks
        ├── checklists/           # Quality checklists
        └── contracts/schemas/    # Data contracts (JSON Schema)
```

---

## Spec-Driven Development (SDD)

This project follows the SDD methodology using [spec-kit](https://github.com/github/spec-kit).

### What is SDD?

SDD is a development approach where **specifications drive implementation**:

1. **Write specs first** - Define what to build before writing code
2. **Constitution enforces standards** - Project principles apply to all code
3. **Contracts prevent breaking changes** - Schemas defined upfront
4. **Tasks enable tracking** - Clear implementation roadmap
5. **AI-assisted implementation** - Claude Code executes from specs

### SDD Workflow

```
┌─────────────────┐
│   CONSTITUTION  │  Project principles & standards
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   SPECIFICATION │  User stories & acceptance criteria
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│      PLAN       │  Architecture & technology decisions
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│     TASKS       │  Phased implementation breakdown
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   IMPLEMENT     │  Code generation from specs
└─────────────────┘
```

### SDD Commands

Run these in Claude Code (`claude` CLI):

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/speckit.constitution` | Define project principles | Project setup |
| `/speckit.specify` | Create feature specification | New feature |
| `/speckit.clarify` | Resolve ambiguities | Before planning |
| `/speckit.plan` | Create technical plan | After spec approval |
| `/speckit.tasks` | Generate task breakdown | After plan approval |
| `/speckit.implement` | Execute implementation | Ready to build |
| `/speckit.analyze` | Check artifact consistency | Before implementation |

### Example Workflow

```bash
# Start Claude Code
cd fsi-lakehouse
claude

# In Claude Code session:
/speckit.constitution Create principles for fraud detection pipeline
with Auto Loader, medallion architecture, and data quality requirements

/speckit.specify Build a pipeline that ingests banking transactions,
cleanses data, and produces ML-ready features for fraud detection

/speckit.plan Databricks, Delta Lake, Auto Loader, DLT, DAB

/speckit.tasks

/speckit.implement
```

---

## SDD Artifacts

### 1. Constitution (`constitution.md`)

Defines **non-negotiable rules** for all code:

- Data quality requirements
- Technology standards (Auto Loader, Delta Lake)
- Code conventions
- Testing requirements

**Key Principle:** Auto Loader is MANDATORY for Bronze layer.

### 2. Specification (`spec.md`)

Defines **WHAT** to build:

- **US-1:** Bronze Layer - Raw data ingestion
- **US-2:** Silver Layer - Data cleansing & enrichment
- **US-3:** Gold Layer - ML feature engineering

### 3. Plan (`plan.md`)

Defines **HOW** to build:

- Technology stack decisions
- Architecture decisions (AD-1 through AD-5)
- Pipeline component specifications
- Data quality strategy

### 4. Tasks (`tasks.md`)

Defines implementation **ORDER**:

| Phase | Focus | Status |
|-------|-------|--------|
| Phase 1 | Setup | ✅ Complete |
| Phase 2 | Foundational | ⏳ Partial |
| Phase 3 | Bronze Layer | ✅ Complete |
| Phase 4 | Silver Layer | ⏳ Partial |
| Phase 5 | Gold Layer | ⏳ Partial |
| Phase 6 | Deployment | ✅ Complete |
| Phase 7 | Testing | ⏳ Partial |
| Phase 8 | Production | ⏳ Pending |

**Progress: 63% Complete (31/49 tasks)**

---

## Pipeline Architecture

### Data Flow

```
Sources (JSON/CSV)
       │
       ▼ [Auto Loader - cloudFiles]
┌─────────────────────────────────────────┐
│            BRONZE LAYER                 │
│  bronze_transactions  │ banking_customers│
│  country_coordinates  │ fraud_reports    │
└─────────────────────────────────────────┘
       │
       ▼ [Streaming + Batch Join]
┌─────────────────────────────────────────┐
│            SILVER LAYER                 │
│         silver_transactions             │
│   (cleansed, enriched with labels)      │
└─────────────────────────────────────────┘
       │
       ▼ [Materialized View]
┌─────────────────────────────────────────┐
│             GOLD LAYER                  │
│          gold_transactions              │
│    (ML-ready, geo-enriched features)    │
└─────────────────────────────────────────┘
```

### Tables

| Layer | Table | Type | Purpose |
|-------|-------|------|---------|
| Bronze | bronze_transactions | Streaming | Raw transactions (JSON) |
| Bronze | banking_customers | Streaming | Customer data (CSV) |
| Bronze | country_coordinates | Streaming | Geo reference (CSV) |
| Bronze | fraud_reports | Streaming | Fraud labels (CSV) |
| Silver | silver_transactions | Streaming | Cleansed + enriched |
| Gold | gold_transactions | Materialized View | ML-ready features |

### Data Quality Expectations

| Layer | Table | Rule | Expression |
|-------|-------|------|------------|
| Bronze | banking_customers | correct_schema | `_rescued_data IS NULL` |
| Silver | silver_transactions | correct_data | `id IS NOT NULL` |
| Silver | silver_transactions | correct_customer_id | `customer_id IS NOT NULL` |
| Gold | gold_transactions | amount_decent | `amount > 10` |

---

## Deployment

### Environments

| Environment | Catalog | Mode | Target |
|-------------|---------|------|--------|
| dev | dev_fsi | development | Development testing |
| staging | stg_fsi | development | Pre-production |
| prod | prd_fsi | production | Live workloads |

### Deploy Commands

```bash
# Validate configuration
databricks bundle validate -t dev

# Deploy to environment
databricks bundle deploy -t dev

# Run pipeline
databricks bundle run fsi_fraud_detection_pipeline -t dev

# Full refresh
databricks bundle run fsi_fraud_detection_pipeline -t dev --full-refresh

# Destroy deployment
databricks bundle destroy -t dev
```

### Using Scripts

```bash
# Deploy
./scripts/deploy.sh dev|staging|prod

# Run pipeline
./scripts/run_pipeline.sh dev [--full-refresh]

# Destroy
./scripts/destroy.sh dev
```

---

## Testing

### Test Structure

```
tests/
├── contract/          # Schema validation against JSON contracts
├── unit/              # Transformation logic tests
├── integration/       # Source/sink connection tests
└── e2e/               # Full pipeline validation
```

### Run Tests

```bash
# All tests
pytest tests/

# Specific test suite
pytest tests/contract/
pytest tests/unit/
pytest tests/e2e/

# With coverage
pytest tests/ --cov=src
```

### Test Categories

| Type | Purpose | Location |
|------|---------|----------|
| Contract | Validate source schemas | `tests/contract/` |
| Unit | Test transformations | `tests/unit/` |
| Integration | Test connections | `tests/integration/` |
| E2E | Full pipeline flow | `tests/e2e/` |

---

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABRICKS_HOST` | Workspace URL | Yes |
| `DATABRICKS_TOKEN` | Access token | Yes |
| `PROD_SP_NAME` | Production service principal | Prod only |

### DAB Variables

Defined in `databricks.yml`:

| Variable | Default | Description |
|----------|---------|-------------|
| `catalog` | main__build | Unity Catalog name |
| `schema` | dbdemos_fsi_fraud_detection | Schema name |
| `volume_path` | /Volumes/.../fraud_raw_data | Source data path |

---

## Auto Loader Configuration

Per Constitution Principle #3, all Bronze tables use Auto Loader:

```python
spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "json|csv")
    .option("cloudFiles.inferColumnTypes", "true")
    .option("cloudFiles.schemaEvolutionMode", "addNewColumns")
    .option("cloudFiles.maxFilesPerTrigger", "1")
    .load("<source_path>")
```

### Benefits

- Exactly-once processing with checkpointing
- Automatic schema inference and evolution
- Scalable to millions of files
- Backpressure handling

---

## Contributing

### Making Changes

1. **Update specs first** - Modify `.specify/` artifacts before code
2. **Follow constitution** - All code must comply with principles
3. **Run tests** - Ensure all tests pass
4. **Update tasks** - Mark completed tasks in `tasks.md`

### SDD Change Workflow

```bash
# 1. Update specification
/speckit.specify <new requirements>

# 2. Update plan if architecture changes
/speckit.plan <updated tech decisions>

# 3. Regenerate tasks
/speckit.tasks

# 4. Implement changes
/speckit.implement
```

---

## References

- [Spec-Kit Documentation](https://github.com/github/spec-kit)
- [Databricks Asset Bundles](https://docs.databricks.com/dev-tools/bundles/)
- [Auto Loader Guide](https://docs.databricks.com/ingestion/auto-loader/)
- [Delta Live Tables](https://docs.databricks.com/delta-live-tables/)

---

## License

Internal use only.

---

## Support

For issues or questions:
1. Check `.specify/` documentation
2. Review `CLAUDE.md` for context
3. Contact Data Platform team
