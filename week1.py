import pandas as pd
from pathlib import Path


# ============================================================
# Week 1 — Monthly Dataset Aggregation
# IDX Exchange Data Analyst Internship
#
# Objective:
# 1. Load all monthly MLS Listing and Sold CSV files
#    from January 2024 through the most recently completed month.
# 2. Concatenate the monthly files into two combined datasets.
# 3. Filter both datasets to PropertyType == "Residential".
# 4. Save the Residential-filtered datasets as new CSV files.
# 5. Document row counts before/after concatenation and filtering.
# ============================================================


# ------------------------------------------------------------
# 1. Define file paths
# ------------------------------------------------------------

# The "csv" folder contains all monthly MLS datasets.
DATA_DIR = Path(
    "/Users/wy/Desktop/idx excahnge/data analyst/dataset/csv"
)

# Output folder
OUTPUT_DIR = DATA_DIR / "week1_output"
OUTPUT_DIR.mkdir(exist_ok=True)


# ------------------------------------------------------------
# 2. Find all monthly Listing and Sold files
# ------------------------------------------------------------

# Listing files:
# CRMLSListing202401.csv
# CRMLSListing202402.csv
# ...
# CRMLSListing202604.csv

listing_files = sorted(DATA_DIR.glob("CRMLSListing*.csv"))

# Sold files:
# CRMLSSold202401_filled.csv
# CRMLSSold202402_filled.csv
# ...
# CRMLSSold202604.csv

sold_files = sorted(DATA_DIR.glob("CRMLSSold*.csv"))


# Print the number of files found
print("=" * 70)
print("FILE CHECK")
print("=" * 70)

print(f"Listing files found: {len(listing_files)}")
print(f"Sold files found:    {len(sold_files)}")


# ------------------------------------------------------------
# 3. Check that the expected 56 files were found
# ------------------------------------------------------------

# We expect:
# 28 monthly Listing files
# 28 monthly Sold files
# Total = 56 files

if len(listing_files) != 28:
    raise ValueError(
        f"Expected 28 Listing files, but found {len(listing_files)}."
    )

if len(sold_files) != 28:
    raise ValueError(
        f"Expected 28 Sold files, but found {len(sold_files)}."
    )

print("File count check passed: 28 Listing + 28 Sold = 56 files.")


# ------------------------------------------------------------
# 4. Display the files that will be loaded
# ------------------------------------------------------------

print("\nListing files:")
for file in listing_files:
    print("  ", file.name)

print("\nSold files:")
for file in sold_files:
    print("  ", file.name)


# ------------------------------------------------------------
# 5. Load and concatenate Listing datasets
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("LOADING LISTING DATA")
print("=" * 70)

listing_dfs = []

for file in listing_files:
    print(f"Reading: {file.name}")

    df = pd.read_csv(file)

    # Store the monthly dataframe
    listing_dfs.append(df)

# Confirm total row count before concatenation
listing_rows_before_concat = sum(len(df) for df in listing_dfs)

print("\nListing rows before concatenation:")
print(f"{listing_rows_before_concat:,}")

# Concatenate all monthly Listing files
listings = pd.concat(
    listing_dfs,
    ignore_index=True
)

# Row count immediately after concatenation
listing_rows_before_filter = len(listings)

print("\nListing rows after concatenation:")
print(f"{listing_rows_before_filter:,}")

print("Listing columns:")
print(f"{listings.shape[1]:,}")


# ------------------------------------------------------------
# 6. Load and concatenate Sold datasets
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("LOADING SOLD DATA")
print("=" * 70)

sold_dfs = []

for file in sold_files:
    print(f"Reading: {file.name}")

    df = pd.read_csv(file)

    # Store the monthly dataframe
    sold_dfs.append(df)


# Row count before concatenation
sold_rows_before_concat = sum(len(df) for df in sold_dfs)

print("\nSold rows before concatenation:")
print(f"{sold_rows_before_concat:,}")

# Concatenate all monthly Sold files
sold = pd.concat(
    sold_dfs,
    ignore_index=True
)

# Row count immediately after concatenation
sold_rows_before_filter = len(sold)

print("\nSold rows after concatenation:")
print(f"{sold_rows_before_filter:,}")

print("Sold columns:")
print(f"{sold.shape[1]:,}")


# ------------------------------------------------------------
# 7. Check PropertyType values before filtering
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("PROPERTY TYPE CHECK")
print("=" * 70)

print("\nListing PropertyType values:")
print(listings["PropertyType"].value_counts(dropna=False))

print("\nSold PropertyType values:")
print(sold["PropertyType"].value_counts(dropna=False))


# ------------------------------------------------------------
# 8. Filter Listing dataset to Residential
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("FILTERING LISTINGS")
print("=" * 70)

listing_residential = listings[
    listings["PropertyType"] == "Residential"
].copy()

listing_rows_after_filter = len(listing_residential)

print(f"Listing rows before Residential filter: "
      f"{listing_rows_before_filter:,}")

print(f"Listing rows after Residential filter:  "
      f"{listing_rows_after_filter:,}")

print(f"Listing rows removed: "
      f"{listing_rows_before_filter - listing_rows_after_filter:,}")


# ------------------------------------------------------------
# 9. Filter Sold dataset to Residential
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("FILTERING SOLD DATA")
print("=" * 70)

sold_residential = sold[
    sold["PropertyType"] == "Residential"
].copy()

sold_rows_after_filter = len(sold_residential)

print(f"Sold rows before Residential filter: "
      f"{sold_rows_before_filter:,}")

print(f"Sold rows after Residential filter:  "
      f"{sold_rows_after_filter:,}")

print(f"Sold rows removed: "
      f"{sold_rows_before_filter - sold_rows_after_filter:,}")


# ------------------------------------------------------------
# 10. Save the Residential-filtered datasets
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("SAVING OUTPUT FILES")
print("=" * 70)

listing_output = OUTPUT_DIR / "CRMLSListing_202401_202604_Residential.csv"
sold_output = OUTPUT_DIR / "CRMLSSold_202401_202604_Residential.csv"

listing_residential.to_csv(
    listing_output,
    index=False
)

sold_residential.to_csv(
    sold_output,
    index=False
)

print(f"Listing output saved to:")
print(f"  {listing_output}")

print(f"\nSold output saved to:")
print(f"  {sold_output}")


# ------------------------------------------------------------
# 11. Final summary
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("WEEK 1 SUMMARY")
print("=" * 70)

print("\nLISTINGS")
print(f"Files loaded:              {len(listing_files)}")
print(f"Rows before concatenation: {listing_rows_before_concat:,}")
print(f"Rows after concatenation:  {listing_rows_before_filter:,}")
print(f"Rows after Residential:    {listing_rows_after_filter:,}")
print(f"Rows removed:              "
      f"{listing_rows_before_filter - listing_rows_after_filter:,}")

print("\nSOLD")
print(f"Files loaded:              {len(sold_files)}")
print(f"Rows before concatenation: {sold_rows_before_concat:,}")
print(f"Rows after concatenation:  {sold_rows_before_filter:,}")
print(f"Rows after Residential:    {sold_rows_after_filter:,}")
print(f"Rows removed:              "
      f"{sold_rows_before_filter - sold_rows_after_filter:,}")

print("\nOutput files:")
print(f"  {listing_output.name}")
print(f"  {sold_output.name}")

print("\nWeek 1 aggregation completed successfully!")

'''
======================================================================
WEEK 1 SUMMARY
======================================================================

LISTINGS
Files loaded:              28
Rows before concatenation: 860,898
Rows after concatenation:  860,898
Rows after Residential:    547,162
Rows removed:              313,736

SOLD
Files loaded:              28
Rows before concatenation: 615,707
Rows after concatenation:  615,707
Rows after Residential:    414,054
Rows removed:              201,653

Output files:
  CRMLSListing_202401_202604_Residential.csv
  CRMLSSold_202401_202604_Residential.csv

Week 1 aggregation completed successfully!

Process finished with exit code 0
'''