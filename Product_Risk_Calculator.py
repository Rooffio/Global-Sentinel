import pandas as pd
import json
import os

"""
REFACTORED PRODUCT RISK CALCULATION ENGINE
------------------------------------------
This script integrates the dynamic weighting from Product_Risk_Factors.json
to calculate the Residual Risk of products listed in the assessment matrix.

Calculation Logic:
1. Inherent Risk = Sum of (RF_flag * RF_weight)
2. Control Strength = Sum of (MF_flag * MF_weight)
3. Residual Risk = Inherent Risk - Control Strength
"""

# Configuration
DATA_DIR = "Data"
FACTORS_FILE = os.path.join(DATA_DIR, "Product_Risk_Factors.json")
MATRIX_FILE = os.path.join(DATA_DIR, "Product_Risk_Assessment_Matrix.csv")
OUTPUT_FILE = "Data/Product_Risk_Rating.json"


def load_weight_map():
    """Loads weights from the Canvas-sourced JSON file."""
    if not os.path.exists(FACTORS_FILE):
        print(f"Error: Missing {FACTORS_FILE}")
        return None, None

    with open(FACTORS_FILE, 'r') as f:
        data = json.load(f)

    rf_weights = {k: v['weight'] for k, v in data['risk_factors'].items()}
    mf_weights = {k: v['weight'] for k, v in data['mitigating_factors'].items()}
    return rf_weights, mf_weights


def calculate_product_risk():
    # 1. Load weights from JSON
    rf_weight_map, mf_weight_map = load_weight_map()
    if not rf_weight_map: return

    # 2. Load the Product Matrix
    if not os.path.exists(MATRIX_FILE):
        print(f"Error: Missing {MATRIX_FILE}")
        return

    df = pd.read_csv(MATRIX_FILE)
    results = []

    # Identify relevant columns in CSV that exist in our Weight Map
    rf_cols = [c for c in df.columns if c in rf_weight_map]
    mf_cols = [c for c in df.columns if c in mf_weight_map]

    for _, row in df.iterrows():
        # A. Calculate Weighted Inherent Risk
        inherent_score = 0
        active_rf_count = 0
        for col in rf_cols:
            if row[col] == 1:
                inherent_score += rf_weight_map[col]
                active_rf_count += 1

        # B. Calculate Weighted Control Strength
        control_score = 0
        active_mf_count = 0
        for col in mf_cols:
            if row[col] == 1:
                control_score += mf_weight_map[col]
                active_mf_count += 1

        # C. Calculate Residual Risk
        # Note: We keep a minimum floor of 1.0
        # The control score is subtracted directly from the inherent score
        residual_raw = inherent_score - control_score
        final_score = round(max(min(residual_raw, 25.0), 1.0), 2)  # Scaled based on total possible weight

        # D. Normalize to a 1-10 Scale for standard reporting
        # Based on theoretical max weight of ~85 for RFs
        normalized_score = round(min((final_score / 20) * 10, 10.0), 2)

        # E. Determine Rating
        if normalized_score >= 7.0:
            rating = "High"
        elif normalized_score >= 4.0:
            rating = "Medium"
        else:
            rating = "Low"

        # F. Calculate Effectiveness Percentage
        effectiveness = 0
        if inherent_score > 0:
            effectiveness = round((control_score / inherent_score) * 100, 1)

        results.append({
            "category": row['Category'],
            "product": row['Product'],
            "residual_risk_score": normalized_score,
            "risk_rating": rating,
            "metrics": {
                "weighted_inherent_risk": inherent_score,
                "weighted_control_strength": control_score,
                "control_effectiveness_pct": f"{min(effectiveness, 100)}%"
            },
            "assumptions": row.get('Assumptions', "")
        })

    # Save Results
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4)

    print(f"Success: Processed {len(results)} products using Canvas-defined weights.")
    print(f"Output generated: {OUTPUT_FILE}")


if __name__ == "__main__":
    calculate_product_risk()