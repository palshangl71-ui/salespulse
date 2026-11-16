import pandas as pd
from pathlib import Path
# --------------------------------
# 1. LOAD THE EXCEL DATASET
# --------------------------------

BASE_DIR = Path(__file__).resolve().parent

FILE_PATH = BASE_DIR / "data" / "SalesPulse_Week2_Day1_Relational_Dataset.xlsx"

tables = pd.read_excel(FILE_PATH, sheet_name=None)

# Store all observations
report = []

def add_report(message):
    report.append(message)
    print(message)


add_report("====================================")
add_report(" SALESPULSE DATA QUALITY REPORT")
add_report("====================================")
# --------------------------------
# 2. CHECK TABLE STRUCTURE
# --------------------------------

add_report("\n1. TABLE STRUCTURE")

for name, df in tables.items():

    add_report(f"\nTable Name: {name}")
    add_report(f"Number of Rows: {len(df)}")
    add_report(f"Number of Columns: {len(df.columns)}")

    add_report(f"Columns: {list(df.columns)}")
# --------------------------------
# 3. CHECK MISSING VALUES
# --------------------------------

add_report("\n2. MISSING VALUE CHECKING")

for name, df in tables.items():

    # Treat empty spaces as missing values
    clean_df = df.replace(r"^\s*$", pd.NA, regex=True)

    missing = clean_df.isnull().sum()

    if missing.sum() == 0:
        add_report(f"{name}: No missing values")

    else:
        for column, count in missing.items():

            if count > 0:
                add_report(
                    f"{name} - {column}: "
                    f"{count} missing value(s)"
                )
# --------------------------------
# 4. CHECK DUPLICATE RECORDS
# --------------------------------

add_report("\n3. DUPLICATE CHECKING")

primary_keys = {
    "Customers": "CustomerID",
    "Products": "ProductID",
    "Orders": "OrderID",
    "OrderItems": "OrderItemID"
}

for name, df in tables.items():

    duplicate_rows = df.duplicated().sum()

    add_report(
        f"{name}: {duplicate_rows} duplicate complete rows"
    )

    key = primary_keys[name]

    duplicate_ids = df[key].duplicated().sum()

    add_report(
        f"{name} - {key}: {duplicate_ids} duplicate ID values"
    )
# --------------------------------
# 5. CHECK NUMERICAL VALUES
# --------------------------------

add_report("\n4. NUMERICAL VALUE CHECKING")

products = tables["Products"]
items = tables["OrderItems"]

# Check product selling price
add_report(
    "Invalid UnitPrice values: "
    + str((products["UnitPrice"] <= 0).sum())
)

# Check product cost
add_report(
    "Invalid UnitCost values: "
    + str((products["UnitCost"] <= 0).sum())
)

# Check order quantity
add_report(
    "Invalid Quantity values: "
    + str((items["Quantity"] <= 0).sum())
)

# Check unusual cost and selling price
add_report(
    "Products where UnitCost exceeds UnitPrice: "
    + str((products["UnitCost"] > products["UnitPrice"]).sum())
)
# --------------------------------
# 6. CHECK DATE VALUES
# --------------------------------

add_report("\n5. DATE VALIDATION")

orders = tables["Orders"]

valid_dates = pd.to_datetime(
    orders["OrderDate"],
    errors="coerce"
)

invalid_dates = valid_dates.isna().sum()

add_report(
    f"Invalid OrderDate values: {invalid_dates}"
)
# --------------------------------
# 7. CHECK TABLE RELATIONSHIPS
# --------------------------------

add_report("\n6. FOREIGN KEY CHECKING")

customers = tables["Customers"]
products = tables["Products"]

relationships = {

    "Orders -> Customers": (
        orders["CustomerID"],
        customers["CustomerID"]
    ),

    "OrderItems -> Orders": (
        items["OrderID"],
        orders["OrderID"]
    ),

    "OrderItems -> Products": (
        items["ProductID"],
        products["ProductID"]
    )
}

for name, (child, parent) in relationships.items():

    invalid = (~child.isin(parent)).sum()

    add_report(
        f"{name}: {invalid} invalid reference(s)"
    )
# --------------------------------
# 8. SAVE THE FINAL REPORT
# --------------------------------

report_file = BASE_DIR / "data_quality_report.txt"

report_file.write_text(
    "\n".join(report),
    encoding="utf-8"
)

print("\n====================================")
print("DATA QUALITY CHECKING COMPLETED!")
print("====================================")

print(f"Report saved at: {report_file}")