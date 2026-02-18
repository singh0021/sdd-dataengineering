# Quickstart: Validation Scenarios

## Key Validation Scenarios

### Scenario 1: Happy Path - Normal Data Flow

**Setup:**
1. Place valid JSON transaction file in `/Volumes/.../transactions/`
2. Ensure matching customer and country reference data exists

**Expected Results:**
- Bronze: Transaction appears in `bronze_transactions`
- Silver: Transaction joined with fraud_reports, cleansed
- Gold: Transaction enriched with geo coordinates and customer data

**Validation Query:**
```sql
-- Verify end-to-end flow
SELECT COUNT(*) FROM gold_transactions
WHERE id = '<test_transaction_id>'
```

---

### Scenario 2: Schema Mismatch Handling

**Setup:**
1. Place CSV with extra/missing columns in `/Volumes/.../customers/`

**Expected Results:**
- Bronze: Row captured with `_rescued_data` populated
- Silver: Row excluded due to `correct_schema` expectation

**Validation Query:**
```sql
-- Check rescued data
SELECT * FROM banking_customers
WHERE _rescued_data IS NOT NULL
```

---

### Scenario 3: Missing Fraud Label

**Setup:**
1. Transaction ID not present in fraud_reports

**Expected Results:**
- Silver: Transaction present with `is_fraud = NULL`
- Gold: Transaction has `is_fraud = false` (coalesced)

**Validation Query:**
```sql
-- Verify coalesce behavior
SELECT id, is_fraud FROM gold_transactions
WHERE id NOT IN (SELECT id FROM fraud_reports)
```

---

### Scenario 4: Invalid Country Code

**Setup:**
1. Transaction with `countryOrig = 'XXX'` (invalid code)

**Expected Results:**
- Bronze: Transaction ingested as-is
- Silver: Transaction present with cleaned country code
- Gold: Transaction **excluded** (INNER JOIN fails)

**Validation Query:**
```sql
-- Should return 0
SELECT COUNT(*) FROM gold_transactions
WHERE countryOrig = 'XXX'
```

---

### Scenario 5: Dirty Country Code Cleaning

**Setup:**
1. Transaction with `countryOrig = '--USA'`

**Expected Results:**
- Bronze: Raw value preserved
- Silver: Cleaned to `countryOrig = 'USA'`
- Gold: Enriched with USA coordinates

**Validation Query:**
```sql
-- Verify cleaning
SELECT
  b.countryOrig as bronze_value,
  s.countryOrig as silver_value
FROM bronze_transactions b
JOIN silver_transactions s ON b.id = s.id
WHERE b.countryOrig LIKE '--%'
```

---

### Scenario 6: Low-Value Transaction Warning

**Setup:**
1. Transaction with `amount = 5` (below 10 threshold)

**Expected Results:**
- Gold: Transaction present (expectation is warn, not fail)
- Pipeline: Warning logged in DLT metrics

**Validation Query:**
```sql
-- Should return results
SELECT * FROM gold_transactions
WHERE amount <= 10
```

---

### Scenario 7: Null Transaction ID Rejection

**Setup:**
1. Attempt to insert transaction with `id = NULL`

**Expected Results:**
- Silver: Pipeline fails with `correct_data` expectation violation

**Validation:**
- Check DLT pipeline run status
- Verify expectation failure in metrics

---

### Scenario 8: Incremental Processing

**Setup:**
1. Run pipeline with initial data
2. Add new file to transactions folder
3. Run pipeline again

**Expected Results:**
- Only new records processed (not full reprocessing)
- Checkpoint advanced

**Validation Query:**
```sql
-- Compare counts before/after
SELECT COUNT(*) FROM bronze_transactions
```

---

## End-to-End Test Data

### Sample Transaction (JSON)
```json
{
  "id": "TEST001",
  "customer_id": "CUST001",
  "amount": 1500.00,
  "countryOrig": "USA",
  "countryDest": "GBR",
  "oldBalanceOrig": 10000.00,
  "newBalanceOrig": 8500.00,
  "oldBalanceDest": 5000.00,
  "newBalanceDest": 6500.00
}
```

### Sample Customer (CSV)
```csv
id,name,email
CUST001,John Doe,john@example.com
```

### Sample Country (CSV)
```csv
alpha3_code,country,lat_avg,long_avg
USA,United States,37.0902,-95.7129
GBR,United Kingdom,55.3781,-3.4360
```

### Sample Fraud Report (CSV)
```csv
id,is_fraud
TEST001,0
```

---

## Validation Checklist

- [ ] Happy path transaction flows through all layers
- [ ] Schema mismatch captured in _rescued_data
- [ ] Missing fraud labels handled gracefully
- [ ] Invalid country codes excluded from gold
- [ ] Country codes cleaned properly
- [ ] Low-value transactions generate warnings
- [ ] Null IDs rejected at silver layer
- [ ] Incremental processing works correctly
