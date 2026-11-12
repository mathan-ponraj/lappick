<div align="center">

# LapPick
### Live Laptop Data Intelligence & Analytical Decision System

**A Python-based system for live product data acquisition, feature engineering, weighted analytical evaluation, and specification similarity analysis.**

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

LapPick is a data-driven application developed to transform live laptop product listings into structured and analytically comparable information.

The system retrieves product data from Croma through the third-party API.SH service, processes product descriptions, extracts hardware specifications, and constructs numerical feature representations. These features are evaluated against user-defined requirements using weighted scoring, while cosine similarity identifies products with comparable specifications.

The application integrates data acquisition, preprocessing, feature engineering, analytical scoring, and interactive visualisation into a unified workflow using Python and Streamlit.

## 2. Problem Statement

Laptop product information is distributed across multiple listings, often containing inconsistent descriptions, varying technical specifications, and changing prices.

Manually evaluating these products makes it difficult to compare hardware configurations and determine which options satisfy specific requirements.

LapPick addresses this problem by establishing an automated data-processing and analytical workflow that converts retrieved product information into structured attributes and supports systematic product evaluation.

## 3. Project Objectives

- Retrieve current laptop listings through REST API integration.
- Extract structured hardware attributes from product descriptions.
- Perform data cleaning, normalisation, and feature engineering.
- Develop usage-dependent analytical scoring.
- Apply constraint-based filtering to product datasets.
- Calculate cosine similarity between numerical product representations.
- Generate interpretable explanations for analytical results.
- Provide interactive comparison and downloadable datasets.

## 4. System Architecture & Methodology

| Stage | Component | Implementation |
|---|---|---|
| 01 | Data Acquisition | API integration using Python Requests |
| 02 | Data Extraction | Product names, highlights, prices and ratings |
| 03 | Data Preprocessing | Pandas-based cleaning and normalisation |
| 04 | Feature Engineering | Hardware specification extraction |
| 05 | Feature Representation | Numerical product feature vectors |
| 06 | Constraint Evaluation | Budget and hardware requirement filtering |
| 07 | Analytical Evaluation | Usage-dependent weighted scoring |
| 08 | Similarity Computation | Cosine similarity using NumPy |
| 09 | Result Interpretation | Feature contribution-based explanations |
| 10 | Application Layer | Interactive Streamlit interface |

### 4.1 Data Acquisition

Product listings are retrieved through the API.SH Croma API using HTTP GET requests.

The integration supports search queries, pagination, and sorting parameters. Retrieved product information is passed to the preprocessing module for further analysis.

### 4.2 Data Preprocessing

Pandas is used to organise and normalise the retrieved product records.

Product names and highlights are combined to extract available technical information. Numerical attributes are converted into appropriate data types, while missing or unavailable values are handled during feature construction.

### 4.3 Feature Engineering

The system derives the following analytical attributes:

| Feature | Description |
|---|---|
| CPU Tier | Processor performance classification (1–5) |
| RAM | Extracted memory capacity in GB |
| Storage | Extracted storage capacity in GB |
| GPU | Dedicated graphics availability |
| Gaming | Gaming-oriented product classification |
| Screen Size | Display size in inches |
| Portability | Screen-size-based portability score |
| Rating | Normalised customer rating |
| Price Value | Budget-relative price score |
| Touchscreen | Touchscreen availability |

### 4.4 Usage-Based Feature Weighting

Five usage profiles define the relative importance of each feature.

| Feature | Student | Coding & ML | Gaming | Creative | Business |
|---|---:|---:|---:|---:|---:|
| CPU Performance | 0.15 | 0.28 | 0.25 | 0.25 | 0.15 |
| RAM | 0.15 | 0.30 | 0.10 | 0.20 | 0.10 |
| Storage | 0.10 | 0.10 | 0.05 | 0.15 | 0.10 |
| GPU | 0.00 | 0.12 | 0.40 | 0.15 | 0.00 |
| Portability | 0.25 | 0.05 | 0.00 | 0.05 | 0.35 |
| Rating | 0.10 | 0.05 | 0.05 | 0.05 | 0.10 |
| Price Value | 0.25 | 0.10 | 0.15 | 0.15 | 0.20 |

Each profile has weights that sum to 1.0.

### 4.5 Weighted Analytical Scoring

Normalised product features are combined using a weighted scoring function:

\[
S(x) = \sum_{i=1}^{n} w_i f_i(x)
\]

Where:

- \(S(x)\): Overall product score.
- \(w_i\): Importance weight assigned to feature \(i\).
- \(f_i(x)\): Normalised feature value.
- \(n\): Number of evaluated features.

The calculated score is converted into a percentage-based match score.

Optional keyword matches contribute an additional scoring adjustment.

### 4.6 Constraint-Based Evaluation

Before ranking, products are filtered according to mandatory requirements:

- Maximum budget.
- Minimum RAM capacity.
- Minimum storage capacity.
- Dedicated GPU requirement.
- Touchscreen requirement.
- Brand preferences.

Products that fail the specified hard constraints are excluded from the eligible results.

### 4.7 Similarity Analysis

Cosine similarity is applied to numerical product feature vectors to identify laptops with comparable specifications.

\[
\operatorname{Similarity}(A,B) =
\frac{A \cdot B}{\|A\|\|B\|}
\]

The implementation uses NumPy matrix operations to calculate similarity. Price is included as a feature, while rating and budget-relative value are excluded from this comparison.

### 4.8 Explainable Analytical Results

The system identifies the highest-contributing features for each evaluated product.

It generates up to three human-readable explanations based on attributes such as processor performance, memory capacity, storage, graphics, ratings, and price compatibility.

This provides additional context behind the calculated match score.

## 5. Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| API Communication | Requests, REST API |
| Data Processing | Pandas, NumPy |
| Feature Engineering | Python, Regular Expressions |
| Analytical Scoring | Weighted Attribute Evaluation |
| Similarity Analysis | Cosine Similarity, NumPy |
| Application Framework | Streamlit |
| Data Export | CSV |
| Version Control | Git, GitHub |

## 6. Application Modules

| File | Responsibility |
|---|---|
| `app.py` | Application interface and workflow management |
| `src/croma_client.py` | External API communication and product retrieval |
| `src/data_utils.py` | Product normalisation and data persistence |
| `src/recommender.py` | Specification parsing, feature engineering, scoring and similarity analysis |

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

## 7. Implementation Results & Limitations

### Implemented Capabilities

- Live retrieval of laptop listings through API integration.
- Automated extraction of available hardware specifications.
- Numerical feature construction for product evaluation.
- Five usage profiles with different feature weight configurations.
- Constraint-based filtering and weighted analytical scoring.
- Cosine similarity for comparable product identification.
- Feature-based explanations for evaluated results.
- Interactive product comparison and CSV export.

### Limitations

1. Product availability depends on the external API provider.
2. Product descriptions may contain incomplete or inconsistent specifications.
3. CPU tiers are heuristic classifications rather than benchmark measurements.
4. Missing numerical specifications are handled using predefined fallback values in feature construction.
5. Weighted scores are analytical match indicators, not measured purchasing success probabilities.
6. The current implementation does not contain a separately trained predictive machine learning model.

## 8. Installation & Execution

**Prerequisites:** Python 3.10+ and a valid API.SH API key.

### Step 1 — Clone the repository

```bash
git clone https://github.com/mathan-ponraj/lappick.git
cd lappick
```

### Step 2 — Create a virtual environment

```powershell
python -m venv .venv
```

Activate on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Configure API credentials

Create a `.env` file in the project root using `.env.example` as a template.

```env
APISH_KEY=your_actual_api_key
```

For Streamlit Community Cloud, configure `APISH_KEY` through the application's Secrets settings.

**Security:** Never commit your actual API key or `.env` file to GitHub.

### Step 5 — Launch the application

```bash
streamlit run app.py
```

## 9. External Data Source & References

| Reference | Details |
|---|---|
| Product Data Provider | API.SH – Croma API |
| Endpoint | `GET https://api.api.sh/croma/v1/search` |
| Authentication Header | `x-api-key` |
| Search Parameter | `q` |
| Additional Parameters | `page`, `sort` |
| Documentation | https://api.sh/croma-api |

The integration uses a third-party API that retrieves information from public Croma product listings. It is not an official Croma developer API.

Product prices, discounts, ratings, and availability may change. Verify information with the retailer before purchasing.

---

<div align="center">

**Developed by Mathan Ponraj**


[GitHub](https://github.com/mathan-ponraj) · [LinkedIn](https://www.linkedin.com/in/mathan03/) · [Portfolio](https://mathan-portfolio-ten.vercel.app/)

</div>
