# DevOpsMortCal – Mortgage Calculator with DevOps Pipeline

![Project Badge](https://img.shields.io/badge/DevOps-Portfolio-green)

## Project Overview

**DevOpsMortCal** is a Python-based mortgage calculator web application that calculates monthly mortgage payments, generates loan amortization schedules, and visually compares payoff scenarios based on different payment strategies. Users can see how extra payments impact total interest paid and loan duration.

This repository also serves as a **DevOps portfolio project**, demonstrating:

* End-to-end **CI/CD pipelines** with GitHub Actions
* **Containerization** with Docker
* **Infrastructure as Code** with Terraform
* **Multi-environment cloud deployment** using Azure Container Apps
* **Observability** via Azure Log Analytics
* **Code quality & security enforcement** with pre-commit hooks and unit tests

---

## Architecture Overview

```
GitHub Repo
     │
     ├─> GitHub Actions (CI/CD)
             │
             ├─> Docker Hub
                     │
                     ├─> Azure Container Apps (Staging / Production)
                             │
                             └─> Logs → Azure Log Analytics
```

* **Source Code:** GitHub
* **Container Images:** Docker Hub
* **Hosting Environments:** Staging and Production (Azure Container Apps)
* **Observability:** Azure Log Analytics
* **CI/CD:** GitHub Actions with automated builds, tests, and deployments

---

## CI/CD Pipeline Overview

| Branch / Action | Trigger        | Pipeline Steps                                                              | Environment |
| --------------- | -------------- | --------------------------------------------------------------------------- | ----------- |
| Feature → Dev   | Pull Request   | Pre-commit checks, unit tests                                               | None        |
| Merge → Main    | Push to `main` | Pre-commit, unit tests, build & push image, deploy to Staging               | Staging     |
| GitHub Release  | Tag `vX.Y.Z`   | Build image, tag with version + SHA, deploy to Production (manual approval) | Production  |

**Key features:**

* Docker images are tagged with the **short commit SHA**; release builds also include the **semantic version**.
* Application UI displays **"Pre-release"** for non-release builds and the release version for tagged releases.
* Production deployments require **manual approval** via GitHub Environments.

---

## Local Development

### Option 1: Run with Python (no Docker)

Create and activate a virtual environment, then install runtime dependencies:

```bash
python3 -m venv venv
source venv/bin/activate       # Linux/macOS
# venv\Scripts\activate       # Windows PowerShell

pip install --upgrade pip
pip install -r requirements.txt

python app.py
# Open http://localhost:8000
```

### Option 2: Run with Docker

```bash
docker build -t mortcal .
docker run -p 8000:8000 mortcal
# Open http://localhost:8000
```

**Notes:**

* Python version: **3.12**
* Flask listens on port **8000**

---

## Testing

Unit tests are written using **pytest** and cover both business logic and Flask routes.

```bash
pytest
```

* Tests are located in the `tests/` directory
* Tests are excluded from Bandit security scans via pre-commit configuration

---

## Code Quality & Security

Quality and security checks are enforced locally and in CI using **pre-commit**.

Included tools:

* **Black** – Code formatting
* **Flake8 / Ruff** – Linting
* **MyPy** – Static type checking
* **Bandit** – Python security scanning (runtime code only)
* **Gitleaks** – Secrets detection

All checks run automatically in GitHub Actions on pull requests and pushes to `main`.

---

## Infrastructure as Code (Terraform)

All Azure infrastructure is defined in the `infra/` directory using Terraform.

* Separate variable files per environment:

  * `stg.tfvars` – Staging
  * `prod.tfvars` – Production

Provisioned resources include:

* Azure Container Apps Environments
* Azure Container Apps (Staging & Production)
* Azure Log Analytics Workspaces

Example usage:

```bash
cd infra
terraform init
terraform plan -var-file=stg.tfvars
terraform apply -var-file=stg.tfvars
```

---

## Configuration

### Environment Variables

| Variable      | Description                                                        |
| ------------- | ------------------------------------------------------------------ |
| `APP_VERSION` | Application version displayed in the UI (`Pre-release` by default) |

This variable is injected during deployment via GitHub Actions.

---

## Tech Stack

### Application & Runtime

* **Python 3.12**
* **Flask** – Web framework
* **Matplotlib** – Visualization of amortization schedules

### Containerization & Hosting

* **Docker** – Containerization
* **Docker Hub** – Image registry
* **Azure Container Apps** – Serverless container hosting

### CI/CD & Release Management

* **GitHub Actions** – CI/CD pipelines
* **GitHub Releases** – Semantic versioning and production promotion

### Observability

* **Azure Log Analytics** – Centralized logging and diagnostics

---

## Portfolio & Contact

* **GitHub:** [https://github.com/DaneJ081](https://github.com/DaneJ081)
* **Project Repo:** DevOpsMortCal

This project is designed to showcase real-world DevOps workflows, tooling, and best practices.
