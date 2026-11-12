<div align="center">

# 💻 LapPick

### Find the right laptop with data, not guesswork.

**An interactive laptop discovery, recommendation, and comparison application powered by live product listings.**

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" />
  <img src="https://img.shields.io/badge/REST_API-2C7A7B?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Recommendation_System-8E44AD?style=for-the-badge" />
</p>

<a href="https://laptop-price-and-recommendation-system-icvhjjspmfrmmy2rfmtuaq.streamlit.app/">
  <img src="https://img.shields.io/badge/🚀_EXPLORE_LIVE_DEMO-7C3AED?style=for-the-badge&logo=streamlit&logoColor=white" />
</a>

</div>

---

## About the Project

LapPick is a Python-based laptop discovery and recommendation application designed to simplify laptop purchasing decisions.

It retrieves current product listings from Croma through the API.SH API, processes technical specifications, and helps users identify suitable laptops based on their budget, intended usage, and hardware requirements.

Instead of manually comparing multiple product listings, users can explore recommendations, filter available products, discover similar laptops, and compare shortlisted options in one place.

## Key Features

- **Personalised Recommendations:** Find suitable laptops based on budget, usage, RAM, storage, and hardware preferences.
- **Live Product Discovery:** Fetch current laptop listings from Croma through API integration.
- **Smart Filtering:** Filter laptops by brand, price, specifications, and other available product details.
- **Usage-Based Matching:** Evaluate laptops for student work, coding, gaming, creative tasks, and business use.
- **Laptop Comparison:** Compare up to four shortlisted laptops side by side.
- **Similar Laptop Discovery:** Identify comparable products using cosine similarity.
- **Product Insights:** Explore prices, discounts, ratings, processors, and available specifications.
- **CSV Export:** Download product data for further analysis.

## How It Works

| Stage | Process | Description |
|---|---|---|
| 1 | Data Retrieval | Fetch current laptop listings through the API.SH Croma API. |
| 2 | Data Processing | Clean, normalise, and organise product information using Pandas. |
| 3 | Requirement Matching | Evaluate products against user preferences and hardware requirements. |
| 4 | Recommendation Ranking | Rank suitable laptops using a weighted scoring approach. |
| 5 | Similarity Analysis | Apply cosine similarity to identify laptops with comparable specifications. |
| 6 | Comparison | Present shortlisted products side by side for easier decision-making. |

## Recommendation Methodology

LapPick uses a **weighted, rule-based recommendation approach** to identify laptops that best match user requirements.

The ranking process considers:

- Budget compatibility
- Intended usage
- Processor capabilities
- RAM and storage
- Dedicated GPU availability
- Screen specifications
- Other available product attributes

For similar product discovery, cosine similarity is applied to numerical product specification vectors.

The recommendation scores are calculated from product attributes and user preferences; they are not predictions from a separately trained machine learning model.

## Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Application Framework | Streamlit |
| Data Processing | Pandas, NumPy |
| Recommendation Logic | Weighted Scoring |
| Similarity Analysis | Cosine Similarity |
| API Integration | API.SH – Croma API |
| Data Export | CSV |
| Version Control | Git, GitHub |

## API Integration

LapPick retrieves product listings using the third-party API.SH Croma API.

| API Detail | Configuration |
|---|---|
| Provider | API.SH |
| Endpoint | `GET https://api.api.sh/croma/v1/search` |
| Authentication | `x-api-key` |
| Search Parameter | `q` |
| Additional Parameters | `page`, `sort` |

API documentation: https://api.sh/croma-api

**Important:** This is a third-party API that retrieves data from public Croma product listings. It is not an official Croma developer API.

API availability, pricing, request quotas, and free credits may change. Refer to the provider's documentation for current limits.

## Project Structure

```text
lappick/
│
├── app.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
├── config.toml
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

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/mathan-ponraj/lappick.git
cd lappick
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the API key

Create a `.env` file in the project root using `.env.example` as a template.

Add your API key:

```env
APISH_KEY=your_actual_api_key
```

Keep your actual API key private. Never upload your `.env` file to GitHub.

### 5. Launch the application

```bash
streamlit run app.py
```

## Data Limitations

- Product prices, discounts, ratings, and availability can change.
- Product listings may not contain every technical specification.
- Recommendations depend on the quality and completeness of the retrieved product information.
- Results represent the listings retrieved at the time of the API request, not guaranteed inventory or offers.

## Future Enhancements

- Historical laptop price tracking.
- PostgreSQL integration for product data management.
- FastAPI backend architecture.
- Recommendation explainability using SHAP where applicable.
- Automated data refresh and monitoring.
- Docker-based deployment and CI/CD integration.

## Developer

<div align="center">

### Mathan Ponraj

**M.E. Computer Science | Python | Data Science | AI & Software Development**

<a href="https://github.com/mathan-ponraj">
  <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" />
</a>
<a href="https://www.linkedin.com/in/mathan03/">
  <img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" />
</a>

*Building practical software solutions through data and technology.*

</div>
