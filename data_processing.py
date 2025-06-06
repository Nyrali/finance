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
