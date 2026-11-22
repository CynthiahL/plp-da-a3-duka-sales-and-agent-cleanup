# plp-da-a3-duka-sales-and-agent-cleanup
# Week 3 Analytics Deliverables: Duka Electronics & Mobile Money Agent Network

## Project Overview
This repository contains two client analytics deliverables built for a Nairobi analytics consultancy:
1. **Duka Electronics (Half-Year Sales Exploration):** Exploratory data analysis of 1,000 retail orders (Jan–Jun 2026) across five Kenyan branches, identifying top-performing locations, product mix dynamics, weekend shopping trends, and spreadsheet reconciliation.
2. **Mobile Money Agent Network (Data Quality Audit & Cleanup):** An automated, reusable Python cleaning pipeline (`cleaning_pipeline.py`) that audits, cleans, flags anomalies, and merges 612 raw legacy transactions with the master agent register.

## How to Regenerate Data & Run Notebooks
1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Regenerate raw datasets (`duka_sales.csv`, `agents.csv`, `agent_transactions.csv`):**
   ```bash
   python generate_data.py
   ```
3. **Run notebooks from top to bottom:**
   * Open `duka_sales_exploration.ipynb` and run all cells to generate `outputs/premium_online_coast_capital.csv` and verify totals against `excel/duka_branch_summary.xlsx`.
   * Open `agent_cleanup.ipynb` and run all cells to execute `clean_agent_data()` and generate `outputs/agent_transactions_clean.csv`.

## Duka Electronics — Executive Summary
* Duka Electronics generated a total half-year revenue of **KES 71,792,500** across **1,000 orders** between January 1 and June 29, 2026.
* **Nairobi** led all branches in both revenue (**KES 26,106,100**, or 36.4% of total sales) and order volume (**376 orders**), followed by **Mombasa** (**KES 14,003,700** across 186 orders).
* **Laptops** generated the highest revenue at **KES 41,535,000** (639 units sold), whereas **Tablets** led total unit volume with **691 units** sold (**KES 19,348,000**).
* Peak monthly revenue occurred in **April 2026** (**KES 13,518,300**), outperforming the lowest month, **June 2026** (**KES 10,903,400**), by **23.98%**.
* High-value **Premium Online orders** from Nairobi and Mombasa accounted for **83 orders** generating **KES 10,218,000** in revenue.

## Mobile Money Agent Data — Row Count Validation
* **Before Cleaning (`agent_transactions.csv`):** `612 rows`
* **Duplicates Removed (`txn_id`):** `12 rows`
* **After Cleaning & Left Merge (`outputs/agent_transactions_clean.csv`):** `600 unique rows` (including `20` median-imputed amount records, `53` IQR-flagged outlier records, and `7` transactions mapped to `Unknown` county for unregistered agent `AG099`).
