from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt


OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


def create_charts(df):
    chart_paths = []
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if "date" in df.columns and "sales" in df.columns:
        sales_by_date = df.groupby("date")["sales"].sum().sort_index()

        plt.figure(figsize=(8, 5))
        sales_by_date.plot(marker="o")
        plt.title("Sales Over Time")
        plt.xlabel("Date")
        plt.ylabel("Sales")
        plt.tight_layout()

        path = OUTPUT_DIR / f"sales_over_time_{timestamp}.png"
        plt.savefig(path)
        plt.close()
        chart_paths.append(str(path))

    if "region" in df.columns and "sales" in df.columns:
        sales_by_region = df.groupby("region")["sales"].sum().sort_values(ascending=False)

        plt.figure(figsize=(8, 5))
        sales_by_region.plot(kind="bar")
        plt.title("Sales by Region")
        plt.xlabel("Region")
        plt.ylabel("Sales")
        plt.tight_layout()

        path = OUTPUT_DIR / f"sales_by_region_{timestamp}.png"
        plt.savefig(path)
        plt.close()
        chart_paths.append(str(path))

    if "date" in df.columns and "customers" in df.columns:
        customers_by_date = df.groupby("date")["customers"].sum().sort_index()

        plt.figure(figsize=(8, 5))
        customers_by_date.plot(marker="o")
        plt.title("Customers Over Time")
        plt.xlabel("Date")
        plt.ylabel("Customers")
        plt.tight_layout()

        path = OUTPUT_DIR / f"customers_over_time_{timestamp}.png"
        plt.savefig(path)
        plt.close()
        chart_paths.append(str(path))

    return chart_paths