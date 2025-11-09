#!/usr/bin/env python3
import json, csv, os, time, pathlib, requests
import logging

logger = logging.getLogger(__name__)

CATEGORY_API = {
    "jackets": "https://www.zara.com/us/en/category/2417772/products?regionGroupId=133&ajax=true",
    "tops": "https://www.zara.com/us/en/category/2419940/products?regionGroupId=133&ajax=true",
    "pants": "https://www.zara.com/us/en/category/2420795/products?regionGroupId=133&ajax=true",
    "dresses": "https://www.zara.com/us/en/category/2420896/products?regionGroupId=133&ajax=true",
    "skirts": "https://www.zara.com/us/en/category/2420454/products?regionGroupId=133&ajax=true",
    "jeans": "https://www.zara.com/us/en/category/2419185/products?regionGroupId=133&ajax=true",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.zara.com/",
}


def first_or_none(xs):
    return xs[0] if isinstance(xs, list) and xs else None


def image_from_xmedia(xmedia):
    """Pick a representative image URL if present."""
    if not xmedia:
        return None
    for xm in xmedia:
        extra = xm.get("extraInfo") or {}
        if extra.get("deliveryUrl"):
            return extra["deliveryUrl"]
    return xmedia[0].get("url")


def build_product_url(keyword, seo_product_id):
    if keyword and seo_product_id:
        return f"https://www.zara.com/us/en/{keyword}-p{seo_product_id}.html"
    return None


def normalize(json_data, category_name):
    out_rows = []
    pgroups = json_data.get("productGroups") or []
    for grp in pgroups:
        elements = grp.get("elements") or []
        for el in elements:
            comps = el.get("commercialComponents") or []
            for comp in comps:
                if (comp.get("type") or "").lower() != "product":
                    continue

                pid = comp.get("id")
                name = comp.get("name")
                availability = comp.get("availability")
                price_cents = comp.get("price")
                price = round((price_cents or 0) / 100, 2)

                seo = comp.get("seo") or {}
                keyword = seo.get("keyword")
                seo_pid = seo.get("seoProductId")
                product_url = build_product_url(keyword, seo_pid)

                detail = comp.get("detail") or {}
                colors = detail.get("colors") or []
                color0 = first_or_none(colors) or {}
                color_name = color0.get("name")

                pdp_media = comp.get("pdpMedia")
                if pdp_media and (pdp_media.get("extraInfo") or {}).get("deliveryUrl"):
                    image_url = pdp_media["extraInfo"]["deliveryUrl"]
                else:
                    image_url = image_from_xmedia(color0.get("xmedia") or [])

                brand = (
                    (comp.get("brand") or {}).get("brandGroupCode") or "zara"
                ).title()

                out_rows.append(
                    {
                        "source": "zara",
                        "reference": pid,
                        "product_id": pid,
                        "name": name,
                        "brand": brand,
                        "price": price,
                        "price_cents": price_cents,
                        "availability": availability,
                        "color": color_name,
                        "image_url": image_url,
                        "product_url": product_url,
                        "category": category_name,
                    }
                )
    return out_rows


def fetch_zara_products(save_raw=True, save_csv=True, category_name="combined"):
    """
    Fetch products from Zara API and optionally save raw JSON and CSV
    Returns: list of normalized product dictionaries
    """
    logger.info("Fetching Zara products...")

    all_rows = []
    try:
        for category_name, api_url in CATEGORY_API.items():
            r = requests.get(api_url, headers=HEADERS, timeout=30)
            r.raise_for_status()
            data = r.json()
            print(category_name)
            if save_raw:
                ts = time.strftime("%Y%m%d-%H%M%S")
                raw_dir = pathlib.Path("data/raw")
                raw_dir.mkdir(parents=True, exist_ok=True)
                raw_path = raw_dir / f"zara_{category_name}_{ts}.json"
                with raw_path.open("w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                logger.info(f"Saved raw JSON → {raw_path}")

            rows = normalize(data, category_name)
            all_rows.extend(rows)
            logger.info(f"Parsed {len(rows)} products from Zara")

        if save_csv and all_rows:
            ts = time.strftime("%Y%m%d-%H%M%S")
            processed_dir = pathlib.Path("data/processed")
            processed_dir.mkdir(parents=True, exist_ok=True)
            csv_path = processed_dir / f"zara_combined.csv"
            with csv_path.open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=list(all_rows[0].keys()))
                writer.writeheader()
                writer.writerows(all_rows)
            logger.info(f"Saved CSV → {csv_path}")
    except Exception as e:
        logger.error(f"Error fetching Zara products: {e}")
        raise

    return all_rows


if __name__ == "__main__":
    products = fetch_zara_products()
    print(f"Successfully fetched {len(products)} products from Zara")
