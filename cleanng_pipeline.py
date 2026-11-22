import pandas as pd
import numpy as np


def clean_agent_data(txns: pd.DataFrame, agents: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """
    Audits, cleans, flags, and merges mobile-money agent transaction data.

    Parameters
    ----------
    txns : pd.DataFrame
        Raw transaction extract DataFrame (agent_transactions.csv).
    agents : pd.DataFrame
        Agent master register DataFrame (agents.csv).

    Returns
    -------
    tuple[pd.DataFrame, dict]
        A tuple containing the cleaned, merged DataFrame and a dictionary
        logging row counts and cleaning actions at each stage.
    """
    df = txns.copy()
    log = {"initial_rows": len(df)}

    # 1. Uniqueness: remove duplicate txn_id rows, keeping first original record
    dup_count = int(df.duplicated(subset=["txn_id"]).sum())
    df = df.drop_duplicates(subset=["txn_id"], keep="first").copy()
    log["duplicates_removed"] = dup_count

    # 2. Consistency: standardise txn_type to 'Deposit' and 'Withdrawal'
    df["txn_type"] = df["txn_type"].astype("string").str.strip().str.title()
    invalid_type_mask = df["txn_type"].isna() | (~df["txn_type"].isin(["Deposit", "Withdrawal"]))
    log["invalid_txn_types"] = int(invalid_type_mask.sum())

    # 3. Validity & types: normalise date delimiters and convert amount/txn_date
    df["txn_date"] = pd.to_datetime(
        df["txn_date"].astype("string").str.replace("/", "-", regex=False),
        format="%Y-%m-%d",
        errors="coerce",
    )
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    # 4. Completeness: flag missing amounts and impute with median
    df["amount_imputed"] = df["amount"].isna()
    log["amounts_imputed"] = int(df["amount_imputed"].sum())
    median_amt = float(df["amount"].median())
    df["amount"] = df["amount"].fillna(median_amt)
    log["imputation_median_kes"] = median_amt

    # 5. Outliers: IQR method (Q3 + 1.5 * IQR) to flag suspicious amounts
    q1 = df["amount"].quantile(0.25)
    q3 = df["amount"].quantile(0.75)
    iqr = q3 - q1
    lower_fence = max(0.0, q1 - 1.5 * iqr)
    upper_fence = q3 + 1.5 * iqr
    df["is_outlier"] = (df["amount"] < lower_fence) | (df["amount"] > upper_fence)
    log["iqr_upper_fence"] = round(float(upper_fence), 2)
    log["outliers_flagged"] = int(df["is_outlier"].sum())

    # 6. Merge: left join onto agent register and label unknown agents
    clean_df = df.merge(agents, on="agent_id", how="left")
    log["unknown_agent_txns"] = int(clean_df["county"].isna().sum())
    clean_df["county"] = clean_df["county"].fillna("Unknown")

    log["final_rows"] = len(clean_df)
    return clean_df, log
