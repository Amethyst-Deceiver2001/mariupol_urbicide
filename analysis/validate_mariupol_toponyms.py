import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'mariupol_mission_critical')
DB_USER = os.getenv('DB_USER', 'mariupol_researcher')
DB_PASSWORD = os.getenv('DB_PASSWORD')

conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)
cur = conn.cursor()

print("--- Data Validation: mariupol_toponyms ---\n")

# 1. Total number of toponyms
cur.execute("SELECT COUNT(*) FROM mariupol_toponyms;")
total = cur.fetchone()[0]
print(f"Total toponyms: {total}")

# 2. Duplicates by osm_id
cur.execute("SELECT osm_id, COUNT(*) FROM mariupol_toponyms GROUP BY osm_id HAVING COUNT(*) > 1;")
dups = cur.fetchall()
if dups:
    print(f"\nDuplicate osm_id entries:")
    for osm_id, count in dups:
        print(f"  osm_id: {osm_id}, count: {count}")
else:
    print("\nNo duplicate osm_id entries found.")

# 3. Nulls in critical fields
cur.execute("SELECT COUNT(*) FROM mariupol_toponyms WHERE name IS NULL OR name_ru IS NULL OR name_uk IS NULL OR geom IS NULL;")
nulls = cur.fetchone()[0]
print(f"\nRows with NULL in name, name_ru, name_uk, or geom: {nulls}")

# 4. Unique types and districts (show up to 20)
cur.execute("SELECT DISTINCT type, type_ru, type_uk, district FROM mariupol_toponyms LIMIT 20;")
types = cur.fetchall()
print("\nSample unique (type, type_ru, type_uk, district):")
for row in types:
    print(f"  {row}")

# 5. Sample entries (show up to 10)
cur.execute("SELECT id, osm_id, name, name_ru, name_uk, type, district FROM mariupol_toponyms LIMIT 10;")
sample = cur.fetchall()
print("\nSample entries:")
for row in sample:
    print(f"  {row}")

cur.close()
conn.close()
print("\nValidation complete.")
