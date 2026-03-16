# 🛡️ Global Sentinel — Multi‑Tiered AML/CFT Risk & Intelligence Framework

**Global Sentinel** is a production‑grade, enterprise‑oriented AML/CFT intelligence stack that delivers deterministic and probabilistic risk scoring across **Customer**, **Product**, and **Country** domains. Built as a modular, data‑centric rating engine, it fuses regulatory best practice with high‑throughput data engineering to automate KYC/KYB, sanctions screening, adverse‑media detection, and enhanced due diligence (EDD) workflows at scale.

---

## 🚀 Executive Summary

Global Sentinel ingests heterogeneous regulatory and operational feeds, normalizes them into structured risk matrices, and executes a multi‑pillar scoring pipeline that produces explainable, auditable **Residual Risk** outputs for downstream case management and SAR filing. 

The system is optimized for high-cardinality datasets (200k+ customer profiles; 1.1M+ product nodes) and supports real‑time and batch evaluation modes for transaction monitoring, onboarding, and periodic reviews.

### **Core Capabilities**
* **End‑to‑end KYC/KYB lifecycle orchestration** * **Deterministic sanctions & PEP screening** with fuzzy and tokenized matching logic.
* **Source of Wealth (SoW) & Source of Funds (SoF)** validation logic and evidence scoring.
* **Product risk taxonomy & Country risk fusion** for composite residual risk calculation.
* **Audit‑first design**: Immutable decision metadata, `override_reason`, and EDD trails.

---

## 🏛️ Regulatory Alignment & Standards

Scoring logic, controls, and governance are engineered to align with global AML/CFT frameworks and major supervisory expectations:

### **Global Standard‑Setters**
* **FATF** — Risk‑Based Approach and 40 Recommendations.
* **Wolfsberg Group** — AML & sanctions screening principles; Correspondent Banking Guidance.
* **JMLSG** — UK sector guidance and typologies.
* **EU AML Directives (including 6AMLD)** — UBO transparency and cross‑border controls.

### **Major Supervisory Markets & Regulators**
* **FinCEN (USA)** — SAR/CTR expectations and beneficial ownership rules.
* **FCA (UK)** — Conduct and AML supervision expectations.
* **MAS (Singapore)** — Technology and transaction monitoring guidance.
* **HKMA (Hong Kong)** — Cross‑border and correspondent banking controls.
* **AUSTRAC (Australia)** — Reporting and threshold rules.
* **BaFin (Germany) & FINMA (Switzerland)** — Prudential AML expectations.

---

## 🧩 Intelligence Pillars (Customer, Product, Country)

### 1. Customer Risk Rating (Comprehensive)
* **Identity & Ownership**: Deterministic UBO resolution, nominee detection, trust settlor/beneficiary mapping, and bearer‑instrument flags.
* **PEP & RCA Handling**: Tiered PEP scoring, RCA propagation, time‑since‑office decay functions, and relationship graph analytics.
* **Behavioral Profiling**: Baseline expected activity, velocity/pattern detection, and smurfing heuristics.
* **Screening & OSINT**: Sanctions/watchlist matching and adverse media scoring.

### 2. Product & Service Risk Taxonomy
* **Multi‑dimensional scoring** across Liquidity, Anonymity, Convertibility, Cross‑Border Exposure, and Settlement Finality.
* **High‑risk product examples**: Correspondent banking, trade finance, crypto on/off ramps, and high‑value goods settlement.

### 3. Macro‑Jurisdictional Assessment
* **Data fusion** of CPI, Basel AML Index, FATF listings, and sanctions regimes.
* **Normalization & scaling** to produce an Inherent Geography Risk Score (1–10) with event‑driven updates (e.g., greylist changes).

---

## ⚙️ Scoring Methodology

* **Three‑pillar composite**: Geography × Behavior × Product with precision multipliers.
* **Residual Risk** = `WeightedAggregate(GeographyScore, BehaviorScore, ProductScore) + Hard-coded Overrides`.
* **Hard Overrides**: Sanctions hits, confirmed foreign PEPs, shell bank flags, and opaque UBOs trigger immediate **High-Risk** classification.
* **Evidence scoring**: Each risk attribute carries provenance metadata (source, timestamp, confidence) to support regulatory challenge.

---

## 🛠️ Architecture & Data Engineering

* **Modular Separation**: JSON rating matrices and rulebooks decoupled from execution logic for runtime reconfiguration.
* **Vectorized Data Processing**: Bulk joins and transforms implemented with optimized **Pandas/NumPy** DataFrame operations for columnar performance.
* **Scalability Patterns**: Parallel batch workers and idempotent processing for replays and backfills.
* **Observability**: Lineage and audit logs for every decision and override.

---

## 📂 Project Layout
```text
.
├── Data/
│   ├── Table1_Core_Customer_Data.csv       # Demographics & PII
│   ├── Table2_Account_Product_Data.csv      # Relational Product Nodes
│   ├── Table3_Transactional_Summary.csv     # Behavioral Patterns
│   ├── Table4_Compliance_Screening.csv      # PEP/Sanctions Hits
│   ├── Country_Risk_Rating.json            # Geography Risk Matrix
│   ├── Product_Risk_Rating.json            # Product Risk Taxonomy
│   └── Basel_Index.json / FATF_Lists.json  # Regulatory Feeds
├── Country_Risk_Rating.py                  # Geography Orchestrator
├── Product_Risk_Calculator.py               # Product Vulnerability Scorer
└── risk_engine.py                          # Master Residual Risk Engine
```

## ⚡ Quick Start

### 1. Installation
```bash
git clone [https://github.com/YOUR_USERNAME/Global-Sentinel.git](https://github.com/YOUR_USERNAME/Global-Sentinel.git)
cd Global-Sentinel
pip install -r requirements.txt
```

### 2. Execution
```bash
# Execute the full rating cycle
python risk_engine.py
```


### 3. Configuration
Tune Logic: Edit Product_Risk_Rating.json and Country_Risk_Rating.json to adjust weights and thresholds without modifying core Python code.

## 🧾 Compliance & Auditability
Global Sentinel is designed to be regulator‑ready. The system supports defensible decisioning for:

* Onboarding & KYC/KYB

* Periodic Review Cycle

* Transaction Monitoring (TM)

* Suspicious Activity Reporting (SAR)

## ⚖️ License & Disclaimer
Distributed under the Apache License 2.0.

> **⚠️ Disclaimer:** *This repository is a demonstration of RegTech engineering using synthetic data. It is not legal advice and must be adapted to local laws, supervisory guidance, and internal risk appetite before production deployment.*
