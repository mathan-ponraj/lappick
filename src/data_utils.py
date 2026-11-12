from datetime import datetime, timezone
from pathlib import Path
import pandas as pd

DATA_DIR = Path("data")
OUTPUT_FILE = DATA_DIR / "live_laptops.csv"

def normalize_products(payload: dict) -> list[dict]:
    """Convert API.SH Croma search results into a consistent tabular schema."""
    rows = payload.get("products", []) if isinstance(payload, dict) else []
    normalized = []
    fetched_at = payload.get("fetched_at") or datetime.now(timezone.utc).isoformat()

    for item in rows:
        if not isinstance(item, dict):
            continue
        normalized.append({
            "product_code": item.get("code"),
            "name": item.get("name"),
            "brand": item.get("brand"),
            "price_inr": item.get("price"),
            "mrp_inr": item.get("mrp"),
            "discount": item.get("discount"),
            "rating": item.get("rating"),
            "ratings_count": item.get("ratings_count"),
            "reviews_count": item.get("reviews_count"),
            "warranty_months": item.get("warranty_months"),
            "highlights": item.get("highlights"),
            "image_url": item.get("image"),
            "product_url": item.get("url"),
            "fetched_at": fetched_at,
            "source": "Croma via API.SH",
        })
    return normalized

def save_products(products: list[dict]) -> Path:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(products)
    if OUTPUT_FILE.exists():
        old = pd.read_csv(OUTPUT_FILE)
        df = pd.concat([old, df], ignore_index=True)
        if "product_code" in df.columns:
            df = df.drop_duplicates(subset=["product_code", "fetched_at"], keep="last")
    df.to_csv(OUTPUT_FILE, index=False)
    return OUTPUT_FILE
