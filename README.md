# Nairobi Analytics Consultancy — Week 3 Client Deliverables

This repository contains the completed analysis and data-cleaning deliverables for two client engagements:
1. **Engagement 1 · Duka Electronics:** Half-year (January–June 2026) sales exploration, branch/product benchmarking, Excel reporting, and executive summary.
2. **Engagement 2 · Mobile Money Agent Network:** Data-quality audit, reusable Python cleaning pipeline (`cleaning_pipeline.py`), agent master register merge, summary reporting, and KDPA 2019 privacy review.

---

## Repository Structure

```text
├── README.md
├── requirements.txt
├── generate_data.py
├── cleaning_pipeline.py
├── duka_sales_exploration.ipynb
├── agent_cleanup.ipynb
├── excel/
│   └── duka_branch_summary.xlsx
└── outputs/
    ├── premium_online_coast_capital.csv
    └── agent_transactions_clean.csv
```

---

## How to Regenerate Data & Run the Notebooks

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Regenerate raw datasets** (excluded from Git per submission guidelines):
   ```bash
   python generate_data.py
   ```
   This creates `duka_sales.csv` (seed `2026`), `agents.csv` (seed `44`), and `agent_transactions.csv` (seed `44`).
3. **Execute notebooks top-to-bottom:**
   * Run `duka_sales_exploration.ipynb` to produce `outputs/premium_online_coast_capital.csv` and validate `excel/duka_branch_summary.xlsx`.
   * Run `agent_cleanup.ipynb` to execute `clean_agent_data()` from `cleaning_pipeline.py` and export `outputs/agent_transactions_clean.csv`.

[Duka Sales Exploration in Colab](https://colab.research.google.com/github/CynthiahL/plp-da-a3-duka-sales-and-agent-cleanup/blob/main/duka_sales_exploration.ipynb)

[Agent Cleanup in Collab](https://colab.research.google.com/github/CynthiahL/plp-da-a3-duka-sales-and-agent-cleanup/blob/main/agent_cleanup.ipynb)


---

## Engagement 1 · Duka Electronics — Executive Summary

* Duka Electronics generated **KES 71,792,500** in total revenue across **1,000 orders** during H1 2026 (January–June).
* **Nairobi** led all five branches in revenue and order volume, though branch revenue rankings diverged from order-count rankings due to differences in high-ticket Laptop and Tablet sales mix.
* **Laptops** (KES 65,000 unit price) generated the highest total revenue, whereas lower-priced accessories (**Chargers** at KES 1,200 and **Headphones** at KES 2,500) drove the highest unit volumes.
* Monthly revenue varied significantly between our peak month and lowest-performing month, highlighting clear seasonal/monthly demand swings across H1 2026.
* High-value **Premium online orders** (unit price ≥ KES 28,000) from **Nairobi and Mombasa** were isolated and exported to `outputs/premium_online_coast_capital.csv` for targeted retention campaigns.

*(Note: Replace any placeholder wording above with your exact branch, product, month, and filtered totals from `duka_sales_exploration.ipynb` so every bullet contains a specific number.)*

---

## Engagement 2 · Mobile Money Agent Network — Row Count Summary

| Stage | Row Count | Notes |
| :--- | :--- | :--- |
| **Raw `agent_transactions.csv`** | **612** | Includes 12 duplicate `txn_id` records, 22 missing/`N/A` amounts, 5 slash-formatted dates, 5 `KES 250,000` spikes, and 8 `AG099` references |
| **After Deduplication (`txn_id`)** | **600** | Removed 12 duplicate `txn_id` rows (`keep="first"`) |
| **Final Cleaned & Merged (`agent_transactions_clean.csv`)** | **600** | All 600 valid transactions preserved via left join (`20` missing amounts median-imputed at `KES 1,776.50`; `53` IQR outliers flagged; `7` `AG099` rows labeled `Unknown`) |
