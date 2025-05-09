import sqlite3
import hashlib
import os

DB_PATH = "data/query_cache.db"

# Ensure cache table exists
def init_cache():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cache (
        key TEXT PRIMARY KEY,
        response TEXT
    )
    """)
    conn.commit()
    conn.close()

# Convert dict to hashable key
def generate_key(parsed_query: dict) -> str:
    key_string = str(sorted(parsed_query.items()))
    return hashlib.sha256(key_string.encode()).hexdigest()

def get_cached_response(key: str) -> str:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT response FROM cache WHERE key = ?", (key,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def save_response_to_cache(key: str, response: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO cache (key, response) VALUES (?, ?)", (key, response))
    conn.commit()
    conn.close()
