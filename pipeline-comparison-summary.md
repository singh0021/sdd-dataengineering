# Pipeline Comparison Summary

**Date:** 2026-02-19
**Directories Compared:**
- `fsi-lakehouse/src/`
- `databricks-transformation/`

## Overview

Both directories contain the same three files implementing a medallion architecture for fraud detection:
- `01-bronze.py` - Raw data ingestion
- `02-silver.py` - Data cleansing & enrichment
- `03-gold.py` - ML-ready feature engineering

**Verdict:** The files are **NOT identical**. The `fsi-lakehouse` version is more polished with additional configuration and documentation.

---

## Detailed Comparison

### 01-bronze.py

| Feature | fsi-lakehouse | databricks-transformation |
|---------|---------------|---------------------------|
| Lines of code | 91 | 72 |
| Header comments | Detailed with Constitution reference | Basic |
| `schemaEvolutionMode` option | All 4 tables | None |
| `inferColumnTypes` option | All 4 tables | Only 2 tables (transactions, customers) |
| Table comments in decorator | All 4 tables | Only 2 tables |

**Key Differences:**

1. **Schema Evolution Mode**
   - fsi-lakehouse includes `.option("cloudFiles.schemaEvolutionMode", "addNewColumns")` on all tables
   - databricks-transformation omits this option entirely

2. **Type Inference**
   - fsi-lakehouse: `inferColumnTypes` on all 4 tables
   - databricks-transformation: Missing on `country_coordinates` and `fraud_reports`

3. **Documentation**
   - fsi-lakehouse: References "Constitution #3" and includes detailed section headers
   - databricks-transformation: Basic inline comments only

---

### 02-silver.py

| Feature | fsi-lakehouse | databricks-transformation |
|---------|---------------|---------------------------|
| Lines of code | 54 | 37 |
| Header comments | Detailed with layer description | None |
| Inline comments | Extensive | Minimal |
| Core transformation logic | Identical | Identical |

**Functional Equivalence:** Yes - same joins, column selections, and transformations

**Differences are documentation only:**
- fsi-lakehouse includes section headers and explains each transformation step
- fsi-lakehouse references "Constitution #1" and "Plan AD-4"

---

### 03-gold.py

| Feature | fsi-lakehouse | databricks-transformation |
|---------|---------------|---------------------------|
| Lines of code | 67 | 39 |
| Header comments | Detailed with layer description | None |
| Materialized view comment | "ML-ready transactions for Data Scientists - geo-enriched with customer features" | "Gold, ready for Data Scientists to consume" |
| Inline comments | Extensive | Minimal |
| Core transformation logic | Identical | Identical |

**Functional Equivalence:** Yes - same joins, column selections, and transformations

**Differences are documentation only:**
- fsi-lakehouse includes section headers and explains join strategy
- fsi-lakehouse references "Plan AD-3" and "Plan AD-5"

---

## Summary Table

| File | Logic Match | Config Match | Documentation Match |
|------|-------------|--------------|---------------------|
| 01-bronze.py | Partial | No | No |
| 02-silver.py | Yes | Yes | No |
| 03-gold.py | Yes | Yes | No |

---

## Recommendations

1. **If consolidating:** Use `fsi-lakehouse` as the source of truth - it has better documentation and more robust configuration (schema evolution)

2. **Key missing features in databricks-transformation:**
   - Add `schemaEvolutionMode` to all bronze tables for production resilience
   - Add `inferColumnTypes` to `country_coordinates` and `fraud_reports`

3. **Documentation:** The `fsi-lakehouse` version follows SDD (Spec-Driven Development) practices with traceability to specifications
