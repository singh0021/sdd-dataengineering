# Spec-Driven Development (SDD) for Data Engineering

A comprehensive guide for building data pipelines using the SDD methodology.

---

## What is SDD?

**Spec-Driven Development** is a methodology where specifications drive implementation:

```
Specifications → Plan → Tasks → Code
```

Instead of writing code directly, you:
1. Define **what** you want to build (specification)
2. Define **how** to build it (plan)
3. Break it into **tasks** (task breakdown)
4. Generate **code** from specs (implementation)

---

## Why SDD for Data Engineering?

| Benefit | Description |
|---------|-------------|
| **Consistency** | Constitution ensures all code follows same standards |
| **Documentation** | Specs serve as living documentation |
| **Traceability** | Clear link from requirements to implementation |
| **AI-Assisted** | Claude Code can implement from specs |
| **Quality** | Built-in checklists and contracts |

---

## SDD Artifacts

### 1. Constitution (`constitution.md`)

**Purpose:** Define project-wide principles and standards.

**Contains:**
- Data quality requirements
- Technology standards
- Code conventions
- Testing requirements

**Example Principles for Databricks:**
```markdown
### Auto Loader for Ingestion
All Bronze tables MUST use Auto Loader (cloudFiles)

### Medallion Architecture
Bronze → Silver → Gold layering

### Data Quality
Use @dp.expect for all critical rules
```

---

### 2. Specification (`spec.md`)

**Purpose:** Define WHAT to build and WHY.

**Contains:**
- Overview
- User stories with acceptance criteria
- Data flow diagrams
- Non-functional requirements

**Template:**
```markdown
# Feature Specification: [Name]

## Overview
[Description]

## User Stories

### US-1: [Title]
**As a** [role]
**I want** [capability]
**So that** [benefit]

**Acceptance Criteria:**
- [ ] [Criterion]
```

---

### 3. Plan (`plan.md`)

**Purpose:** Define HOW to build it.

**Contains:**
- Technology stack
- Architecture decisions
- Pipeline components
- Data quality strategy
- Deployment environments

**Template:**
```markdown
# Technical Plan: [Name]

## Technology Stack
| Component | Technology | Rationale |

## Architecture Decisions
### AD-1: [Decision]
**Decision:** [What]
**Rationale:** [Why]
**Trade-offs:** [Pros/Cons]

## Pipeline Components
### [Layer] Layer
| Table | Source | Format | Options |
```

---

### 4. Tasks (`tasks.md`)

**Purpose:** Define implementation ORDER.

**Contains:**
- Phased task breakdown
- Task dependencies
- Progress tracking

**Template:**
```markdown
# Task Breakdown: [Name]

## Phase 1: Setup
- [ ] T001 [Task]
- [ ] T002 [Task]

## Phase 2: [Feature]
- [ ] T010 [Task]

## Progress Summary
| Phase | Completed | Remaining |
```

---

## SDD Workflow

### Step 1: Initialize Project

```bash
# Create directory structure
mkdir -p my-pipeline/.specify/{memory,specs/001-feature/{checklists,contracts/schemas}}
mkdir -p my-pipeline/{src,resources,scripts,tests/{contract,unit,integration,e2e}}

# Navigate to project
cd my-pipeline
```

### Step 2: Write Constitution

```bash
# In Claude Code
claude

/speckit.constitution Create principles for a [describe your pipeline]
with [key requirements like Auto Loader, data quality, etc.]
```

Or manually create `.specify/memory/constitution.md`

### Step 3: Write Specification

```bash
/speckit.specify Build a [describe your feature] that [key capabilities]
```

Or manually create `.specify/specs/001-feature/spec.md`

### Step 4: Create Plan

```bash
/speckit.plan [Your tech stack: Databricks, Delta Lake, Auto Loader, etc.]
```

Or manually create `.specify/specs/001-feature/plan.md`

### Step 5: Generate Tasks

```bash
/speckit.tasks
```

Or manually create `.specify/specs/001-feature/tasks.md`

### Step 6: Implement

```bash
/speckit.implement
```

---

## Directory Structure Template

```
my-pipeline/
├── databricks.yml                 # DAB configuration
├── README.md                      # Project documentation
├── CLAUDE.md                      # AI context
│
├── src/                           # Pipeline code
│   ├── 01-bronze.py
│   ├── 02-silver.py
│   └── 03-gold.py
│
├── resources/                     # Deployment configs
│   └── pipeline.yml
│
├── scripts/                       # Automation
│   ├── deploy.sh
│   ├── run_pipeline.sh
│   └── destroy.sh
│
├── tests/                         # Test suites
│   ├── contract/
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
└── .specify/                      # SDD artifacts
    ├── memory/
    │   └── constitution.md
    └── specs/001-feature/
        ├── spec.md
        ├── plan.md
        ├── research.md
        ├── data-model.md
        ├── quickstart.md
        ├── tasks.md
        ├── checklists/
        │   ├── requirements.md
        │   └── data-quality.md
        └── contracts/schemas/
            └── *.json
```

---

## SDD Commands Reference

| Command | Purpose | Input |
|---------|---------|-------|
| `/speckit.constitution` | Create project principles | Description of standards |
| `/speckit.specify` | Create feature spec | Feature description |
| `/speckit.clarify` | Resolve ambiguities | Questions to answer |
| `/speckit.plan` | Create technical plan | Tech stack |
| `/speckit.tasks` | Generate task breakdown | (reads spec + plan) |
| `/speckit.implement` | Execute tasks | (reads all artifacts) |
| `/speckit.analyze` | Check consistency | (validates artifacts) |
| `/speckit.checklist` | Generate checklist | Checklist type |

---

## Best Practices

### Constitution
- Keep principles actionable and testable
- Include code examples for standards
- Reference principles by number in other docs

### Specification
- Focus on WHAT and WHY, not HOW
- Write clear acceptance criteria
- Include data flow diagrams

### Plan
- Document all architecture decisions
- Include code templates/patterns
- Define data quality strategy upfront

### Tasks
- Keep tasks small and specific
- Mark parallel tasks with `[P]`
- Update progress regularly

---

## Example: Databricks Pipeline

### Constitution Excerpt
```markdown
### Auto Loader for Bronze (MANDATORY)
All Bronze tables MUST use:
- `cloudFiles.format`
- `cloudFiles.inferColumnTypes`
- `cloudFiles.schemaEvolutionMode`
```

### Spec Excerpt
```markdown
### US-1: Raw Data Ingestion
**As a** Data Engineer
**I want** to ingest data via Auto Loader
**So that** I have schema evolution support

**Acceptance Criteria:**
- [ ] All Bronze tables use cloudFiles format
- [ ] Schema inference enabled
```

### Plan Excerpt
```markdown
### AD-1: Auto Loader for Bronze
**Decision:** Use cloudFiles for all Bronze tables
**Rationale:** Schema inference, exactly-once processing
**Code Pattern:**
```python
spark.readStream.format("cloudFiles")...
```
```

### Tasks Excerpt
```markdown
## Phase 2: Bronze Layer
- [ ] T010 Implement bronze_table_1 with Auto Loader
- [ ] T011 Implement bronze_table_2 with Auto Loader
- [ ] T012 Add schema validation expectations
```

---

## Troubleshooting

### Spec-kit not installed
```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
```

### Commands not recognized
Ensure you're running inside Claude Code (`claude` CLI).

### Artifacts out of sync
Run `/speckit.analyze` to check consistency.

### Tasks not updating
Manually edit `tasks.md` or regenerate with `/speckit.tasks`.

---

## References

- [Spec-Kit Repository](https://github.com/github/spec-kit)
- [Databricks Asset Bundles](https://docs.databricks.com/dev-tools/bundles/)
- [Delta Live Tables](https://docs.databricks.com/delta-live-tables/)
- [Auto Loader](https://docs.databricks.com/ingestion/auto-loader/)
