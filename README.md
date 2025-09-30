# Detection as Code (DaC)

This project demonstrates a **Detection-as-Code (DaC) pipeline** implemented in **GitLab CI/CD**. It serves as an experimental framework for automating detection engineering workflows while leveraging GitLab's strong CI/CD capabilities.

## Project Goals

* Version control
* Automated deployments
* Testing without dev/test environment

## Pipeline Overview

The `.gitlab-ci.yml` pipeline currently focuses on deployment workflows. Future updates may include validation and linting.

## Splunk Integration

The repository also includes support for **Splunk**:

* A Python script leverages the **Splunk SDK** to create or update detections.
* Future work will include testing **Sigma to Splunk conversion limitations** (e.g., Sigma’s support for data models, calculated fields, `stats`, etc.).

## Elastic Integration

This repo includes a **deploy to Elastic script** that pushes rules into an **ElastAlert**-based workflow.

* Important limitation: After deployment, **ElastAlert must be restarted** for changes to take effect.
* The **Elastic Community Edition** does not currently support a seamless DaC integration.
