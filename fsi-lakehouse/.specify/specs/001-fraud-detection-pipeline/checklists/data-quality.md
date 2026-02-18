# Data Quality Checklist

## Schema Validation

### Bronze Layer
- [ ] All tables capture `_rescued_data` for schema mismatches
- [ ] `banking_customers` drops rows with non-null `_rescued_data`
- [ ] Schema inference enabled for flexible source schemas
- [ ] No explicit schema enforcement at bronze (raw ingestion)

### Silver Layer
- [ ] Transaction ID cannot be NULL
- [ ] Customer ID cannot be NULL
- [ ] `_rescued_data` columns excluded from output

### Gold Layer
- [ ] All joins are INNER (complete data only)
- [ ] Fraud flag has no NULLs (coalesced to false)
- [ ] Amount threshold validated (> 10)

---

## Transformation Validation

### Country Code Cleaning
- [ ] Double-dash prefix removed: `--USA` → `USA`
- [ ] Single-dash handled: `-USA` → `USA` (verify behavior)
- [ ] Empty string handled gracefully
- [ ] NULL values preserved as NULL

### Balance Calculations
- [ ] diffOrig = newBalanceOrig - oldBalanceOrig
- [ ] diffDest = newBalanceDest - oldBalanceDest
- [ ] NULL inputs produce NULL outputs
- [ ] No overflow for large values

### Fraud Flag Coalesce
- [ ] NULL → 0 → false
- [ ] 1 → true
- [ ] 0 → false
- [ ] Type is BOOLEAN in gold layer

---

## Referential Integrity

### Transactions → Customers
- [ ] INNER JOIN ensures all gold transactions have customer data
- [ ] Orphan transactions (invalid customer_id) excluded from gold
- [ ] Customer ID format consistent between tables

### Transactions → Country Coordinates
- [ ] Both origin and destination lookups succeed for gold records
- [ ] Invalid country codes excluded via INNER JOIN
- [ ] Alpha3 codes are case-sensitive (verify source data)

### Transactions → Fraud Reports
- [ ] LEFT JOIN preserves transactions without labels
- [ ] Fraud labels correctly matched by transaction ID
- [ ] No duplicate labels per transaction

---

## Data Freshness

- [ ] Bronze: Near real-time (streaming Auto Loader)
- [ ] Silver: Near real-time (streaming from bronze)
- [ ] Gold: Materialized view refresh frequency documented
- [ ] Checkpoint paths configured for recovery

---

## Data Completeness

### Required Fields (Silver)
- [ ] id: NOT NULL enforced
- [ ] customer_id: NOT NULL enforced

### Expected Fields (Gold)
- [ ] All geographic columns populated (INNER JOIN)
- [ ] All customer columns populated (INNER JOIN)
- [ ] is_fraud never NULL (coalesced)

---

## Expectation Summary

| Layer | Table | Expectation | Expression | Action |
|-------|-------|-------------|------------|--------|
| Bronze | banking_customers | correct_schema | `_rescued_data IS NULL` | Drop |
| Silver | silver_transactions | correct_data | `id IS NOT NULL` | Fail |
| Silver | silver_transactions | correct_customer_id | `customer_id IS NOT NULL` | Fail |
| Gold | gold_transactions | amount_decent | `amount > 10` | Warn |

---

## Monitoring Metrics

- [ ] Records processed per batch/trigger
- [ ] Expectation pass/fail rates
- [ ] Join success rates (records matched vs. dropped)
- [ ] Pipeline latency (source file → gold table)
- [ ] Schema evolution events (rescued data count)
