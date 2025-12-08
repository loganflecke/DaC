# ROADMAP

## 1. **Detection Data-Source Mapper**

Map each detection to its required data sources by querying Splunk programmatically using Python + splunklib.


1. Use splunklib to authenticate and run metadata + field discovery searches
2. Parse detection YAML/JSON to extract field dependencies
3. Cross-reference required fields vs. indexed data
4. Generate a coverage report (CSV/Markdown)

**Outcome:**
Clear visibility into which detections are fully, partially, or not at all supported by available data sources. Enable extensive detection creation.

**Components:**
Python, splunklib, Splunk REST API, detection repository, search head.

---

## 2. **Lightweight Detection Test Runner**

Run detection searches automatically and evaluate them for correctness, stability, and execution behavior using Splunk’s API.


1. Build Python functions to run detection SPL on-demand
2. Validate SPL syntax, search performance, and field availability
3. Save results for each run (status, errors, timing, warnings)
4. Generate per-rule “unit test” summaries

**Outcome:**
A repeatable, code-driven framework for detecting broken, underperforming, or invalid detections before deployment.

**Components:**
Python, splunklib, Splunk KVStore or external local storage, Git repo of detections.

---

## 3. **Alert Noise & Stability Analyzer**

Evaluate detection alerts over time for frequency, stability, and noise patterns to automatically flag problematic rules.


1. Pull alert history via Splunk searches (stats/timechart)
2. Calculate frequency, burstiness, and long-term baselines
3. Identify noisy or silent detections
4. Produce visual or numerical stability scores

**Outcome:**
Prioritized list of detections that need tuning, with historical context, without requiring new attack simulations or sample data.

**Components:**
Python, splunklib, Splunk summary indexes or search queries, detection metadata.

---

## 4. **Detection Deployment Feasibility Checker (Infrastructure Fit Report)**

Automatically determine whether each detection can be realistically deployed based on your current Splunk environment and data availability.


1. Parse detection prerequisites (fields, indexes, evals)
2. Compare with actual Splunk ingestion
3. Identify pre-deployment blockers
4. Provide automated deployment readiness scoring

**Outcome:**
Confidence that the pipeline supports the detection—especially useful without an enterprise-grade data volume.

**Components:**
Detection repo, Python + splunklib, Splunk metadata endpoints.

---

## 5. **Data Attack Replay Simulator**

Replay very small, synthetic log samples to confirm functionality of detections without generating full-scale traffic.


1. Build synthetic event samples for a small set of attacks
2. Send events to Splunk with the HTTP Event Collector (HEC)
3. Validate detections hit on synthetic events
4. Provide “functional-only” test validation

**Outcome:**
A safe method to test detection logic without needing large data volumes or running full red-team simulations.

**Components:**
Python, Splunk HEC, synthetic logs, splunklib.

## Components

* GitLab CI/CD Pipeline
* Python
* Splunklib
* Detection Repository
* Splunk Enterprise
