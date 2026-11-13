
def calculate_revenue(df):

    # Revenue for each valid order
    df["Revenue"] = df["Quantity"] * df["UnitPrice"]

    # Total product cost
    df["TotalCost"] = df["Quantity"] * df["UnitCost"]

    # Estimated gross profit
    df["GrossProfit"] = (
        df["Quantity"] *
        (df["UnitPrice"] - df["UnitCost"])
    )

    # Calculate overall metrics
    total_revenue = df["Revenue"].sum()

    total_orders = len(df)

    total_quantity = df["Quantity"].sum()

    total_profit = df["GrossProfit"].sum()

    # Prevent division by zero
    if total_orders > 0:
        aov = total_revenue / total_orders
    else:
        aov = None

    metrics = {
        "Total Revenue": total_revenue,
        "Total Valid Orders": total_orders,
        "Average Order Value": aov,
        "Total Quantity Sold": total_quantity,
        "Estimated Gross Profit": total_profit
    }

    return df, metrics
