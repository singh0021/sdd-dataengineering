# Requirements Checklist

## Data Sources

### Transactions (JSON)
- [ ] Source path configured: `/Volumes/main__build/dbdemos_fsi_fraud_detection/fraud_raw_data/transactions`
- [ ] Format: JSON
- [ ] Schema inference enabled
- [ ] Rate limiting configured (maxFilesPerTrigger)
- [ ] Streaming mode enabled

### Customers (CSV)
- [ ] Source path configured: `/Volumes/main__build/dbdemos_fsi_fraud_detection/fraud_raw_data/customers`
- [ ] Format: CSV
- [ ] Schema inference enabled
- [ ] Multi-line support enabled
- [ ] Schema validation expectation added

### Country Coordinates (CSV)
- [ ] Source path configured: `/Volumes/main__build/dbdemos_fsi_fraud_detection/fraud_raw_data/country_code`
- [ ] Format: CSV
- [ ] Streaming mode enabled

### Fraud Reports (CSV)
- [ ] Source path configured: `/Volumes/main__build/dbdemos_fsi_fraud_detection/fraud_raw_data/fraud_report`
- [ ] Format: CSV
- [ ] Streaming mode enabled

---

## Bronze Layer

### bronze_transactions
- [ ] Table decorator with name and comment
- [ ] Auto Loader with cloudFiles format
- [ ] JSON format specified
- [ ] Column type inference enabled
- [ ] Max files per trigger set to 1

### banking_customers
- [ ] Table decorator with name and comment
- [ ] Auto Loader with cloudFiles format
- [ ] CSV format specified
- [ ] Column type inference enabled
- [ ] Multi-line option enabled
- [ ] Schema expectation: `_rescued_data IS NULL`

### country_coordinates
- [ ] Table decorator with name
- [ ] Auto Loader with cloudFiles format
- [ ] CSV format specified

### fraud_reports
- [ ] Table decorator with name
- [ ] Auto Loader with cloudFiles format
- [ ] CSV format specified

---

## Silver Layer

### silver_transactions
- [ ] Table decorator with name and comment
- [ ] Streaming read from bronze_transactions
- [ ] Batch read from fraud_reports
- [ ] LEFT JOIN on id column
- [ ] Country code cleaning (regexp_replace)
- [ ] Balance diff calculations (diffOrig, diffDest)
- [ ] _rescued_data columns excluded
- [ ] Expectation: `id IS NOT NULL`
- [ ] Expectation: `customer_id IS NOT NULL`

---

## Gold Layer

### gold_transactions
- [ ] Materialized view decorator with name and comment
- [ ] Batch read from silver_transactions
- [ ] Batch read from country_coordinates (aliased twice)
- [ ] Batch read from banking_customers
- [ ] INNER JOIN: countryOrig = alpha3_code (origin)
- [ ] INNER JOIN: countryDest = alpha3_code (destination)
- [ ] INNER JOIN: customer_id = id (customers)
- [ ] Fraud flag coalesced and cast to boolean
- [ ] Geographic columns mapped with aliases
- [ ] Customer columns included (excluding id, _rescued_data)
- [ ] Expectation: `amount > 10`

---

## Data Quality

- [ ] Bronze schema validation for customers
- [ ] Silver null checks for id and customer_id
- [ ] Gold amount threshold validation
- [ ] Expectations use descriptive names
- [ ] Appropriate action for each expectation (drop/fail/warn)

---

## Testing

- [ ] Contract tests for all source schemas
- [ ] Unit tests for transformation logic
- [ ] Integration tests for joins
- [ ] E2E tests for full pipeline
- [ ] Sample test data created

---

## Deployment

- [ ] DAB configuration (databricks.yml)
- [ ] Pipeline resource definition (resources/pipeline.yml)
- [ ] Dev/staging/prod targets configured
- [ ] Permissions configured
- [ ] Deployment scripts created
