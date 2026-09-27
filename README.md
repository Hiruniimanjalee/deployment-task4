# Deployment Task 4: Docker Applications

This repository contains my work for SWE40006 Software Deployment and Evolution, Deployment Task 4. It includes three Python applications developed for the Credit, Distinction and High Distinction levels.

## Projects

| Folder | Level | Description |
|---|---|---|
| `credit-web` | Credit | A basic Flask web application running in Docker. |
| `distinction-web` | Distinction | A Milestone Progress Tracker web application with an optimized Dockerfile. |
| `hd-cli` | High Distinction | A non-web Python application that reads a CSV file and writes a progress summary. |

## Requirements

- Docker installed and running
- A terminal such as PowerShell

Run the following commands from the repository's main folder.

## Credit: Basic Flask application

```powershell
docker build -t task4-credit:1.0 ./credit-web
docker run --rm -p 8080:5000 task4-credit:1.0
```

Open `http://localhost:8080` in a browser. The application also has a health endpoint at `http://localhost:8080/health`.

## Distinction: Milestone Progress Tracker

```powershell
docker build -t milestone-tracker:1.0 ./distinction-web
docker run --rm -p 8082:5000 -e APP_TITLE="Milestone Progress Tracker" -e DAILY_TARGET=3 milestone-tracker:1.0
```

Open `http://localhost:8082` to use the tracker. It calculates completed milestones, progress percentage, remaining milestones and estimated days based on the daily target.

## High Distinction: Non-web CLI application

The `hd-cli/data/tasks.csv` file provides sample task data. The application reads this file and saves its results to `hd-cli/data/summary.txt`.

In PowerShell, run:

```powershell
docker build -t milestone-cli:1.0 ./hd-cli
docker run --rm --network none --read-only -v "${PWD}/hd-cli/data:/data" milestone-cli:1.0
```

After the container finishes, open `hd-cli/data/summary.txt` to view the generated summary. The mounted folder keeps the output available on the host computer after the container is removed. The CLI image runs as a non-root user and does not require network access.

## Author

Hiruni Imanjalee
