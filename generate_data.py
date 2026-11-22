import numpy as np
import pandas as pd


def generate_duka_sales(seed: int = 2026) -> pd.DataFrame:
    """Generates the 1,000-row Duka Electronics H1 2026 sales dataset."""
    rng = np.random.default_rng(seed)
    n = 1000
    branches = ["Nairobi", "Mombasa", "Nakuru", "Kisumu", "Eldoret"]
    branch_weights = [0.35, 0.22, 0.18, 0.15, 0.10]
    products = {
        "Laptop": 65000,
        "Tablet": 28000,
        "Phone": 15000,
        "Headphones": 2500,
        "Charger": 1200,
    }
    product_names = list(products.keys())
    channels = ["In-store", "Online", "Phone order"]
    channel_weights = [0.55, 0.32, 0.13]

    chosen_products = rng.choice(product_names, size=n)
    order_dates = pd.to_datetime("2026-01-01") + pd.to_timedelta(
        rng.integers(0, 180, size=n), unit="D"
    )

    duka = pd.DataFrame({
        "order_id": np.arange(1001, 1001 + n),
        "order_date": order_dates.strftime("%Y-%m-%d"),
        "branch": rng.choice(branches, size=n, p=branch_weights),
        "product": chosen_products,
        "quantity": rng.integers(1, 6, size=n),
        "channel": rng.choice(channels, size=n, p=channel_weights),
        "unit_price": [products[p] for p in chosen_products],
    })
    duka.to_csv("duka_sales.csv", index=False)
    return duka


def generate_agent_network(seed: int = 44) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Generates agents.csv and agent_transactions.csv with deliberate data quality issues."""
    rng = np.random.default_rng(seed)
    n = 600
    agents = pd.DataFrame({
        "agent_id": [f"AG{i:03d}" for i in range(1, 21)],
        "county": rng.choice(["Nairobi", "Kiambu", "Nakuru", "Mombasa", "Kisumu"], 20),
        "onboarded": pd.date_range("2024-01-01", periods=20, freq="MS").strftime("%Y-%m-%d"),
    })
    txns = pd.DataFrame({
        "txn_id": [f"TX{i:05d}" for i in range(1, n + 1)],
        "agent_id": rng.choice(agents["agent_id"], n),
        "txn_type": rng.choice(
            ["Deposit", "withdrawal", "DEPOSIT ", "Withdrawal", "deposit"], n
        ),
        "amount": rng.lognormal(7.5, 0.8, n).round(0).astype(str),
        "txn_date": (
            pd.to_datetime("2026-03-01")
            + pd.to_timedelta(rng.integers(0, 60, n), unit="D")
        ).strftime("%Y-%m-%d"),
    })
    idx = rng.choice(n, 30, replace=False)
    txns.loc[idx[:15], "amount"] = np.nan
    txns.loc[idx[15:20], "amount"] = "N/A"
    txns.loc[idx[20:25], "amount"] = "250000"
    txns.loc[idx[25:], "txn_date"] = txns.loc[idx[25:], "txn_date"].str.replace("-", "/")
    txns = pd.concat([txns, txns.sample(12, random_state=1)], ignore_index=True)
    txns.loc[rng.choice(len(txns), 8, replace=False), "agent_id"] = "AG099"

    agents.to_csv("agents.csv", index=False)
    txns.to_csv("agent_transactions.csv", index=False)
    return agents, txns


if __name__ == "__main__":
    generate_duka_sales()
    generate_agent_network()
    print("Generated duka_sales.csv, agents.csv, and agent_transactions.csv")
