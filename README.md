# 🛡️ Global Sentinel — Multi-Tiered AML/CFT Risk & Intelligence Framework

**Global Sentinel** is a production-grade, modular AML/CFT risk orchestration engine engineered to automate the identification, quantification, and classification of financial crime threats. By fusing international regulatory indices with institutional behavioral telemetry, the framework delivers explainable, deterministic risk scoring across **Customer (KYC/KYB)**, **Product**, and **Jurisdictional (Country)** domains.

Built to bridge the gap between raw data engineering and regulatory intelligence, Global Sentinel transforms disparate data points into actionable compliance insights. This ensures a robust **Risk-Based Approach (RBA)** that is fully aligned with the expectations of global standard-setters and supervisory authorities.

---

# 🚀 Executive Summary

Global Sentinel operates as a **high-throughput multi-stage pipeline** designed to ingest and harmonize heterogeneous **CSV and JSON data feeds**. The system normalizes raw regulatory inputs into structured risk matrices, executing a sophisticated **Weighted Scoring Engine** that evaluates risk across six distinct pillars of financial crime vulnerability. 

Unlike "black-box" solutions, Global Sentinel prioritizes **explainability**—ensuring that every risk rating is backed by a transparent audit trail of specific risk factors and mitigating controls.

### **Enterprise-Scale Resilience**
The framework is architected for **high-cardinality datasets**, providing the computational power required for complex entity resolution and periodic portfolio reviews. It currently supports the orchestration of simulations involving:
* **200,000+ Unique Customer Profiles**: Comprehensive identity mapping including PII, UBO (Ultimate Beneficial Ownership) structures, and KYB entity hierarchies.
* **1.1 Million+ Product-Account Relationships**: Mapping complex 1:N relational nodes to detect risk propagation across product lines and nested accounts.

### **Precision Risk Decisioning**
At the core of the system is the **Master Risk Engine**, a hybrid decision-making layer that balances granular quantitative weighting with a **Zero-Tolerance Hard Override Logic**. 

* **Weighted Aggregation**: Allows compliance teams to tune the engine based on their institution’s specific **Risk Appetite Statement (RAS)**, weighting factors like behavior, channel, and jurisdiction.
* **Deterministic Guardrails**: Ensures that critical high-risk indicators—such as **Sanctions nexus, Foreign PEP exposure, Shell Bank status, or Opaque Beneficial Ownership**—trigger immediate, non-dilutable **High-Risk classifications**. 

By bypassing weighted averages when critical threats are detected, the system maintains absolute regulatory safety, institutional integrity, and a defensible posture for **SAR/STR filing** and internal audits.

---

## 🛡️ Core Capabilities & Risk Framework

Global Sentinel’s architecture is built on the principle of **Defensible Logic**. Each capability is designed to ensure that the transition from raw data to a Risk Rating is transparent, documented, and fully aligned with the **Risk-Based Approach (RBA)**.

* **Dynamic Jurisdictional Orchestration**
    The engine moves beyond static country lists by calculating a dynamic **Inherent Geography Risk (IGR)**. It merges qualitative data from the **Basel AML Index** with the **Transparency International Corruption Perceptions Index (CPI)**. To ensure instantaneous compliance with international shifts, the system applies automated **FATF Status Multipliers** (1.5x for Grey-listed / 2.0x for Black-listed jurisdictions), enabling immediate portfolio-wide re-rating.

* **Multi-Dimensional Product Risk Taxonomy**
    The system quantifies the specific "exploitability" of financial instruments using a net-risk calculation. It evaluates **Inherent Risk Factors (RF)**—such as cash-intensity, anonymity, and settlement finality—and offsets them against institutional **Mitigating Factors (MF)** like transaction limits and mandatory face-to-face onboarding. This results in a granular **Residual Product Risk** score that reflects true institutional exposure.

* **Six-Pillar Weighted Scoring Engine**
    To provide a 360-degree view of the risk profile, the engine executes a simultaneous evaluation across six critical pillars:
    * **Geography**: Macro-jurisdictional exposure.
    * **Product**: Inherent vulnerability of the service utilized.
    * **Channel**: Risk associated with the delivery method (e.g., Non-Face-to-Face vs. Branch).
    * **Identity**: Entity transparency and complexity (e.g., Trusts/PICs vs. Natural Persons).
    * **Behavior**: Deviations in transactional velocity, volume, and value.
    * **KYC Status**: Verification integrity and completeness of due diligence documentation.

* **Deterministic "Hard Override" Guardrails**
    To prevent **Risk Dilution**—a common failure where a critical threat is "averaged out" by low-risk data—the system employs non-dilutable triggers. Detection of a **Sanctions Nexus, Foreign PEP status, Shell Bank indicator, or Opaque Ownership structure** terminates the weighted calculation and forces an immediate **High-Risk (10.0)** classification.

* **Audit Transparency & Explainability**
    Every decision produced by the engine is accompanied by an immutable `override_reason` and provenance metadata. This ensures that every risk rating—whether automated or manually adjusted—is fully auditable, providing the necessary evidence for **SAR/STR filings** and internal/external regulatory examinations.

---

# 🏛️ Regulatory Alignment & Governance

The scoring logic, weighting factors, and override triggers within Global Sentinel are meticulously mapped to internationally recognized AML/CFT standards. This alignment ensures that the framework remains **audit-ready** and provides a defensible methodology during regulatory examinations or independent third-party audits.

* **FATF (Financial Action Task Force): The Global Gold Standard**
    The engine is built on the **FATF Risk-Based Approach (RBA)** and specifically addresses the **40 Recommendations**. Most notably, it operationalizes Recommendation 19 (Higher-Risk Countries) by integrating automated Black and Grey list multipliers. This ensures that the system doesn't just "flag" jurisdictions, but mathematically adjusts risk weights in real-time as FATF designations shift.

* **The Wolfsberg Group: Correspondent Banking & Sanctions Effectiveness**
    Global Sentinel incorporates the **Wolfsberg Anti-Money Laundering Principles**. Our Product Risk Taxonomy specifically weighs "Anonymity" and "Settlement Finality"—key vulnerabilities identified in the Wolfsberg Correspondent Banking Guidance. Furthermore, the engine’s hard-override logic is designed to meet the group’s expectations for **Sanctions Screening Effectiveness**, ensuring zero-tolerance for prohibited counterparty nexus.

* **Basel Institute on Governance: Jurisdictional Health Metrics**
    The framework directly ingests the **Basel AML Index** to evaluate the quality of a country’s AML/CFT framework, the risk of bribery/corruption, and the level of financial transparency. By integrating this index, the engine provides a nuanced view of "Geography Risk" that goes beyond simple Sanctions lists to include systemic institutional risk.

* **Transparency International: Corruption Perception Index (CPI) Normalization**
    To quantify the risk of **bribery and state-level corruption**, the engine normalizes the **Corruption Perception Index (CPI)** into a 1–10 risk scale. This allows the system to accurately identify and elevate the risk levels for customers or entities originating from environments where public sector corruption may facilitate large-scale money laundering.

* **Regional Supervisory Expectations (FinCEN, FCA, MAS, HKMA)**
    While global in scope, the engine’s modular configuration allows for the fine-tuning of thresholds to meet specific local requirements—such as the **US Bank Secrecy Act (BSA)**, the **UK Money Laundering Regulations**, and the **MAS/HKMA technology risk management guidelines**.

---

# 🧩 Intelligence Pillars

## 2. Product & Service Risk Taxonomy

Calculated in **`Product_Risk_Calculator.py`**.

This module quantifies the specific **exploitability of financial instruments and services**. It moves beyond static product classifications by implementing a **net-vulnerability assessment** that balances inherent product risks against the institution's active control environment.

---

### The Net-Risk Equation

The module operates on a **Residual Risk formula**, ensuring that product risk is never evaluated in isolation:

### Residual Product Risk



\[
\text{Residual Product Risk} \;=\; (\text{Inherent Risk Factors}) \;-\; (\text{Mitigating Control Effectiveness})
\]



---

### Inherent Risk Factors (RF)

The engine evaluates **19 distinct risk indicators** to determine how easily a product could be exploited for **money laundering or terrorist financing**.

Key indicators include:

- **Anonymity & Complexity**  
  Determines whether the product enables **non-face-to-face onboarding**, use of **bearer instruments**, or complex ownership structures.

- **Liquidity & Velocity**  
  Measures how quickly value can be transferred and whether the product allows **rapid conversion into cash or other liquid assets**.

- **Cross-Border Reach**  
  Assesses whether the service facilitates **international value transfer**, particularly into **higher-risk jurisdictions**.

---

### Mitigating Factors (MF) & Controls

To prevent inflated risk classifications, the system incorporates **12 internal control layers** designed to reduce product vulnerability.

Examples include:

- **Transactional Thresholds**  
  Hard limits on transaction volume or value that restrict the scale of potential illicit activity.

- **Onboarding Stringency**  
  Enhanced **KYC requirements** or **mandatory in-person verification** for certain high-risk products or services.

- **Monitoring Intensity**  
  The **frequency and depth of automated transaction monitoring** applied to the product’s activity.

---

### Compliance Outcome

By calculating a **granular net-risk score**, the engine allows compliance teams to justify the continued use of inherently high-risk financial services—such as **Trade Finance** or **Correspondent Banking**—by demonstrating that **internal controls effectively reduce the underlying risk to an acceptable level**.

---



## 2. Product & Service Risk Taxonomy

Calculated in **`Product_Risk_Calculator.py`**.

This module quantifies the **exploitability of financial instruments and services**. By moving beyond static product classifications, the engine implements a **net-vulnerability assessment** that balances the inherent dangers of a product against the institution's active control environment.

---

### Risk Matrix Framework

The module operates on a **Residual Risk model**, ensuring that product risk is never evaluated in isolation. It calculates the **delta between potential exposure and existing safeguards**.

### Residual Product Risk Formula



\[
\text{Residual Product Risk} = (\text{Inherent Risk Factors}) - (\text{Mitigating Control Effectiveness})
\]



---

### Inherent Risk Factors (RF)

The engine evaluates **19 distinct indicators** to determine how susceptible a financial product is to **money laundering or terrorist financing**.

Key variables include:

- **Anonymity & Transparency**  
  The degree to which a product allows **non-face-to-face onboarding**, pseudonymous usage, or the use of **bearer instruments**.

- **Liquidity & Velocity**  
  The ease with which assets can be **converted to cash** and the **speed at which funds can be transferred**.

- **Convertibility**  
  The ability to **move value across different asset classes, instruments, or currencies**.

---

### Mitigating Factors (MF)

To prevent overstating risk, the system incorporates **12 internal control layers** that reduce product vulnerability.

Examples include:

- **KYC/CDD Stringency**  
  The depth of **customer documentation and verification** required for a specific product line.

- **Transactional Thresholds**  
  Hard limits on **transaction value or volume** that restrict the scale of potential illicit activity.

- **Monitoring Intensity**  
  The **frequency, automation level, and sophistication** of transaction surveillance applied to the product.

---

### Compliance Outcome

The resulting score represents the **net vulnerability of financial instruments**.  

By calculating a **granular residual score**, the engine enables compliance teams to justify the use of **inherently higher-risk financial services**—such as **Trade Finance** or **Correspondent Banking**—by demonstrating that the institution’s **internal control framework effectively reduces the inherent risk to an acceptable level**.



## 3. Customer & Behavioral Risk Profiling

Managed by **`risk_engine.py`**.

This module serves as the **final integration layer**, synthesizing **identity-based risk indicators** with **real-world activity telemetry**. By evaluating both **how a customer enters the ecosystem** and **how they interact with it**, the engine transitions from static “paper-based” risk assessments to **dynamic behavioral intelligence**.

---

### Critical Risk Vectors

The engine evaluates the customer across **three primary risk lenses** to determine the likelihood of illicit activity.

---

### Politically Exposed Persons (PEP) & Entity Status

The module identifies **high-risk personas**, including:

- **Domestic and Foreign Politically Exposed Persons (PEPs)**
- **Relatives and Close Associates (RCAs)**
- High-risk corporate or institutional affiliations

By assigning **specific weighting to these classifications**, the engine ensures that individuals with elevated **influence or corruption exposure** are subjected to **enhanced monitoring and due diligence controls**.

---

### Onboarding & Delivery Channel Analysis

Risk exposure is significantly influenced by **how the customer relationship is established**.

The engine applies a **risk premium** to **Non-Face-to-Face (Digital/Remote) onboarding** compared to traditional **Face-to-Face interactions**, reflecting:

- Increased **identity verification challenges**
- Higher potential for **synthetic identity fraud**
- Reduced reliability of **document-based verification**

---

### Transactional Intensity & Velocity Patterns

This sub-module analyzes the **financial activity profile** of the customer to identify behavioral anomalies.

Key signals include:

- **Velocity**  
  Rapid movement of funds **in and out of accounts** without a clear economic purpose.

- **Intensity**  
  High volumes of **cash-equivalent transactions**, frequent transfers, or **repeated transactions near regulatory reporting thresholds**.

These patterns may indicate typologies such as:

- **Structuring**
- **Smurfing**
- Rapid value cycling across accounts.

---

### Final Risk Classification

The culmination of this analysis results in the assignment of the **Final Customer Risk Category**:

- **Low Risk**
- **Medium Risk**
- **High Risk**

This classification determines:

- The **frequency of the Periodic Review Cycle**
- The **level of Enhanced Due Diligence (EDD)** required
- The ongoing monitoring intensity needed to maintain the relationship within the institution’s **risk appetite framework**.




# ⚙️ Scoring Methodology

The final **Residual Risk Score** is derived from two distinct logic layers.

---

## Weighted Base Score

Six core pillars are evaluated using weighted scoring:

* **Geography** — weight 1.4
* **Product** — weight 1.2
* **Behavior** — weight 1.5
* **Identity / Customer Type** — weight 1.0
* **KYC Control Strength** — weight 1.1
* **Channel Risk** — weight 0.8

---

## Hard Overrides (Non-Dilutable)

If a record satisfies an override condition (for example `media_status == "Sanctions"`), the system **forces the score to 10.0**, bypassing the weighted scoring mechanism.

This ensures **critical compliance risks cannot be diluted by statistical averaging**.

---

# 📂 Project Layout

```text
.
├── Data/
│   ├── Table1_Core_Customer_Data.csv       # PII & Demographics (200k rows)
│   ├── Table2_Account_Product_Data.csv     # Relational Product Map (1.1M rows)
│   ├── Table3_Transactional_Summary.csv    # Behavioral Patterns
│   ├── Table4_Compliance_Screening.csv     # PEP / Sanctions / Media Flags
│   ├── Countries.json                      # Master Country List
│   ├── Product_Risk_Factors.json           # RF/MF Weighting Logic
│   └── FATF_Lists.json                     # Black / Grey List Source
├── Country_Risk_Rating.py                  # Geography Risk Orchestrator
├── Product_Risk_Calculator.py              # Product Vulnerability Scorer
├── generate_table1.py                      # Synthetic Customer Generator
├── generate_table2.py                      # Relational Account Generator
└── risk_engine.py                          # Master Scoring & Override Engine
```

---

# ⚡ Quick Start

## 1. Installation

```bash
git clone https://github.com/YOUR_USERNAME/Global-Sentinel.git
cd Global-Sentinel
pip install pandas numpy
```

---

## 2. Execute Data Pipeline

```bash
# Generate the synthetic environment
python generate_table1.py
python Product_Risk_Calculator.py
python generate_table2.py

# Run the final risk assessment
python risk_engine.py
```

---

## 3. Review Results

The final classifications are exported to:

```
Data/Final_Customer_Risk_Rating.csv
```

Each record includes the **specific `override_reason` field**, enabling **full audit transparency and traceability**.

---

# ⚖️ License & Disclaimer

Distributed under the **Apache License 2.0**.

⚠️ **Disclaimer:** This framework uses synthetic data and is intended for **RegTech architectural modeling and experimentation**. It does not constitute legal, regulatory, or compliance advice and must be adapted to applicable jurisdictional requirements before production deployment.
