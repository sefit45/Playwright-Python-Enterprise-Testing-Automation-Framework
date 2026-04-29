# Playwright Python Automation Framework

Enterprise-level UI + API + Database Automation Framework built with:

* Python
* Pytest
* Playwright
* Requests
* SQLite
* Allure Reports
* HTML Reports
* Logging Framework
* Parallel Execution
* Retry Handling
* Environment Management
* Secret Handling with .env
* CI/CD Ready Structure

---

# Project Goal

This framework was designed to simulate real enterprise QA automation architecture used in large-scale production environments such as:

* Telecom systems
* Banking systems
* SaaS platforms
* CRM / Billing systems
* Enterprise web applications

The focus is not only test execution, but also:

* maintainability
* scalability
* reporting
* stability
* CI/CD readiness
* production-level framework design

---

# Project Structure

```text
playwright-python-framework/
│
├── API_Tests/
│   ├── api_client.py
│   ├── assertions.py
│   └── test_users_api.py
│
├── pages/
│   └── login_page.py
│
├── tests/
│   ├── test_login.py
│   ├── test_database.py
│   └── test_retry_demo.py
│
├── utils/
│   ├── logger.py
│   └── db_helper.py
│
├── logs/
│   └── test_execution.log
│
├── screenshots/
│
├── conftest.py
├── pytest.ini
├── requirements.txt
├── environments.json
├── test_data.json
├── .env
├── .gitignore
├── report.html
└── README.md
```

---

# Core Features

## UI Automation

Built with Playwright using:

* Page Object Model (POM)
* reusable fixtures
* centralized browser setup
* screenshot support
* clean architecture

Examples:

* login validation
* UI negative scenarios
* business flow validations

---

## API Automation

Built with reusable API client architecture

Supports:

* GET / POST validations
* response code validation
* JSON field validation
* negative API testing
* reusable assertions
* test data driven execution

Examples:

* validate existing user
* validate non-existing user
* create new post

---

## Database Validation

Built with SQLite helper layer

Supports:

* table creation
* insert validation
* select validation
* backend verification
* data consistency validation

This simulates enterprise backend validation scenarios.

---

## Logging Framework

Centralized logging using Python logging module

Provides:

* execution traceability
* debugging support
* production-grade investigation
* audit-ready execution history

Example log output:

INFO | Starting test
INFO | Sending API request
INFO | Received status code: 200

---

## Reporting

### HTML Report

Generated automatically using:

* pytest-html

Provides:

* execution summary
* passed / failed results
* fast debugging

### Allure Report

Enterprise-level reporting using:

* allure-pytest

Provides:

* detailed execution history
* logs
* retries
* test breakdown
* professional stakeholder presentation

---

## Parallel Execution

Built using:

* pytest-xdist

Supports:

* multi-worker execution
* faster regression cycles
* CI/CD optimization

Example:

```bash
pytest -n 4
```

---

## Retry Handling

Built using:

* pytest-rerunfailures

Supports:

* automatic retry for flaky failures
* temporary environment issues handling
* stable CI execution

Examples:

* API timeout
* slow UI loading
* temporary DB issue

---

## Test Markers

Custom markers:

* smoke
* sanity
* regression
* api
* ui
* negative
* critical
* db

Examples:

```bash
pytest -m smoke
pytest -m regression
pytest -m api
pytest -m db
```

---

## Environment Management

Supports multiple environments:

* dev
* qa
* prod

Managed via:

* environments.json

Example:

```bash
pytest --env=qa
```

---

## Secret Handling

Sensitive data managed using:

* .env

Supports:

* credentials
* tokens
* secrets
* private URLs

Prevents hardcoded security risks.

---

## CI/CD Ready

Framework designed for:

* Jenkins
* GitHub Actions
* GitLab CI
* Azure DevOps

Includes:

* clean structure
* retry strategy
* parallel execution
* reporting
* logs
* environment separation
* dependency management

---

# Installation

## Install dependencies

```bash
pip install -r requirements.txt
```

## Install Playwright browsers

```bash
playwright install
```

---

# Execute Tests

## Run all tests

```bash
pytest
```

## Run smoke tests

```bash
pytest -m smoke
```

## Run regression tests

```bash
pytest -m regression
```

## Run API tests

```bash
pytest -m api
```

## Run UI tests

```bash
pytest -m ui
```

## Run DB tests

```bash
pytest -m db
```

## Run with specific environment

```bash
pytest --env=qa
```

## Run in parallel

```bash
pytest -n 4
```

## Run with retry mechanism

```bash
pytest
```

(automatic retry is already configured in pytest.ini)

---

# Generate Allure Report

## Execute tests and create allure results

```bash
pytest --alluredir=allure-results
```

## Open Allure report

```bash
allure serve allure-results
```

---

# Example Jenkins Flow

```bash
git clone project
cd project
pip install -r requirements.txt
playwright install
pytest -m smoke
allure generate
```

This is real enterprise CI/CD execution.

---

# Interview-Level Summary

I built a reusable enterprise-level automation framework using Playwright with Python, covering UI testing, API testing, database validation, reporting, retry handling, environment management, secret handling, and CI/CD readiness across complex production environments.

---

# Why This Framework

This project demonstrates not only automation skills, but also:

* architecture thinking
* senior QA mindset
* production readiness
* enterprise delivery standards

This is not just test scripts.

This is Automation Engineering.