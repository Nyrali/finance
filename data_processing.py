import pandas as pd
import sys

sys.path.append("D:/finance")
from chart_funcs import generate_chart_with_templates
from data_cleanse import data_cleanse

# Load CSV with correct encoding
df = pd.read_csv("D:/finance/george.csv", encoding="utf-16")
df = data_cleanse(df)

df_filter = df[df["booking_date"] > "2024-01-01"]
categories = [i for i in df["category_high_lvl"].unique()]

generate_chart_with_templates(df_filter, categories)


df = pd.read_csv(
    "D:/finance/patron.csv",
    sep=";",
)

df = patron_data_cleanse(df)
df["category_high_lvl"] = (
    df["category_high_lvl"]
    .fillna("Jiné finanční výdaje")  # skutečné NaN
    .astype(str)
    .replace(
        ["nan", "NaN", "None", ""], "Jiné finanční výdaje"
    )  # stringové "neviditelné" NaN
    .str.strip()
)


categories = [i for i in df["category_high_lvl"].unique()]
patron_generate_resizable_stacked_chart_html_1(df, categories)
