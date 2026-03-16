"""
PROJECT: Automated Country Risk Rating Engine
=============================================
PURPOSE:
Aggregates and synchronizes multiple international risk indices to produce
a unified 0.0 to 10.0 Risk Score for global AML and Sanctions compliance.

LOGIC ARCHITECTURE:
1. NORMALIZATION: Flips the CPI score (where high is good) so that 10.0
   consistently represents Maximum Risk across all data points.
2. AGGREGATION: Calculates the base average of Basel and CPI metrics.
3. WEIGHTING: Applies FATF Multipliers (1.5x for Grey List, 2.0x for Black List)
   to the base average to reflect international financial restrictions.
4. CATEGORIZATION: Tags results as 'High', 'Medium', or 'Low' risk.

DEPENDENCIES (Expected in the /Data folder):
- Countries.json: Master list for iteration (ISO Alpha3 & Region).
- Basel_Index.json: AML Risk values (0-10 scale).
- CPI.json: Corruption Perception values (0-100 scale).
- FATF_Lists.json: Arrays for 'fatf_black_list' and 'fatf_grey_list'.

OUTPUT:
Generates 'Country_Risk_Rating.json' in the project root.
"""


import json
import os

# File Paths
DATA_DIR = "Data"
BASEL_FILE = os.path.join(DATA_DIR, "Basel_Index.json")
COUNTRIES_FILE = os.path.join(DATA_DIR, "Countries.json")
CPI_FILE = os.path.join(DATA_DIR, "CPI.json")
FATF_FILE = os.path.join(DATA_DIR, "FATF_Lists.json")
OUTPUT_FILE = "Data/Country_Risk_Rating.json"


def load_json(filepath):
    """Safely loads JSON data from a file."""
    try:
        if not os.path.exists(filepath):
            print(f"Warning: {filepath} not found.")
            return None
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None


def list_to_map(data_list, key_name="name", value_name="score"):
    """Converts a list of dicts like [{'name': 'X', 'score': 5}] to a dict {'X': 5}"""
    if not data_list or not isinstance(data_list, list):
        return {}
    return {item[key_name]: item.get(value_name) for item in data_list if key_name in item}


def calculate_risk():
    # 1. Load Data
    raw_countries = load_json(COUNTRIES_FILE)
    raw_basel = load_json(BASEL_FILE)
    raw_cpi = load_json(CPI_FILE)
    fatf_data = load_json(FATF_FILE) or {}

    # 2. Process lists into searchable dictionaries
    basel_map = list_to_map(raw_basel)
    cpi_map = list_to_map(raw_cpi)

    # FATF uses specific keys: "fatf_black_list" and "fatf_grey_list"
    blacklist = fatf_data.get("fatf_black_list", [])
    greylist = fatf_data.get("fatf_grey_list", [])

    risk_report = {}

    if not raw_countries:
        print("Error: No country data found. Aborting.")
        return

    # 3. Iterate through Countries
    for country_obj in raw_countries:
        name = country_obj.get("name")
        if not name:
            continue

        # --- A. Basel Score (0-10, Higher = Riskier) ---
        b_score = basel_map.get(name)
        if b_score is None:
            b_score = 5.0

        # --- B. CPI Score (0-100, Higher = Cleaner) ---
        raw_cpi_val = cpi_map.get(name)
        if raw_cpi_val is None:
            raw_cpi_val = 50  # Default mid-point
            c_score = 5.0
        else:
            # Normalize: (100 - Score) / 10
            c_score = (100 - raw_cpi_val) / 10

        # --- C. FATF Multipliers ---
        fatf_multiplier = 1.0
        status = "None"

        if name in blacklist:
            fatf_multiplier = 2.0
            status = "Black_List"
        elif name in greylist:
            fatf_multiplier = 1.5
            status = "Grey_List"

        # --- D. Final Calculation ---
        base_avg = (b_score + c_score) / 2
        final_score = round(min(base_avg * fatf_multiplier, 10.0), 2)

        # Categorization logic
        if final_score >= 7.0:
            rating = "High"
        elif final_score >= 4.0:
            rating = "Medium"
        else:
            rating = "Low"

        # Add to report with refactored keys and risk_score explicitly included
        risk_report[name] = {
            "iso_alpha3": country_obj.get("alpha3"),
            "region": country_obj.get("region"),
            "risk_score": final_score,
            "risk_rating": rating,
            "fatf_status": status,
            "metrics": {
                "risk_score_value": final_score,
                "basel_score": b_score,
                "raw_cpi": raw_cpi_val,
                "normalized_cpi": round(c_score, 2)
            }
        }

    # 4. Save result to project root
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(risk_report, f, indent=4)
        print(f"Successfully generated {OUTPUT_FILE} with {len(risk_report)} countries.")
    except Exception as e:
        print(f"Failed to write output: {e}")


if __name__ == "__main__":
    calculate_risk()