# LapPick

Live laptop data. Smarter decisions. A Python app that pulls live laptop listings, extracts specs, and ranks laptops for different uses.

[![Live Demo](https://img.shields.io/badge/LIVE%20DEMO-Try%20LapPick-6366f1?style=for-the-badge&logo=streamlit&logoColor=white)](https://laptop-price-and-recommendation-system-icvhjjspmfrmmy2rfmtuaq.streamlit.app/)

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)

---

## Problem Statement

Laptop prices and specs change constantly, and listings describe the same hardware in different ways. This makes it hard for buyers to compare laptops and find the ones that fit their needs and budget.

## What I Built

In this project, I used the API.SH Croma API to pull live laptop listings and extracted CPU, RAM, storage, GPU, and display specs from product descriptions. I then ranked laptops with usage-based weighted scoring, constraint filters, and cosine similarity. I built the app with Python and Streamlit.

## Key Features

- Pulls live laptop listings through a REST API.
- Extracts hardware specs from product names and highlights.
- Scores laptops for five uses: Student, Coding and ML, Gaming, Creative, and Business.
- Filters laptops by budget, RAM, storage, GPU, touchscreen, and brand.
- Finds laptops with similar specs using cosine similarity.
- Explains each result with up to three top-scoring features.
- Lets users compare laptops and download the data as CSV.

## Tech Stack

| Area                | Tools                                    |
| ------------------- | ---------------------------------------- |
| Language            | Python                                   |
| API communication   | Requests, REST API                       |
| Data processing     | Pandas, NumPy                            |
| Feature engineering | Python, regular expressions              |
| Scoring             | Usage-based weighted scoring             |
| Similarity          | Cosine similarity with NumPy             |
| Application         | Streamlit                                |
| Data export         | CSV                                      |
| Version control     | Git, GitHub                              |

## Project Structure

```text
lappick/
│
├── app.py                  # Streamlit interface and workflow
├── requirements.txt        # Python dependencies
├── config.toml             # App configuration
├── .env.example            # Template for the API key
├── .gitignore              # Files Git should ignore
│
├── src/
│   ├── __init__.py         # Marks src as a package
│   ├── croma_client.py     # Calls the API and retrieves listings
│   ├── data_utils.py       # Cleans listings and saves data
│   └── recommender.py      # Spec parsing, features, scoring, similarity
│
├── data/                   # Saved data files
│   └── .gitkeep
│
├── model/                  # Placeholder folder
│   └── .gitkeep
│
└── README.md               # Project documentation
```

## Data

- **Source:** API.SH Croma API, a third-party service that reads public Croma product listings. It is not an official Croma API.
- **Endpoint:** `GET https://api.api.sh/croma/v1/search`, with search, page, and sort parameters.
- **Size:** [TODO: add the number of listings you usually pull]
- **Raw fields:** Product name, highlights, price, and rating.
- **Engineered columns:** CPU tier (1 to 5), RAM (GB), storage (GB), dedicated GPU, gaming flag, screen size (inches), portability score, normalised rating, price value, and touchscreen.
- **Cleaning steps:**
  - Organise the listings into a Pandas table.
  - Combine product names and highlights to find spec details.
  - Convert numbers to the right data types.
  - Fill missing specs with preset fallback values.

## Approach / Methodology

1. Request laptop listings from the API with Python Requests.
2. Extract names, highlights, prices, and ratings.
3. Clean and normalise the data with Pandas.
4. Pull out hardware specs from the text using regular expressions.
5. Turn each laptop into a numerical feature vector.
6. Remove laptops that fail the user's hard requirements: budget, RAM, storage, GPU, touchscreen, and brand.
7. Score the remaining laptops with the weights for the chosen use.
8. Find similar laptops using cosine similarity on the feature vectors.
9. Show the top three features behind each score as a short explanation.
10. Show the results in Streamlit, with comparison and CSV download.

**Scoring formula:** score = sum of (weight x normalised feature value). The score is shown as a match percentage. Matching keywords add a small adjustment.

**Usage weights:**

| Feature         | Student | Coding and ML | Gaming | Creative | Business |
| --------------- | ------: | ------------: | -----: | -------: | -------: |
| CPU performance |    0.15 |          0.28 |   0.25 |     0.25 |     0.15 |
| RAM             |    0.15 |          0.30 |   0.10 |     0.20 |     0.10 |
| Storage         |    0.10 |          0.10 |   0.05 |     0.15 |     0.10 |
| GPU             |    0.00 |          0.12 |   0.40 |     0.15 |     0.00 |
| Portability     |    0.25 |          0.05 |   0.00 |     0.05 |     0.35 |
| Rating          |    0.10 |          0.05 |   0.05 |     0.05 |     0.10 |
| Price value     |    0.25 |          0.10 |   0.15 |     0.15 |     0.20 |

Each column adds up to 1.0.

**Similarity:** Price is included in the comparison. Rating and price value are left out.

## Results and Insights

- Live and deployed: [LapPick on Streamlit](https://laptop-price-and-recommendation-system-icvhjjspmfrmmy2rfmtuaq.streamlit.app/)
- Listings processed in a typical search: [TODO: add the number if you measured it]
- Share of listings where all specs were found: [TODO: add if you measured it]
- Example insight: [TODO: add one finding, such as how rankings change between Student and Gaming]

**Limitations**

1. Available laptops depend on the API provider.
2. Product descriptions can be incomplete or inconsistent.
3. CPU tiers are rule-based groups, not benchmark scores.
4. Missing specs are filled with preset fallback values.
5. The match score shows how well a laptop fits your needs. It does not predict whether you will be happy with it.
6. There is no trained machine learning model in this project.

## How to Run Locally

You need Python 3.10 or higher and an API.SH API key.

Clone the repository:

```bash
git clone https://github.com/mathan-ponraj/lappick.git
```

Go to the project folder:

```bash
cd lappick
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

On macOS or Linux, use `source .venv/bin/activate` instead.

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root, using `.env.example` as a template:

```env
APISH_KEY=your_actual_api_key
```

On Streamlit Community Cloud, add `APISH_KEY` in the app's Secrets settings. Never commit your real API key or `.env` file to GitHub.

Start the app:

```bash
streamlit run app.py
```

## Screenshots

| Home | Ranked results |
| ---- | -------------- |
| ![Home](screenshots/home.png) | ![Results](screenshots/results.png) |

| Compare laptops | Similar laptops |
| --------------- | --------------- |
| ![Compare](screenshots/compare.png) | ![Similar](screenshots/similar.png) |

<!-- [TODO: add your screenshots to a screenshots/ folder with these file names, or update the paths] -->

## What I Learned and Future Improvements

**What I learned**

- Pulled live data from a REST API and turned it into a clean table with Pandas.
- Extracted structured features from messy product text using regular expressions.
- Built numerical feature vectors and normalised them for fair comparison.
- Designed weighted scoring and chose different weights for different uses.
- Applied cosine similarity with NumPy to find laptops with similar specs.
- Wrote clear explanations for each result so the score is easy to understand.
- Documented the limits of my method, such as rule-based CPU tiers and fallback values.

**Future improvements**

- Replace the rule-based CPU tiers with benchmark data.
- Test how well the extraction finds specs across more listings.
- Track price changes over time to show price trends.

## Contact

[![Live Demo](https://img.shields.io/badge/Live%20Demo-LapPick-6366f1?style=for-the-badge&logo=streamlit&logoColor=white)](https://laptop-price-and-recommendation-system-icvhjjspmfrmmy2rfmtuaq.streamlit.app/)
[![GitHub](https://img.shields.io/badge/GitHub-mathan--ponraj-181717?style=for-the-badge&logo=github)](https://github.com/mathan-ponraj)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-mathan03-0A66C2?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/mathan03/)

---

Developed by Mathan
