# Task Breakdown: Fraud Detection Pipeline

## Phase 1: Setup
- [x] T001 Initialize DAB project structure with `databricks.yml`
- [x] T002 Configure environment variables (dev/staging/prod)
- [x] T003 Setup Unity Catalog schema references

## Phase 2: Foundational
- [x] T004 [P] Define Avro/JSON schemas for all source data
- [ ] T005 [P] Create base logging configuration
- [x] T006 Setup test framework (pytest + pyspark)
- [ ] T007 Create sample test data files

## Phase 3: User Story 1 - Bronze Layer (P1) - AUTO LOADER MANDATORY

**Per Constitution #3 & Plan AD-2: All Bronze tables MUST use Auto Loader (`cloudFiles`)**

### Contract Tests
- [x] T010 [P] Contract test: transactions JSON schema in `tests/contract/`
- [x] T011 [P] Contract test: customers CSV schema in `tests/contract/`
- [x] T012 [P] Contract test: country_coordinates CSV schema in `tests/contract/`
- [x] T013 [P] Contract test: fraud_reports CSV schema in `tests/contract/`

### Auto Loader Implementation (MANDATORY)
- [x] T014 Implement `bronze_transactions` with Auto Loader:
  - `cloudFiles.format = json`
  - `cloudFiles.inferColumnTypes = true`
  - `cloudFiles.schemaEvolutionMode = addNewColumns`
  - `cloudFiles.maxFilesPerTrigger = 1`
- [x] T015 Implement `banking_customers` with Auto Loader:
  - `cloudFiles.format = csv`
  - `cloudFiles.inferColumnTypes = true`
  - `multiLine = true`
  - Schema expectation: `_rescued_data IS NULL`
- [x] T016 Implement `country_coordinates` with Auto Loader:
  - `cloudFiles.format = csv`
  - `cloudFiles.inferColumnTypes = true`
- [x] T017 Implement `fraud_reports` with Auto Loader:
  - `cloudFiles.format = csv`
  - `cloudFiles.inferColumnTypes = true`

### Auto Loader Validation
- [x] T018 Unit test: Verify all Bronze tables use `cloudFiles` format
- [x] T019 Unit test: Verify `inferColumnTypes` enabled on all tables
- [x] T01A Unit test: Verify `schemaEvolutionMode` configured
- [x] T01B Compliance check: Bronze code matches plan AD-2 pattern

## Phase 4: User Story 2 - Silver Layer (P1)
- [x] T020 [P] Unit test: country code cleaning logic in `tests/unit/`
- [x] T021 [P] Unit test: balance diff calculation in `tests/unit/`
- [ ] T022 [P] Integration test: bronze → silver join in `tests/integration/`
- [x] T023 Implement `silver_transactions` table in `src/02-silver.py`
- [x] T024 Add data quality expectations (id NOT NULL, customer_id NOT NULL)
- [ ] T025 Verify streaming join behavior with fraud_reports

## Phase 5: User Story 3 - Gold Layer (P1)
- [x] T030 [P] Unit test: fraud flag coalesce logic in `tests/unit/`
- [ ] T031 [P] Unit test: geo-enrichment join logic in `tests/unit/`
- [ ] T032 [P] Integration test: silver → gold enrichment in `tests/integration/`
- [x] T033 Implement `gold_transactions` materialized view in `src/03-gold.py`
- [x] T034 Add amount expectation (amount > 10)
- [ ] T035 Verify all column mappings and aliases

## Phase 6: Deployment
- [x] T040 Create `resources/pipeline.yml` DLT definition
- [x] T041 Create `scripts/deploy.sh` deployment script
- [x] T042 Create `scripts/run_pipeline.sh` execution script
- [x] T043 Configure pipeline permissions (engineers, scientists, analysts)
- [x] T044 Setup scheduled job for production refresh

## Phase 7: Testing & Polish
- [x] T050 [P] E2E test: full pipeline with sample data in `tests/e2e/`
- [ ] T051 [P] E2E test: schema evolution scenario
- [ ] T052 [P] E2E test: incremental processing verification
- [ ] T053 Run all quickstart validation scenarios
- [x] T054 Generate CLAUDE.md context file
- [ ] T055 Final code review against constitution principles

## Phase 8: Production Readiness
- [ ] T060 Deploy to dev environment
- [ ] T061 Run integration tests against dev
- [ ] T062 Deploy to staging environment
- [ ] T063 Run E2E tests against staging
- [ ] T064 Production deployment approval
- [ ] T065 Deploy to production
- [ ] T066 Verify production pipeline health

---

## Progress Summary

| Phase | Total | Completed | Remaining |
|-------|-------|-----------|-----------|
| Phase 1: Setup | 3 | 3 | 0 |
| Phase 2: Foundational | 4 | 2 | 2 |
| Phase 3: Bronze Layer | 12 | 12 | 0 |
| Phase 4: Silver Layer | 6 | 4 | 2 |
| Phase 5: Gold Layer | 6 | 3 | 3 |
| Phase 6: Deployment | 5 | 5 | 0 |
| Phase 7: Testing & Polish | 6 | 2 | 4 |
| Phase 8: Production | 7 | 0 | 7 |
| **Total** | **49** | **31** | **18** |

**Implementation Progress: 63% Complete**

---

## Task Dependencies

```
T001 ──► T002 ──► T003 ✅
              │
              ▼
T004 ──► T010-T013 (parallel contract tests) ✅
              │
              ▼
         T014-T017 (parallel Auto Loader impl) ✅
              │
              ▼
         T018-T01B (parallel Auto Loader validation) ✅
              │
              ▼
T020-T022 ──► T023 ──► T024 ✅ (partial)
              │
              ▼
T030-T032 ──► T033 ──► T034 ✅ (partial)
              │
              ▼
         T040-T044 (parallel) ✅
              │
              ▼
         T050-T055 (parallel) ⏳
              │
              ▼
T060 ──► T061 ──► T062 ──► T063 ──► T064 ──► T065 ──► T066 ⏳
```

---

## Legend

- `[x]` = Completed
- `[ ]` = Pending
- `[P]` = Parallel task (can run concurrently with others in phase)
- `T0XX` = Task ID for tracking
- P1/P2/P3 = Priority (P1 = Must have, P2 = Should have, P3 = Nice to have)
