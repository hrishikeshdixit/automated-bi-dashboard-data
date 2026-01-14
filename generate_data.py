import pandas as pd
import random
import os
from datetime import datetime

file_path = "data/amazon.csv"

print("Starting data generator...")

df = pd.read_csv(file_path)
print(f"Rows before update: {len(df)}")

df.columns = df.columns.str.strip()

# Safe review_id extraction
df["review_id_num"] = (
    df["review_id"]
    .astype(str)
    .str.extract(r'(\d+)')[0]
    .fillna(0)
    .astype(int)
)

last_review_id = df["review_id_num"].max()
products = df["product_id"].unique()

num_new = random.randint(10, 20)
print(f"Generating {num_new} new rows")

new_rows = []

for i in range(num_new):
    product_id = random.choice(products)
    product_row = df[df["product_id"] == product_id].iloc[0]

    new_rows.append({
        "product_id": product_id,
        "product_name": product_row["product_name"],
        "category1": product_row["category1"],
        "category2": product_row["category2"],
        "category3": product_row["category3"],
        "discounted_price": product_row["discounted_price"],
        "actual_price": product_row["actual_price"],
        "discount_percentage": product_row["discount_percentage"],
        "rating": round(random.uniform(1, 5), 1),
        "rating_count": None,
        "about_product": product_row["about_product"],
        "user_id": f"U{random.randint(100000,999999)}",
        "user_name": f"user_{random.randint(10000,99999)}",
        "review_id": f"R{last_review_id + i + 1}",
        "review_title": "Automated Review",
        "review_content": "This review was generated automatically.",
        "img_link": product_row["img_link"],
        "product_link": product_row["product_link"]
    })

new_df = pd.DataFrame(new_rows)
print(f"New rows created: {len(new_df)}")

df_final = pd.concat([df.drop(columns=["review_id_num"]), new_df], ignore_index=True)
print(f"Rows after update: {len(df_final)}")

df_final.to_csv(file_path, index=False)
print("CSV saved successfully")
