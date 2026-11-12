# LaptopIQ — India Live Laptop Intelligence

A compact portfolio project that fetches current laptop listings from Croma through API.SH, normalizes the results with Pandas, summarizes listed prices, filters by brand, and exports CSV data.

## API details

- Provider: API.SH Croma API
- Endpoint: `GET https://api.api.sh/croma/v1/search`
- Authentication header: `x-api-key`
- Search parameter: `q` (for example, `laptop`)
- Other parameters used: `page`, `sort`
- API documentation: https://api.sh/croma-api

The API.SH page currently advertises 1,000 free credits per month for new accounts. Each Croma search request costs one credit according to its current documentation. Check the provider's pricing page before relying on the free allowance, because plans and quotas can change.

This is a third-party API that returns data from public Croma product pages. It is not an official Croma developer API.

## 1. Set up in VS Code

Open this project folder in VS Code, then run these commands in the terminal one at a time:

```powershell
python -m venv .venv
```

```powershell
.venv\Scripts\Activate.ps1
```

```powershell
pip install -r requirements.txt
```

## 2. Add your API key

Copy `.env.example` and rename the copy to `.env`.

Open `.env` and replace the placeholder:

```env
APISH_KEY=your_real_api_key
```

Do not add quotation marks. Never upload `.env` to GitHub.

## 3. Run LaptopIQ

```powershell
streamlit run app.py
```

Enter a search term such as `laptop`, `gaming laptop`, or `HP laptop`, choose a page and sort order, then select **Fetch latest listings**.

## Project structure

```text
LaptopIQ_India_Live_API/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── src/
│   ├── __init__.py
│   ├── croma_client.py
│   └── data_utils.py
├── data/
│   └── .gitkeep
└── model/
    └── .gitkeep
```

## Notes about your existing XGBoost model

This API integration is intentionally kept separate from your historical ML training dataset. Croma search listings do not guarantee the same feature columns or a comparable `Rating` target as your original training CSV. Do not feed the live listings directly into the existing XGBoost model until the fields have been mapped and validated.

Keep your original `data/data.csv` and trained model files in a backup. This package does not contain your private dataset or trained model because those files were not attached to this chat.

## Data limitations

- Prices, discounts, stock and ratings can change.
- Search results may omit detailed processor/RAM/storage fields; the API's product-detail endpoint can be integrated later if needed.
- Treat the results as a current snapshot, not a guaranteed inventory or offer.
- Check API.SH terms, current quota and Croma's applicable terms before public/commercial use.
<div align="center">

# 💻 LapPick

### Find the right laptop with data, not guesswork.

**A live laptop discovery and recommendation platform built for smarter buying decisions.**

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/API_Integration-2C7A7B?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Recommendation_System-8E44AD?style=for-the-badge" />
</p>

<a href="https://laptop-price-and-recommendation-system-icvhjjspmfrmmy2rfmtuaq.streamlit.app/">
  <img src="https://img.shields.io/badge/🚀_EXPLORE_LIVE_DEMO-7C3AED?style=for-the-badge&logo=streamlit&logoColor=white" />
</a>

</div>

---

## About LapPick

LapPick is a laptop discovery and recommendation platform that helps users find suitable laptops based on their budget, usage, and technical requirements.

It retrieves laptop listings from Croma through the API.SH API, processes product specifications, and ranks suitable options using a weighted recommendation approach.

The goal is simple: make laptop research easier by bringing product discovery, personalised recommendations, and side-by-side comparisons into one application.

## Key Features

- **Personalised Recommendations:** Find laptops based on budget, usage, RAM, storage, and brand preferences.
- **Live Product Listings:** Retrieve laptop product information through API integration.
- **Smart Filtering:** Filter products using price, specifications, keywords, and hardware requirements.
- **Laptop Comparison:** Compare up to four shortlisted laptops side by side.
- **Similar Product Discovery:** Identify similar laptops using cosine similarity on product specifications.
- **Product Insights:** View pricing, discounts, ratings, processor details, and other available specifications.
- **CSV Export:** Download laptop listing data for further analysis.

## How It Works

| Step | Process | Description |
|---|---|---|
| 1 | Data Retrieval | Fetch laptop listings through the Croma API provided by API.SH. |
| 2 | Data Processing | Extract and organise product details and technical specifications. |
| 3 | Requirement Matching | Apply user preferences such as budget, usage, RAM, and storage. |
| 4 | Recommendation Ranking | Rank suitable laptops using weighted scoring. |
| 5 | Similarity Analysis | Use cosine similarity to identify laptops with comparable specifications. |
| 6 | Product Comparison | Compare shortlisted products to support purchasing decisions. |

## Recommendation Approach

LapPick uses a **weighted, rule-based recommendation system** to rank laptops according to user requirements.

The recommendation process considers factors such as:

- Budget compatibility
- Intended usage
- Processor and GPU specifications
- RAM and storage
- Screen size and available product details

For similar laptop discovery, cosine similarity is applied to product specification vectors.

## Technology Stack

| Category | Technologies |
|---|---|
| Programming | Python |
| Application | Streamlit |
| Data Processing | Pandas, NumPy |
| Recommendation | Weighted Scoring, Cosine Similarity |
| API Integration | API.SH – Croma API |
| Data Export | CSV |
| Version Control | Git, GitHub |

## Skills Demonstrated

- Python Application Development
- REST API Integration
- Data Extraction and Processing
- Recommendation System Development
- Product Data Analysis
- Similarity Analysis
- Interactive Application Development
- Data-Driven Decision Support

## Future Enhancements

- SHAP-based recommendation explainability.
- PostgreSQL integration for product data management.
- FastAPI backend development.
- Automated data refresh and historical price tracking.
- MLflow for experiment tracking.
- Docker and CI/CD deployment.

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/mathan-ponraj/Laptop-Price-And-Recommendation-System.git
cd Laptop-Price-And-Recommendation-System
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the API key

Create a `.env` file in the project root:

```env
APISH_KEY=your_api_key
```

Replace `your_api_key` with your API.SH key.

**Important:** Keep your actual API key private. Never commit your `.env` file to GitHub.

### 4. Run the application

```bash
streamlit run app.py
```

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
