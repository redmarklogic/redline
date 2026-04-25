import pandas as pd

path = r"G:\My Drive\Library\library-index.xlsx"
df = pd.read_excel(path, sheet_name="Master")

# Show each row with key fields
cols_to_show = ["sha256", "title", "author", "publisher", "year", "edition", "domain", "subdomain", "category", "path", "notes"]
for col in cols_to_show:
    if col not in df.columns:
        print(f"MISSING COLUMN: {col}")

available = [c for c in cols_to_show if c in df.columns]
pd.set_option("display.max_colwidth", 80)
pd.set_option("display.max_rows", 100)
print(df[available].to_string())

# Also show Engineering sheet
print("\n\n=== ENGINEERING SHEET ===")
df_eng = pd.read_excel(path, sheet_name="Engineering")
print(f"Columns: {list(df_eng.columns)}")
print(f"Rows: {len(df_eng)}")
if len(df_eng) > 0:
    print(df_eng.to_string())
