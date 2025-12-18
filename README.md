# Detection-as-Code (DaC)

> **New! Automatic Splunk Detection Data Validation**
> This small utility validates that all fields referenced in deployed Splunk detections actually exist in indexes and sourcetypes. It ensures detection logic runs reliably, reduces false positives, and gives immediate feedback on missing or misconfigured fields—boosting confidence in detection pipeline.

This repository implements a Detection-as-Code workflow: author Sigma detection rules, convert them to Splunk alert JSON, and programmatically deploy them to Splunk for execution and analysis.

---
![Detection_as_Code](./Detection_as_Code.png)
---

## Overview

This project is a compact pipeline that enables:

* Writing detection logic as Sigma rules under `rules/`
* Converting Sigma rules into Splunk-compatible search queries and base alert JSON (`convert_to_splunk_alert.py`)
* Deploying alerts to Splunk with full metadata and actions (`deploy_to_splunk.py`)
* Writing alert results to a dedicated index for downstream detection analysis
* Validating that all fields used in Splunk detections exist in the appropriate index/sourcetype (`detection_data_validation.py`)

  * This helps catch misconfigured alerts, missing data sources, and prevents runtime errors.

* Version control and iterative rule testing

All detections are treated as versioned code artifacts, allowing reproducibility, tuning, and historical tracking.

---

## Repository Structure

```
DaC/
├── rules/                         # Sigma detection rules (YAML)
│   └── windows/                   # OS/category-specific rule subfolders
├── convert_to_splunk_alert.py     # Converts Sigma rules → Splunk SPL + base alert JSON
├── deploy_to_splunk.py            # Deploys alerts to Splunk; adds metadata + actions
├── detection_data_validation.py   # Validates that fields used in detections exist in Splunk
├── gitlab-ci.yml                   # Optional CI pipeline for automated deployment/testing
└── README.md
```

---

## Workflow (Current)

1. **Write or edit Sigma rules**

   * Place rules in `rules/` (e.g., `rules/windows/my_suspicious_login.yml`).

2. **Convert Sigma → Splunk alert JSON**

   * Run `convert_to_splunk_alert.py`
   * The script generates a Splunk alert JSON with the search query derived from the Sigma rule.
   * This is a base alert definition (no schedule or alert actions yet).

3. **Deploy alerts to Splunk**

   * Run `deploy_to_splunk.py`
   * Reads the JSON output from `convert_to_splunk_alert.py`
   * Adds alert metadata (name, description, severity, cron schedule) and alert actions (e.g., writing results to your designated index)
   * Creates or updates the alert in Splunk via the REST API

4. **Validate detection fields (new)**

   * Run `detection_data_validation.py`
   * Checks that all fields referenced in your deployed searches exist in the target index/sourcetype
   * Prints missing fields (if any) and prevents silent misfires
   * Helps ensure that all detections will run successfully and provide reliable telemetry

5. **Alert execution and telemetry ingestion**

   * Alerts run according to the configured schedule in Splunk
   * Results are written to a dedicated index for detection analytics, tuning, or version comparison

---

## Splunk Integration Notes

* `convert_to_splunk_alert.py` handles the Sigma-to-SPL conversion and produces the base JSON used for alert creation.
* `deploy_to_splunk.py` completes the alert definition with scheduling, severity, and actions before deploying it via the API.
* `detection_data_validation.py` ensures that all referenced fields exist before relying on alerts for analysis.
* All alert results are centralized in a Splunk index, which is the foundation for downstream detection analysis (telemetry dashboards, tuning, false-positive tracking).

---

## Usage

```bash
# Convert Sigma rules to base Splunk alert JSON
python convert_to_splunk_alert.py

# Deploy alerts to Splunk with metadata/actions
python deploy_to_splunk.py

# Validate that all fields used in detections exist in Splunk
python detection_data_validation.py
```

* Edit rules in `rules/` before conversion to update detection logic.
* Run validation to catch missing or misconfigured fields early.
* Alerts are automatically created/updated and start sending results to your configured index.
