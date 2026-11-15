# GMP Deviation & CAPA Tracker

A quality management system for logging production deviations and generating audit-ready CAPA reports, built for UK medical cannabis manufacturing workflows.

## Problem Statement

MHRA GMP inspections turn on documentation discipline. When a deviation occurs on a production floor, teams need to log containment actions immediately, drive root cause analysis, and produce a formatted report before the next shift begins. Existing QMS platforms are expensive and slow to deploy for small licensed operators.

## Features

- **Structured deviation intake** — batch reference, severity classification (Critical / Major / Minor), containment action
- **CAPA workflow** — separate corrective and preventive action fields, mapped to EU GMP Annex 15 expectations
- **Root cause capture** — 5 Whys field structured for investigator review
- **PDF report generation** — one-click export formatted for QA sign-off and inspector submission
- **Role-based access control** — session-based authentication enforcing data integrity requirements
- **Persistent storage** — SQLite, zero-infrastructure, portable

## Tech Stack

Python · Streamlit · ReportLab · SQLite

## Getting Started

```bash
pip install -r requirements.txt
streamlit run app.py
