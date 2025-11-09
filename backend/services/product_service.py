from typing import List, Dict, Optional
import logging
from database.db_manager import DatabaseManager
import pandas as pd

path_name = "../data/processed/zara_combined.csv"


def search_items(
    csv_path=path_name,
    product_ids=None,
    style_keywords=None,
    min_price=None,
    max_price=None,
    sizes=None,
    brands=None,
    page=1,
    limit=20,
):
    """
    Search products in a CSV file based on filters (size, brand, price, etc.)
    Returns a dictionary with product IDs and metadata.
    """

    # --- Load CSV ---
    df = pd.read_csv(csv_path)

    # --- Filter step by step ---
    df["reference"] = df["reference"].astype(str)
    if product_ids:
        df = df[df["reference"].isin(product_ids)]

    # if sizes:
    #    df = df[df["size"].isin(sizes)]

    if brands:
        df = df[df["brand"].isin(brands)]

    if min_price is not None:
        df = df[df["price"] >= min_price]

    if max_price is not None:
        df = df[df["price"] <= max_price]

    # --- Optional: match style keywords (e.g., from NLP aesthetic) ---
    if style_keywords:
        keyword_mask = df["name"].str.contains(
            "|".join(style_keywords), case=False, na=False
        )
        df = df[keyword_mask]

    # --- Pagination ---
    start = (page - 1) * limit
    end = start + limit
    paginated = df.iloc[start:end]

    # --- Build response ---
    result = {"products": paginated.to_dict(orient="records"), "total": len(paginated)}

    return result


def get_product_by_id(csv_path=path_name, product_id=None):
    """
    Retrieve a single product by its ID from the CSV file.
    Returns a dictionary with product details or None if not found.
    """
    if product_id is None:
        raise ValueError("Product ID must be provided")

    # Load CSV
    df = pd.read_csv(csv_path)

    # Filter by product ID
    product = df[df["reference"] == product_id]

    if not product.empty:
        return product.iloc[0].to_dict()
    else:
        return None
