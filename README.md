<div align="center">

# LapPick
### Live Laptop Data Intelligence & Decision-Support System

**A Python-based application for real-time product data acquisition, specification analysis, and data-driven laptop evaluation.**

<br>

<a href="https://laptop-price-and-recommendation-system-icvhjjspmfrmmy2rfmtuaq.streamlit.app/">
  <img src="https://img.shields.io/badge/▶_LIVE_APPLICATION-2563EB?style=for-the-badge&logo=streamlit&logoColor=white" />
</a>
<a href="https://github.com/mathan-ponraj/lappick">
  <img src="https://img.shields.io/badge/SOURCE_CODE-181717?style=for-the-badge&logo=github&logoColor=white" />
</a>

</div>

---

## 1. Abstract

LapPick is a live product data intelligence application developed to simplify the evaluation of laptop products using current market listings. The system retrieves product information from Croma through the third-party API.SH service, processes unstructured product specifications, and transforms the retrieved information into structured data for analysis.

It evaluates product attributes against user-defined constraints using weighted scoring and applies cosine similarity to identify products with comparable specifications. The application provides interactive filtering, product comparison, analytical summaries, and CSV export through a Streamlit interface.

## 2. Problem Statement

Laptop specifications and prices are distributed across numerous product listings, making systematic product evaluation difficult. Product descriptions may also contain inconsistent or incomplete technical information.

The objective of LapPick is to establish a structured data-processing workflow that converts retrieved product listings into comparable product records and supports data-driven purchasing decisions.

## 3. System Objectives

- Acquire current laptop product listings through REST API integration.
- Extract and standardise technical specifications from product descriptions.
- Transform retrieved records into a structured analytical dataset.
- Evaluate products against budget and hardware constraints.
- Implement weighted attribute scoring for usage-based evaluation.
- Apply cosine similarity for product specification analysis.
- Provide interactive comparison, filtering, and CSV data export.

## 4. System Architecture & Methodology

| Stage | Module | Implementation |
|---|---|---|
| 01 | Data Acquisition | API requests to API.SH Croma endpoint |
| 02 | Data Extraction | Retrieval of product descriptions, prices and attributes |
| 03 | Data Preprocessing | Cleaning, normalisation and specification parsing |
| 04 | Feature Engineering | Extraction of RAM, storage, processor, GPU and screen attributes |
| 05 | Constraint Evaluation | Budget and mandatory specification filtering |
| 06 | Analytical Scoring | Weighted evaluation of product attributes |
| 07 | Similarity Computation | Cosine similarity on numerical specification vectors |
| 08 | Presentation | Interactive Streamlit interface and CSV export |

### Analytical Methodology

**A. Data Acquisition and Preprocessing**

Product listings are retrieved through the API endpoint. Pandas is used to organise and process the returned records. Technical attributes are extracted from available product information and normalised for downstream processing.

**B. Feature Engineering**

Product descriptions are parsed to derive structured attributes, including:

- Processor tier
- RAM capacity
- Storage capacity
- Graphics capability
- Screen specifications
- Product price and rating, when available

**C. Weighted Attribute Evaluation**

Products are evaluated against user requirements using a weighted scoring approach. Attribute importance varies according to the selected usage profile.

Budget and mandatory hardware requirements are applied as constraints before ranking eligible products.

**D. Similarity Analysis**

Cosine similarity is applied to numerical product specification vectors to identify products with comparable hardware configurations.

**E. Analytical Presentation**

Processed records are presented through interactive filters, comparison views, pricing information, and downloadable CSV datasets.

## 5. Technology Stack

| Layer | Technologies |
|---|---|
| Programming | Python |
| API Integration | Requests, REST API |
| Data Processing | Pandas, NumPy |
| Feature Extraction | Python-based specification parsing |
| Analytical Methods | Weighted Scoring, Cosine Similarity |
| Application Interface | Streamlit |
| Data Storage / Export | CSV |
| External Data Provider | API.SH – Croma API |

## 6. Application Modules

| Module | Responsibility |
|---|---|
| `croma_client.py` | API communication and laptop listing retrieval |
| `data_utils.py` | Product data normalisation and CSV handling |
| `recommender.py` | Specification parsing, weighted evaluation and similarity calculations |
| `app.py` | Application workflow, user inputs, analytical views and product comparison |

### Repository Structure

```text
lappick/
│
├── app.py
├── requirements.txt
├── README.md
├── config.toml
├── .env.example
├── .gitignore
│
├── src/
│   ├── __init__.py
│   ├── croma_client.py
│   ├── data_utils.py
│   └── recommender.py
│
├── data/
│   └── .gitkeep
│
└── model/
    └── .gitkeep
```

## 7. Results & System Limitations

The implemented application provides:

- Live retrieval of laptop listings through an external API.
- Structured product information for interactive analysis.
- Usage-dependent evaluation of available products.
- Similarity-based identification of comparable specifications.
- Side-by-side comparison of up to four shortlisted products.
- CSV export for independent analysis.

**Limitations:**

1. Data availability depends on the external API provider.
2. Product descriptions may contain incomplete or inconsistent specifications.
3. Prices, discounts, ratings, and availability are time-dependent.
4. Analytical results depend on the quality of extracted product attributes.
5. The current implementation uses weighted scoring and cosine similarity; it does not include a separately trained predictive ML model.

## 8. Installation & Execution

**Prerequisites:** Python 3.10+ and an API.SH account with an available API key.

**Step 1 — Clone the repository**

```bash
git clone https://github.com/mathan-ponraj/lappick.git
cd lappick
```

**Step 2 — Create and activate a virtual environment**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Step 3 — Install dependencies**

```bash
pip install -r requirements.txt
```

**Step 4 — Configure API credentials**

Create a `.env` file in the root directory:

```env
APISH_KEY=your_actual_api_key
```

For Streamlit Community Cloud, configure the same credential through the application's Secrets settings.

**Step 5 — Execute the application**

```bash
streamlit run app.py
```

## 9. Data Source & References

- **Product Data Provider:** API.SH – Croma API
- **API Endpoint:** `GET https://api.api.sh/croma/v1/search`
- **Authentication:** `x-api-key`
- **API Documentation:** https://api.sh/croma-api
- **Similarity Method:** Cosine Similarity

The API is a third-party integration that retrieves information from public Croma product listings. It is not an official Croma developer API. Users should verify product information with the retailer before making purchasing decisions.

---

<div align="center">

**Developed by Mathan Ponraj**

M.E. Computer Science & Engineering · 2026

[GitHub](https://github.com/mathan-ponraj) · [LinkedIn](https://www.linkedin.com/in/mathan03/) · [Portfolio](https://mathan-portfolio-ten.vercel.app/)

</div>
