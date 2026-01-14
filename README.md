# DevOpsMortCal – Mortgage Calculator with DevOps Pipeline

![Project Badge](https://img.shields.io/badge/DevOps-Portfolio-green)

## Project Overview
**DevOpsMortCal** is a Python-based mortgage calculator web application that calculates, monthly mortgage payments, loan amortization schedules and visually compares payoff scenarios based on different monthly payment amounts. Users can see how different payment strategies affect interest paid and total loan duration.  

This project is also a **DevOps portfolio demonstration**, showcasing:

- End-to-end **CI/CD pipelines** with GitHub Actions
- **Containerization** with Docker
- **Infrastructure as Code** with Terraform
- **Multi-environment cloud deployment** on Azure Container Apps
- **Observability** via Azure Log Analytics
- **Code quality & security enforcement** with pre-commit hooks and unit tests

---

## Architecture Overview

```
GitHub Repo
     │
     ├─> GitHub Actions (CI/CD)
             │
             ├─> DockerHub
                     │
                     ├─> Azure Container Apps (Staging / Prod)
                             │
                             └─> Logs → Azure Log Analytics
```

- **Source Code:** GitHub
- **Container Images:** DockerHub
- **Hosting Environments:** Staging, Production (Azure Container Apps)
- **Observability:** Log Analytics for logs & metrics
- **CI/CD:** GitHub Actions with PR-based merges, automated builds, and deployments

---

## CI/CD Pipeline Overview

| Branch / Action       | Trigger            | Pipeline Steps                                      | Environment      |
|-----------------------|------------------|---------------------------------------------------|----------------|
| Feature → Dev         | Pull Request      | Run pre-commit, unit tests, build container| None       |
| Merge → Main          | Pull Request      | Run pre-commit, unit tests, build container, push | Staging ACA    |
| GitHub Release        | Tag vX.Y.Z        | Build container, push prod image, deploy         | Production ACA |

**Key features:**
- Pre-commit hooks enforce code quality and security
- Merges to `main` require passing checks and PR approvals
- Manual approval gate before Production deployment
- Semantic version tagging for releases

---

## Local Development

### Python (without Docker)
```bash
pip install -r requirements.txt
python app.py
# Open http://localhost:8000
```

### Docker
```bash
docker build -t mortcal .
docker run -dp 8000:80 mortcal
# Open http://localhost:8000
```

**Notes:**
- Python version: 3.12
- Flask default port: 8000

---

## Infrastructure as Code (Terraform)

- Terraform defines all cloud resources in the `infra/` folder
- Separate `.tfvars` files for **staging** (`stg.tfvars`) and **production** (`prod.tfvars`)
- Managed resources:
  - Container Apps Environments
  - Azure Container Apps (Dev, Staging, Prod)
  - Log Analytics Workspaces
- Example commands:
```bash
cd infra
terraform init
terraform plan -var-file=stg.tfvars
terraform apply -var-file=stg.tfvars
```

---

## Observability & Logging

- Azure Container Apps logs are streamed to **Azure Log Analytics**
- Basic health check endpoint: `/health`
- Optional: Alerts can be configured for errors or failures
- Query example in Log Analytics:
```kusto
ContainerAppConsoleLogs_CL
| where TimeGenerated > ago(1h)
| order by TimeGenerated desc
```

---

## Code Quality & Security

- **Pre-commit hooks**:
  - Python formatting: Black
  - Linting: Flake8
  - Security checks: Bandit
- CI runs all pre-commit checks on pull requests
- Branch protections enforce merge-only updates for `main`

---

## Tech Stack

### Application & Runtime
- **Python 3.12**
- **Flask** – Web application framework
- **Matplotlib** – Amortization and payoff visualizations

### Containerization & Hosting
- **Docker** – Application containerization
- **Docker Hub** – Image registry
- **Azure Container Apps** – Serverless container hosting (Dev / Staging / Prod)

### Infrastructure as Code
- **Terraform** – Provisioning Azure resources (ACR, ACA, Log Analytics)

### CI/CD & Release Management
- **GitHub Actions** – Build, test, security scanning, and deployments
- **GitHub Releases** – Semantic versioning and production promotion

### Testing, Quality & Security
- **Pytest** – Unit testing
- **Ruff** – Fast Python linting
- **Black** – Code formatting
- **MyPy** – Static type checking
- **Bandit** – Python security scanning
- **Gitleaks** – Secrets detection

### Observability
- **Azure Log Analytics** – Centralized logging and monitoring

---

## Contact / Portfolio

- GitHub: [https://github.com/DaneJ081](https://github.com/DaneJ081)
