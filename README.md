# Project Overview:
This application uses Flask and Matplotlib to calculate loan amortization schedules and visually compare payoff scenarios based on different monthly payment amounts. It highlights differences in interest paid and total loan duration.

## Architecture Overview
Source Code stored in GitHub
Container Images stored in Azure Container Registry (ACR)
Hosting via Azure Container Apps (ACA) for Dev, Staging, and Production environments
CI/CD Pipeline implemented using GitHub Actions

## Pipeline Overview:
1. Create a feature branch
   Submit a pull request to Dev
2. Merge into Dev triggers:
    Build the container image
    Tag & push image as dev
    Deploy image to Dev ACA environment
3. Merge into main triggers:
    Build the staging container image
    Tag & push the image as staging
    Deploy to Staging ACA environment
4. Creating a GitHub release triggers:
    Tag image as prod & semantic version ( vX.Y.Z )
    Deploy to Production ACA environment

## Local Development
Validate that the application code runs locally

pip install -r requirements.txt
python app.py
Then open http://localhost:8000

Validate the container builds and runs

docker build -t mortcal .
docker run -dp 8000:80 mortcal
then open http://localhost:8000

## Tech Stack
Python
Flask
Matplotlib
Docker
DockerHub
Azure Container Apps
GitHub Actions
