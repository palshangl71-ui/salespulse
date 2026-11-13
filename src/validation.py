
import pandas as pd
import os


def validate_data():

    # Read the original dataset
    file_path = "data/sales.csv"

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            "sales.csv not found inside the data folder."
        )

    df = pd.read_csv(file_path)

    original_count = len(df)

    # Check required columns
    required_columns = [
        "OrderID",
        "ProductName",
        "Region",
        "Quantity",
        "UnitPrice",
        "UnitCost"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # Clean spaces from text columns
    for col in ["OrderID", "ProductName", "Region"]:
        df[col] = df[col].astype("string").str.strip()
        df[col] = df[col].replace("", pd.NA)

    # Convert numerical columns safely
    for col in ["Quantity", "UnitPrice", "UnitCost"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Identify duplicate Order IDs.
    # Keep the first occurrence and flag later occurrences.
    duplicate_ids = (
        df["OrderID"].notna()
        & df["OrderID"].duplicated(keep="first")
    )

    reasons = []

    # Check every record
    for index, row in df.iterrows():

        issues = []

        if pd.isna(row["OrderID"]):
            issues.append("Missing Order ID")

        if pd.isna(row["Quantity"]) or row["Quantity"] <= 0:
            issues.append("Zero or negative quantity")

        if pd.isna(row["UnitPrice"]) or row["UnitPrice"] <= 0:
            issues.append("Zero or negative UnitPrice")

        if pd.isna(row["UnitCost"]) or row["UnitCost"] < 0:
            issues.append("Negative or missing UnitCost")

        if pd.isna(row["ProductName"]):
            issues.append("Missing ProductName")

        if pd.isna(row["Region"]):
            issues.append("Missing Region")

        if duplicate_ids.loc[index]:
            issues.append("Duplicate Order ID")

        reasons.append("; ".join(issues))

    # Add reasons to original data
    df["InvalidReason"] = reasons

    # Separate records
    invalid = df[df["InvalidReason"] != ""].copy()
    valid = df[df["InvalidReason"] == ""].copy()

    # Save output files
    os.makedirs("data", exist_ok=True)

    valid.to_csv("data/cleaned_sales.csv", index=False)

    invalid.to_csv("data/invalid_records.csv", index=False)

    # Count each type of issue
    issue_counts = {}

    for reason in [
        "Missing Order ID",
        "Zero or negative quantity",
        "Zero or negative UnitPrice",
        "Negative or missing UnitCost",
        "Missing ProductName",
        "Missing Region",
        "Duplicate Order ID"
    ]:

        issue_counts[reason] = int(
            invalid["InvalidReason"]
            .str.contains(reason, regex=False)
            .sum()
        )

    # Print summary
    print("\n========== DATA VALIDATION ==========")

    print("Original records:", original_count)
    print("Valid records:", len(valid))
    print("Invalid records:", len(invalid))

    print("\nIssue-wise summary:")

    for issue, count in issue_counts.items():
        print(f"{issue}: {count}")

    print("\nCleaned and invalid datasets saved.")

    return valid, invalid, issue_counts, original_count
