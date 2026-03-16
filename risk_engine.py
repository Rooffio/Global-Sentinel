"""
AML Customer Risk Rating (CRR) Engine
-------------------------------------
Author: [Your Name/GitHub Handle]
Version: 1.0.0

DESCRIPTION:
This engine calculates the Residual Risk for a banking customer base.
It uses a Multi-Factor Weighted Scoring model combined with Compliance
Hard Overrides (Automatic High Risk triggers).

METHODOLOGY:
1. Data Ingestion: Merges Core, Product, Behavioral, and Compliance datasets.
2. Weighted Scoring: Applies specific weights to different risk pillars
   (Geography, Product, Behavior, etc.) based on a 1-10 scale.
3. Hard Overrides: Critical threats (PEPs, Sanctions) bypass the weighted
   average to be locked into 'High Risk'.
4. Categorization: Final scores are bucketed into Low, Medium, and High.
"""


import pandas as pd
import numpy as np
import json
import os
import sys


def run_risk_engine():
    """
    Main execution engine with Weighted Scoring and Hard Overrides (Automatic High Risk Triggers).
    This ensures that critical risk factors cannot be 'diluted' by a weighted average.
    """
    # --- 1. SETUP & PATHS ---
    DATA_DIR = "Data"
    # CSVs
    table1_path = os.path.join(DATA_DIR, "Table1_Core_Customer_Data.csv")
    table2_path = os.path.join(DATA_DIR, "Table2_Account_Product_Data.csv")
    table3_path = os.path.join(DATA_DIR, "Table3_Transactional_Summary.csv")
    table4_path = os.path.join(DATA_DIR, "Table4_Compliance_Screening.csv")
    # JSONs
    country_risk_path = "Data/Country_Risk_Rating.json"
    product_risk_path = "Data/Product_Risk_Rating.json"
    delivery_risk_path = os.path.join(DATA_DIR, "Delivery_Channels.json")

    print("🚀 Initializing Master Risk Engine with Hard Overrides...")

    # --- 2. LOAD LOOKUP DATA (MATRICES) ---
    try:
        with open(country_risk_path, 'r') as f:
            country_data = json.load(f)
            country_lookup = {name: info['risk_score'] for name, info in country_data.items()}

        with open(product_risk_path, 'r') as f:
            product_data = json.load(f)
            product_lookup = {item['product']: item['residual_risk_score'] for item in product_data}

        with open(delivery_risk_path, 'r') as f:
            delivery_raw = json.load(f)
            delivery_list = delivery_raw.get('delivery_channel_risk', [])
            delivery_lookup = {item['channel']: item['risk_score'] for item in delivery_list}

    except Exception as e:
        print(f"❌ Initialization Error: {e}")
        return

    # --- 3. LOAD & MERGE CLIENT DATA ---
    print("📥 Loading and Merging Datasets...")
    try:
        df1 = pd.read_csv(table1_path)
        df3 = pd.read_csv(table3_path).rename(columns={'customer_id': 'customer_no'})
        df4 = pd.read_csv(table4_path).rename(columns={'customer_id': 'customer_no'})

        # Table 2: Aggregating to find Max Product Risk per Client
        df2 = pd.read_csv(table2_path)
        df2['prod_score'] = df2['product_name'].map(product_lookup)
        max_prod_df = df2.groupby('customer_id')['prod_score'].max().reset_index()
        max_prod_df.columns = ['customer_no', 'product_risk_score']

        # Master Merge
        master_df = df1.merge(df3, on='customer_no').merge(df4, on='customer_no').merge(max_prod_df, on='customer_no')
    except Exception as e:
        print(f"❌ Error during data merge: {e}")
        return

    # --- 4. SCORING DICTIONARY (Non-JSON Criteria) ---
    risk_map = {
        "Individual": 2, "Sole trader": 5, "Company": 5, "Trust": 9, "NGO": 9, "Shell Bank": 10,
        "Biometric + Gov ID": 2, "Government ID verified": 5, "Minimal": 9,
        "Professional services": 2, "High-cash retail": 7, "High-value goods": 9,
        "None": 1, "Domestic PEP": 6, "RCA": 7, "Foreign PEP": 10,
        "Verified": 2, "Mixed": 5, "Unverifiable": 10,
        "Low": 2, "Medium": 5, "High": 10,
        "Full docs": 1, "Standard capture": 5, "Missing / Expired": 10,
        "Up-to-Date": 1, "Overdue": 10
    }

    # --- 5. WEIGHTED CALCULATION ---
    print("⚖️ Calculating Weighted Base Scores...")
    master_df['s_geo'] = master_df['residency_country'].map(country_lookup).fillna(5) * 1.4
    master_df['s_prod'] = master_df['product_risk_score'].fillna(5) * 1.2
    master_df['s_chan'] = master_df['onboarding_channel'].map(delivery_lookup).fillna(5) * 0.8
    master_df['s_ident'] = master_df['customer_type'].map(risk_map).fillna(5) * 1.0
    master_df['s_beh'] = master_df['cash_intensity'].map(risk_map).fillna(5) * 1.5
    master_df['s_ctrl'] = master_df['kyc_status'].map(risk_map).fillna(5) * 1.1

    total_weights = 1.4 + 1.2 + 0.8 + 1.0 + 1.5 + 1.1
    master_df['final_weighted_score'] = (
                                                master_df['s_geo'] + master_df['s_prod'] + master_df['s_chan'] +
                                                master_df['s_ident'] + master_df['s_beh'] + master_df['s_ctrl']
                                        ) / total_weights

    # --- 6. OVERRIDE LOGIC (AUTOMATIC HIGH TRIGGERS) ---
    print("⚠️ Applying Hard Overrides (Automatic High Triggers)...")

    master_df['override_triggered'] = False
    master_df['override_reason'] = "None"

    # Define strict conditions for an 'Automatic High' rating
    # 1. Foreign PEPs
    # 2. Sanctions or Criminal Media hits
    # 3. Prohibited Entities (Shell Banks)
    # 4. Countries with score >= 9.5 (Sanctioned/Extreme Risk)
    # 5. Opaque ownership (Nominee UBOs or Bearer Shares)

    override_conditions = [
        (master_df['pep_status'] == "Foreign PEP"),
        (master_df['media_status'] == "Sanctions / Criminal"),
        (master_df['customer_type'] == "Shell Bank"),
        (master_df['ubo_clarity'] == "Nominee / Opaque"),
        (master_df['bearer_instrument_flag'] == "Bearer-Shares"),
        (master_df['residency_country'].map(country_lookup) >= 9.5)
    ]

    reasons = [
        "Foreign PEP",
        "Sanctions / Criminal Media",
        "Prohibited Entity (Shell Bank)",
        "Opaque UBO Structure",
        "Bearer Instruments Present",
        "Extreme-Risk Jurisdiction"
    ]

    for cond, reason in zip(override_conditions, reasons):
        master_df.loc[cond, 'final_weighted_score'] = 10.0
        master_df.loc[cond, 'override_triggered'] = True
        master_df.loc[cond, 'override_reason'] = reason

    # --- 7. CATEGORIZATION ---
    def categorize_risk(score):
        if score < 3.5:
            return "Low"
        elif score < 6.5:
            return "Medium"
        else:
            return "High"

    master_df['risk_rating'] = master_df['final_weighted_score'].apply(categorize_risk)

    # --- 8. EXPORT RESULTS ---
    output_path = os.path.join(DATA_DIR, "Final_Customer_Risk_Rating.csv")
    export_columns = [
        'customer_no', 'customer_name', 'customer_type', 'residency_country',
        'final_weighted_score', 'risk_rating', 'override_triggered', 'override_reason'
    ]
    master_df[export_columns].to_csv(output_path, index=False)

    print(f"✅ Risk Calculation Complete.")
    print(f"📝 Results saved to: {output_path}")
    print(f"🚩 Total Overrides Applied: {master_df['override_triggered'].sum()}")
    print("\n--- Risk Distribution Summary ---")
    print(master_df['risk_rating'].value_counts())
    print("---------------------------------")


if __name__ == "__main__":
    run_risk_engine()