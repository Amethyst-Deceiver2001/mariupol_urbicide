import pandas as pd
import re
from transliterate import translit

# Translation dictionary for common Russian business types
RU_TYPE_TO_EN = {
    "магазин": "shop",
    "аптека": "pharmacy",
    "кафе": "cafe",
    "парикмахерская": "hairdresser",
    "киоск": "kiosk",
    "салон": "salon",
    "стоматологическая клиника": "dental clinic",
    "фотоателье": "photo studio",
    "зоотовары": "pet store",
    "ателье": "atelier",
    "гараж": "garage",
    "офисное помещение": "office space",
    "юридические": "legal services",
    "услуги": "services",
    "церковь": "church",
    "продуктов": "grocery",
    "одежды": "clothing",
    "продукты": "grocery",
    "мясо": "meat",
    "банк": "bank",
    "павильон": "pavilion",
    "unknown": "unknown"
    # Add more as needed
}

# List of known types for splitting
KNOWN_TYPES = sorted(RU_TYPE_TO_EN.keys(), key=len, reverse=True)

def parse_service_info(info):
    if pd.isnull(info) or str(info).strip() == "-":
        return pd.Series(["unknown", "", "unknown", "unknown", ""])
    s = str(info).strip().lower()
    # Try to match known type at the start
    for t in KNOWN_TYPES:
        if s.startswith(t):
            name = s[len(t):].strip(' "\'')
            service_type = t
            service_name = name if name else ""
            service_type_lat = translit(service_type, 'ru', reversed=True)
            # English translation
            service_type_en = RU_TYPE_TO_EN.get(service_type, service_type)
            # For name, transliterate if not empty, else blank
            service_name_en = translit(service_name, 'ru', reversed=True) if service_name else ""
            return pd.Series([service_type, service_name, service_type_lat, service_type_en, service_name_en])
    # Fallback: try quoted name
    m = re.match(r"([\w\s]+)\s+['\"]?(.+?)['\"]?$", s)
    if m:
        service_type = m.group(1).strip()
        service_name = m.group(2).strip()
        service_type_lat = translit(service_type, 'ru', reversed=True)
        service_type_en = RU_TYPE_TO_EN.get(service_type, service_type)
        service_name_en = translit(service_name, 'ru', reversed=True)
        return pd.Series([service_type, service_name, service_type_lat, service_type_en, service_name_en])
    # Fallback: treat whole as type
    service_type_lat = translit(s, 'ru', reversed=True)
    service_type_en = RU_TYPE_TO_EN.get(s, s)
    return pd.Series([s, "", service_type_lat, service_type_en, ""])

# File paths
XLSX_PATH = "data/raw/seized_nonresidential.xlsx"
GEOCODED_CSV_PATH = "data/processed/commercial_clean.csv"
OUTPUT_CSV_PATH = "data/processed/commercial_harmonized.csv"
SUMMARY_PATH = "data/processed/commercial_harmonized_summary.txt"

# Load Russian original data (skip metadata/header rows)
df_ru = pd.read_excel(XLSX_PATH, skiprows=2)

# Adjust these column names as needed!
col_address_ru = "Адрес"
col_service_info = "Информация о ранее осуществляемой деятельности"
col_area = "Ориентировочная площадь, кв.м"
col_date_pub = "Дата публикации"
col_date_cad = "Дата постановки на кадастровый учет"

df_ru[["service_type", "service_name", "service_type_lat", "service_type_en", "service_name_en"]] = df_ru[col_service_info].apply(parse_service_info)

def norm(s):
    return str(s).lower().replace("ё", "е").replace("й", "и").replace("'", "").replace('"', '').strip()

df_ru["street_norm"] = df_ru[col_address_ru].apply(lambda x: norm(x.split(",")[0]) if pd.notnull(x) else "")
df_ru["housenumber_norm"] = df_ru[col_address_ru].apply(
    lambda x: norm(x.split(",")[1]) if (pd.notnull(x) and "," in x) else ""
)
df_ru["orig_address_ru"] = df_ru[col_address_ru]

df_ua = pd.read_csv(GEOCODED_CSV_PATH)
df_ua["street_norm"] = df_ua["street"].apply(norm)
df_ua["housenumber_norm"] = df_ua["housenumber"].apply(norm)

df_merged = pd.merge(
    df_ru, df_ua,
    on=["street_norm", "housenumber_norm"],
    suffixes=("_ru", "_ua"),
    how="left"
)

print("Merged columns:", df_merged.columns.tolist())

output_cols = [
    "orig_address_ru",
    "address",    # Ukrainianized/geocoded address (from df_ua)
    "lat", "lon",
    "service_type", "service_type_lat", "service_type_en", "service_name", "service_name_en",
    col_area,
    col_date_pub,
    col_date_cad
]

rename_map = {
    "address": "address_ua",
    "service_type": "service_type",
    "service_type_lat": "service_type_lat",
    "service_type_en": "service_type_en",
    "service_name": "service_name",
    "service_name_en": "service_name_en",
    col_area: "area_sqm",
    col_date_pub: "date_published",
    col_date_cad: "date_cadastral"
}

missing = [col for col in output_cols if col not in df_merged.columns]
if missing:
    print("Warning: Missing columns in merged dataframe:", missing)
    for i, col in enumerate(output_cols):
        if col not in df_merged.columns:
            if col + "_ru" in df_merged.columns:
                output_cols[i] = col + "_ru"
            elif col + "_ua" in df_merged.columns:
                output_cols[i] = col + "_ua"

df_out = df_merged[output_cols].rename(columns=rename_map)
df_out = df_out.drop_duplicates()

df_out.to_csv(OUTPUT_CSV_PATH, index=False)
print(f"Harmonized commercial addresses written to {OUTPUT_CSV_PATH}")
print("df_out columns:", df_out.columns.tolist())

def find_col(possible_names):
    for name in possible_names:
        if name in df_out.columns:
            return name
    return None

service_type_col = find_col(["service_type", "service_type_ru", "service_type_en"])
service_name_col = find_col(["service_name", "service_name_ru", "service_name_en"])


with open(SUMMARY_PATH, "w") as f:
    f.write(f"Total entries: {len(df_out)}\n")
    f.write(f"With coordinates: {(~df_out['lat'].isnull() & ~df_out['lon'].isnull()).sum()}\n")
    f.write(f"Missing coordinates: {(df_out['lat'].isnull() | df_out['lon'].isnull()).sum()}\n")
    f.write("\nTop 10 service types:\n")
    if service_type_col:
        f.write(df_out[service_type_col].value_counts().head(10).to_string())
    else:
        f.write("No service_type column found.\n")
    f.write("\n\nTop 10 service names:\n")
    if service_name_col:
        f.write(df_out[service_name_col].value_counts().head(10).to_string())
    else:
        f.write("No service_name column found.\n")
print(f"Summary written to {SUMMARY_PATH}")

print(df_out.head())