#!/usr/bin/env python3
"""
Remove duplicate products from the database
Keeps the oldest entry for each (source, reference) pair
"""

import sqlite3
import os

DB_PATH = os.environ.get("DB_PATH", "backend/data/fittingroom.db")

def clean_duplicates():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Count duplicates before
    cursor.execute("""
        SELECT COUNT(*) FROM products
        WHERE id NOT IN (
            SELECT MIN(id) FROM products GROUP BY source, reference
        )
    """)
    dup_count = cursor.fetchone()[0]
    
    if dup_count == 0:
        print("✅ No duplicates found!")
        conn.close()
        return
    
    print(f"🔍 Found {dup_count} duplicate products")
    
    # Delete duplicates
    cursor.execute("""
        DELETE FROM products
        WHERE id NOT IN (
            SELECT MIN(id) FROM products GROUP BY source, reference
        )
    """)
    
    conn.commit()
    deleted = cursor.rowcount
    print(f"🗑️  Deleted {deleted} duplicate entries")
    
    # Vacuum database to reclaim space
    cursor.execute("VACUUM")
    print("✨ Database optimized")
    
    conn.close()

if __name__ == "__main__":
    clean_duplicates()
