# Data Model: Fraud Detection Pipeline

## Entity Relationship Diagram

```
┌─────────────────────┐       ┌─────────────────────┐
│   banking_customers │       │  country_coordinates│
├─────────────────────┤       ├─────────────────────┤
│ PK  id              │       │ PK  alpha3_code     │
│     name            │       │     country         │
│     email           │       │     lat_avg         │
│     ...             │       │     long_avg        │
└──────────┬──────────┘       └──────────┬──────────┘
           │                             │
           │ customer_id                 │ countryOrig/countryDest
           │                             │
           ▼                             ▼
┌─────────────────────────────────────────────────────┐
│                 bronze_transactions                  │
├─────────────────────────────────────────────────────┤
│ PK  id                                              │
│ FK  customer_id → banking_customers.id              │
│     amount                                          │
│     countryOrig → country_coordinates.alpha3_code   │
│     countryDest → country_coordinates.alpha3_code   │
│     oldBalanceOrig                                  │
│     newBalanceOrig                                  │
│     oldBalanceDest                                  │
│     newBalanceDest                                  │
│     _rescued_data                                   │
└──────────┬──────────────────────────────────────────┘
           │
           │ id
           │
           ▼
┌─────────────────────┐
│    fraud_reports    │
├─────────────────────┤
│ FK  id → bronze_transactions.id                     │
│     is_fraud (0/1)  │
└─────────────────────┘
```

---

## Table Schemas

### Bronze Layer

#### bronze_transactions
| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | STRING | NO | Transaction identifier (PK) |
| customer_id | STRING | YES | Customer reference |
| amount | DOUBLE | YES | Transaction amount |
| countryOrig | STRING | YES | Origin country code |
| countryDest | STRING | YES | Destination country code |
| oldBalanceOrig | DOUBLE | YES | Origin balance before |
| newBalanceOrig | DOUBLE | YES | Origin balance after |
| oldBalanceDest | DOUBLE | YES | Destination balance before |
| newBalanceDest | DOUBLE | YES | Destination balance after |
| _rescued_data | STRING | YES | Schema mismatch data |

#### banking_customers
| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | STRING | NO | Customer identifier (PK) |
| name | STRING | YES | Customer name |
| email | STRING | YES | Contact email |
| ... | ... | ... | Additional attributes (inferred) |
| _rescued_data | STRING | YES | Schema mismatch data |

#### country_coordinates
| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| alpha3_code | STRING | NO | ISO 3166-1 alpha-3 code (PK) |
| country | STRING | YES | Country name |
| lat_avg | DOUBLE | YES | Average latitude |
| long_avg | DOUBLE | YES | Average longitude |

#### fraud_reports
| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| id | STRING | NO | Transaction ID (FK) |
| is_fraud | INTEGER | YES | Fraud label (1=fraud, 0=legit) |

---

### Silver Layer

#### silver_transactions
| Column | Type | Source | Description |
|--------|------|--------|-------------|
| id | STRING | bronze_transactions | Transaction ID |
| customer_id | STRING | bronze_transactions | Customer reference |
| amount | DOUBLE | bronze_transactions | Transaction amount |
| countryOrig | STRING | CLEANED | Origin country (-- removed) |
| countryDest | STRING | CLEANED | Destination country (-- removed) |
| oldBalanceOrig | DOUBLE | bronze_transactions | Balance before (origin) |
| newBalanceOrig | DOUBLE | bronze_transactions | Balance after (origin) |
| oldBalanceDest | DOUBLE | bronze_transactions | Balance before (dest) |
| newBalanceDest | DOUBLE | bronze_transactions | Balance after (dest) |
| is_fraud | INTEGER | fraud_reports | Fraud label (nullable) |
| diffOrig | DOUBLE | CALCULATED | newBalanceOrig - oldBalanceOrig |
| diffDest | DOUBLE | CALCULATED | newBalanceDest - oldBalanceDest |

---

### Gold Layer

#### gold_transactions
| Column | Type | Source | Description |
|--------|------|--------|-------------|
| id | STRING | silver | Transaction ID |
| customer_id | STRING | silver | Customer reference |
| amount | DOUBLE | silver | Transaction amount |
| diffOrig | DOUBLE | silver | Origin balance change |
| diffDest | DOUBLE | silver | Destination balance change |
| is_fraud | BOOLEAN | COALESCED | Fraud indicator (false if null) |
| countryOrig | STRING | country_coordinates | Origin country code |
| countryOrig_name | STRING | country_coordinates | Origin country name |
| countryLongOrig_long | DOUBLE | country_coordinates | Origin longitude |
| countryLatOrig_lat | DOUBLE | country_coordinates | Origin latitude |
| countryDest | STRING | country_coordinates | Destination country code |
| countryDest_name | STRING | country_coordinates | Destination country name |
| countryLongDest_long | DOUBLE | country_coordinates | Destination longitude |
| countryLatDest_lat | DOUBLE | country_coordinates | Destination latitude |
| [customer fields] | VARIOUS | banking_customers | Customer attributes |

---

## Data Lineage

```
/Volumes/.../transactions (JSON)
         │
         ▼
   bronze_transactions ─────┐
         │                  │
         │                  ▼
         │           fraud_reports
         │                  │
         ▼                  │
   silver_transactions ◄────┘
         │
         ├──────────────────┬──────────────────┐
         │                  │                  │
         ▼                  ▼                  ▼
country_coordinates  country_coordinates  banking_customers
    (origin)            (dest)
         │                  │                  │
         └──────────────────┴──────────────────┘
                           │
                           ▼
                   gold_transactions
                           │
                           ▼
                     ML Models
```

---

## Partitioning Strategy

| Table | Partition Key | Rationale |
|-------|---------------|-----------|
| bronze_transactions | None (Auto Loader managed) | Small files, streaming |
| silver_transactions | None | Streaming destination |
| gold_transactions | None | Materialized view |

*Note: Consider partitioning by date for large-scale production*

---

## Retention Policy

| Layer | Retention | Rationale |
|-------|-----------|-----------|
| Bronze | 90 days | Audit, reprocessing |
| Silver | 30 days | Standard retention |
| Gold | Indefinite | ML training history |
