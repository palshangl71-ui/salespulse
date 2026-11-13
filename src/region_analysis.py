
def analyze_regions(df):

    # Calculate revenue and profit for each region
    region_data = (
        df.groupby("Region")
        .agg(
            TotalRevenue=("Revenue", "sum"),
            EstimatedGrossProfit=("GrossProfit", "sum")
        )
        .sort_values(
            "TotalRevenue",
            ascending=False
        )
    )

    if not region_data.empty:

        best_region = region_data["TotalRevenue"].idxmax()

    else:

        best_region = None

    return region_data, best_region
