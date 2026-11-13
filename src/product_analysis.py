
def analyze_products(df):

    # Calculate revenue by product
    product_revenue = (
        df.groupby("ProductName")["Revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    # Identify top five products
    top_five = product_revenue.head(5)

    # Calculate quantity sold by product
    product_quantity = (
        df.groupby("ProductName")["Quantity"]
        .sum()
        .sort_values(ascending=False)
    )

    # Identify highest quantity product
    if not product_quantity.empty:
        highest_quantity_product = product_quantity.idxmax()
    else:
        highest_quantity_product = None

    return (
        product_revenue,
        top_five,
        product_quantity,
        highest_quantity_product
    )
