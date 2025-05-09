import re

def parse_query(query):
    query = query.strip().lower()

    # 🏷 Extract price
    price_match = re.search(r'(under|below|less than|for|within)\s*(₹)?(\d{4,6})', query)
    price_limit = int(price_match.group(3)) if price_match else None

    # 🏷 Extract brand (simple list match)
    brands = ["hp", "dell", "lenovo", "asus", "acer", "msi", "apple"]
    brand = next((b for b in brands if b in query), None)

    # 🏷 Extract RAM (e.g., 8gb, 16 gb)
    ram_match = re.search(r'(\d{1,2})\s*gb\s*ram', query)
    ram = int(ram_match.group(1)) if ram_match else None

    # 🏷 Extract SSD/HDD keyword
    if "ssd" in query:
        storage_type = "ssd"
    elif "hdd" in query:
        storage_type = "hdd"
    else:
        storage_type = None

    return {
        "raw": query,
        "price_limit": price_limit,
        "brand": brand,
        "ram": ram,
        "storage_type": storage_type
    }
