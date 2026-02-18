# Feature Specification: Fraud Detection Data Pipeline

## Overview

Build a data lakehouse pipeline that ingests banking transaction data from multiple sources, cleanses and enriches the data through medallion architecture layers, and produces ML-ready datasets for fraud detection model training and inference.

---

## User Stories

### US-1: Raw Data Ingestion (Bronze Layer)
**As a** Data Engineer
**I want** to ingest raw transaction, customer, and reference data incrementally
**So that** I have a reliable bronze layer with full data history and schema evolution support

**Acceptance Criteria:**
- [ ] All Bronze tables use Auto Loader (`cloudFiles` format) - MANDATORY per constitution
- [ ] Transactions ingested from JSON files via Auto Loader streaming
- [ ] Customers ingested from CSV files via Auto Loader streaming
- [ ] Country coordinates loaded via Auto Loader streaming
- [ ] Fraud report labels loaded via Auto Loader streaming
- [ ] `cloudFiles.inferColumnTypes` enabled for automatic schema detection
- [ ] `cloudFiles.schemaEvolutionMode` configured for schema evolution
- [ ] `cloudFiles.maxFilesPerTrigger` set for backpressure control
- [ ] Schema location configured for checkpoint persistence
- [ ] Bad schema records captured in `_rescued_data` column
- [ ] Exactly-once processing guaranteed via Auto Loader checkpointing

---

### US-2: Data Cleansing & Enrichment (Silver Layer)
**As a** Data Analyst
**I want** cleansed transaction data joined with fraud labels
**So that** I can analyze transactions with quality guarantees

**Acceptance Criteria:**
- [ ] Transactions joined with fraud reports (LEFT JOIN on id)
- [ ] Country codes cleaned (remove `--` patterns)
- [ ] Balance differences calculated (diffOrig, diffDest)
- [ ] Null transaction IDs rejected
- [ ] Null customer IDs rejected
- [ ] `_rescued_data` columns excluded from output

---

### US-3: ML Feature Engineering (Gold Layer)
**As a** Data Scientist
**I want** enriched transaction data with geographic and customer features
**So that** I can train fraud detection models

**Acceptance Criteria:**
- [ ] Transactions enriched with origin country coordinates
- [ ] Transactions enriched with destination country coordinates
- [ ] Customer attributes joined to transactions
- [ ] Fraud flag coalesced (NULL → 0 → boolean)
- [ ] Low-value transactions filtered (amount > 10)
- [ ] Materialized view for query performance

---

## Data Flow

```
Sources (JSON/CSV)
       │
       ▼ [Auto Loader - cloudFiles]
┌─────────────────────────────────────────┐
│            BRONZE LAYER                 │
│  (All tables via Auto Loader streaming) │
│  bronze_transactions  │ banking_customers│
│  country_coordinates  │ fraud_reports    │
└─────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────┐
│            SILVER LAYER                 │
│         silver_transactions             │
│   (cleansed, enriched with labels)      │
└─────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────┐
│             GOLD LAYER                  │
│          gold_transactions              │
│    (ML-ready, geo-enriched features)    │
└─────────────────────────────────────────┘
```

---

## Non-Functional Requirements

| Requirement | Target |
|-------------|--------|
| Ingestion Latency | < 5 minutes from file arrival |
| Data Freshness | Near real-time (streaming) |
| Data Quality | > 99% records pass expectations |
| Scalability | Handle 10M+ transactions/day |
| Recovery | Checkpoint-based, exactly-once |
