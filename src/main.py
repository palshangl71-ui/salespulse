
import os

from validation import validate_data
from revenue import calculate_revenue
from product_analysis import analyze_products
from region_analysis import analyze_regions


def main():

    print("\n" + "=" * 55)
    print("          SALESPULSE RETAIL ANALYTICS")
    print("=" * 55)

    # STEP 1: DATA VALIDATION

    df, invalid, issue_counts, original_count = validate_data()

    # STEP 2: REVENUE CALCULATIONS

    df, metrics = calculate_revenue(df)

    # Save the enriched valid dataset
    df.to_csv("data/cleaned_sales.csv", index=False)

    # STEP 3: PRODUCT ANALYSIS

    (
        product_revenue,
        top_five,
        product_quantity,
        highest_quantity_product
    ) = analyze_products(df)

    # STEP 4: REGIONAL ANALYSIS

    region_data, best_region = analyze_regions(df)

    # STEP 5: ADDITIONAL ANALYSIS

    loss_orders = int((df["UnitCost"] > df["UnitPrice"]).sum())

    zero_cost_orders = int((df["UnitCost"] == 0).sum())

    # STEP 6: CREATE FINAL REPORT

    report = []

    report.append("SALESPULSE - RETAIL SALES ANALYTICS REPORT")
    report.append("=" * 55)

    # Data quality summary

    report.append("\n1. DATA QUALITY SUMMARY")

    report.append(f"Original records: {original_count}")
    report.append(f"Valid records: {len(df)}")
    report.append(f"Invalid records: {len(invalid)}")

    report.append("\nIssue-wise breakdown:")

    for issue, count in issue_counts.items():
        report.append(f"{issue}: {count}")

    report.append(
        "\nNote: Issue counts can overlap when one record has "
        "multiple validation problems."
    )

    # Overall metrics

    report.append("\n2. OVERALL SALES METRICS")

    for key, value in metrics.items():

        if value is None:
            report.append(f"{key}: N/A")

        else:
            report.append(f"{key}: Rs. {value:,.2f}")

    report.append(f"Loss-making orders retained: {loss_orders}")

    report.append(f"Orders with zero UnitCost retained: {zero_cost_orders}")

    # Product analysis

    report.append("\n3. TOP FIVE PRODUCTS BY REVENUE")

    if not top_five.empty:
        report.append(top_five.to_string())

    else:
        report.append("No valid product data.")

    report.append("\n4. HIGHEST QUANTITY SOLD")

    if highest_quantity_product is not None:

        report.append(
            f"{highest_quantity_product}: "
            f"{product_quantity[highest_quantity_product]} units"
        )

    else:
        report.append("No valid product data.")

    # Regional analysis

    report.append("\n5. REGION-WISE SALES PERFORMANCE")

    report.append(region_data.to_string())

    if best_region is not None:
        report.append(f"\nHighest revenue region: {best_region}")

    # Business insights

    report.append("\n6. BUSINESS INSIGHTS")

    if not product_revenue.empty:

        top_product = product_revenue.idxmax()

        report.append(
            f"1. {top_product} is the highest revenue-generating "
            f"product, contributing Rs. "
            f"{product_revenue.max():,.2f}."
        )

    if highest_quantity_product is not None:

        report.append(
            f"2. {highest_quantity_product} has the highest "
            f"sales volume with "
            f"{product_quantity[highest_quantity_product]} units."
        )

    if best_region is not None:

        report.append(
            f"3. {best_region} is the strongest region in terms "
            f"of revenue, generating Rs. "
            f"{region_data.loc[best_region, 'TotalRevenue']:,.2f}."
        )

    if not region_data.empty:

        best_profit_region = (
            region_data["EstimatedGrossProfit"].idxmax()
        )

        report.append(
            f"4. {best_profit_region} generates the highest "
            f"estimated regional gross profit."
        )

    # Recommendations

    report.append("\n7. RECOMMENDATIONS")

    if not product_revenue.empty:

        report.append(
            f"1. Maintain adequate inventory of {top_product}, "
            "which contributes the highest product revenue."
        )

    if not region_data.empty:

        lowest_region = region_data["TotalRevenue"].idxmin()

        report.append(
            f"2. Investigate the reasons for lower sales in "
            f"{lowest_region} and introduce targeted promotions "
            "and regional sales strategies."
        )

    # STEP 7: DISPLAY REPORT

    final_report = "\n".join(report)

    print("\n")
    print(final_report)

    # STEP 8: SAVE REPORT

    os.makedirs("reports", exist_ok=True)

    with open(
        "reports/sales_report.txt",
        "w",
        encoding="utf-8"
    ) as file:

        file.write(final_report)

    print("\n" + "=" * 55)
    print("REPORT GENERATED SUCCESSFULLY!")
    print("Location: reports/sales_report.txt")
    print("=" * 55)


if __name__ == "__main__":

    main()
