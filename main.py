import argparse
import pandas as pd
import sys
from pathlib import Path

# Add your source directory to the path (adjust if needed)
sys.path.append("D:/finance")  # or use "." if everything is local

from funcs.chart_funcs import generate_chart_with_templates
from funcs.data_cleanse import data_cleanse


def main():
    parser = argparse.ArgumentParser(
        description="Generate interactive debit chart from transaction CSV."
    )
    parser.add_argument("--csv", default="george.csv", help="Path to input CSV file")
    parser.add_argument(
        "--output", default="chart.html", help="Path to output HTML file"
    )
    parser.add_argument(
        "--since",
        default="2024-01-01",
        help="Filter transactions after this booking date (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--encoding",
        default="utf-16",
        help="Encoding of the CSV file (default: utf-16)",
    )

    args = parser.parse_args()

    if not Path(args.csv).exists():
        print(f"❌ Error: File not found at {args.csv}")
        return

    # Load and clean data
    df = pd.read_csv(args.csv, encoding=args.encoding)
    df = data_cleanse(df)

    # Filter by date
    df = df[df["booking_date"] > args.since]

    # Extract categories
    if "category_high_lvl" not in df.columns:
        print("❌ Error: 'category_high_lvl' column not found in the dataset.")
        return

    categories = df["category_high_lvl"].dropna().unique().tolist()

    # Generate the chart
    generate_chart_with_templates(df, categories, output_file=args.output)


if __name__ == "__main__":
    main()
