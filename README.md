![Status](https://img.shields.io/badge/Status-Active-brightgreen) ![License](https://img.shields.io/badge/License-MIT-yellow.svg) ![Python](https://img.shields.io/badge/Python-3.9+-blue)

# GMP Deviation & CAPA Tracker

A quality management system for logging production deviations and generating audit-ready CAPA reports, built for UK pharmaceutical manufacturing workflows.

## Problem Statement

MHRA GMP inspections turn on documentation discipline. When a deviation occurs on a production floor, teams need to log containment actions immediately, drive root cause analysis, and produce a formatted report before the next shift begins. Existing QMS platforms are expensive and slow to deploy for small licensed operators.

## Features

- **Structured deviation intake** — batch reference, severity classification (Critical / Major / Minor), containment action
- **CAPA workflow** — separate corrective and preventive action fields, mapped to EU GMP Annex 15 expectations
- **Root cause capture** — 5 Whys field structured for investigator review
- **PDF report generation** — one-click export formatted for QA sign-off and inspector submission
- **Role-based access control** — session-based authentication enforcing data integrity requirements
- **Persistent storage** — SQLite, zero-infrastructure, portable

## Screenshots

| Login Screen | PDF Report |
| :--- | :--- |
| ![Login](screenshots/login.png) | ![Report](screenshots/pdf-sample.png) |

## Tech Stack

Python · Streamlit · ReportLab · SQLite

## Getting Started

    pip install -r requirements.txt
    streamlit run app.py

Default credentials: `admin` / `password`

> Credentials are stored in plaintext for demonstration purposes only. Production deployments must hash credentials and enforce account lockout per 21 CFR Part 11.

## Applicable Guidance

- MHRA 'The Rules and Guidance Governing Medical Cannabis Licences'
- EU GMP Annex 15 (Qualification and Validation)
- ICH Q10 (Pharmaceutical Quality System)
- 21 CFR Part 11 (Electronic Records; Electronic Signatures)

## Disclaimer

This is a demonstration project. It does not constitute validated software and must not be used for actual GMP compliance without formal IQ/OQ/PQ qualification per Annex 15.
