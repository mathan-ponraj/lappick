<div align="center">

# 💻 LapPick

### Find the right laptop with data, not guesswork.

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Machine_Learning-8E44AD?style=for-the-badge" />
  <img src="https://img.shields.io/badge/XGBoost-EC6B23?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
</p>

<br/>

<a href="https://laptop-price-and-recommendation-system-icvhjjspmfrmmy2rfmtuaq.streamlit.app/">
  <img src="https://img.shields.io/badge/🚀_EXPLORE_LIVE_DEMO-7C3AED?style=for-the-badge&logo=streamlit&logoColor=white" />
</a>

<br/><br/>

*An interactive machine learning application for smarter laptop recommendations.*

</div>

---

## About the Project

LapPick is a machine learning-based laptop recommendation system that helps users find suitable laptops based on their budget, brand, RAM, storage, and storage type requirements.

It uses an **XGBoost regression model** to predict laptop ratings and ranks matching laptops based on their predicted performance.

The trained model is integrated into a Streamlit application to deliver an interactive recommendation experience.

## Key Features

* Budget-based laptop filtering.
* Brand and specification-based recommendations.
* XGBoost-powered rating prediction.
* Top 5 matching laptop recommendations.
* Interactive Streamlit interface.
* CSV export for recommended laptops.

## Project Workflow

1. **Data Exploration** – Analyzed laptop prices, brands, RAM, storage, ratings, and other available features.
2. **Data Preprocessing** – Handled missing values, capped extreme prices, encoded categorical features, and scaled numerical features.
3. **Feature Engineering** – Prepared numerical and categorical variables for model training.
4. **Model Training** – Developed an XGBoost regression model to predict laptop ratings.
5. **Model Evaluation** – Evaluated performance using RMSE and R² metrics.
6. **Recommendation Engine** – Filtered laptops based on user preferences and ranked them using predicted ratings.
7. **Deployment** – Integrated the trained model into a Streamlit application.

## Obstacles & Solutions

| Challenge                    | Solution                                                                   |
| ---------------------------- | -------------------------------------------------------------------------- |
| Different feature types      | Used `ColumnTransformer`, `OneHotEncoder`, and `StandardScaler`.           |
| Extreme price values         | Applied 1st and 99th percentile price capping.                             |
| Variation in rating values   | Applied log transformation to the target variable.                         |
| Consistent preprocessing     | Combined preprocessing and XGBoost into a single Scikit-learn pipeline.    |
| Personalized recommendations | Implemented filters for budget, brand, RAM, and storage.                   |
| Model deployment             | Used Joblib to save the trained pipeline and integrated it with Streamlit. |

## Model & Results

**Algorithm:** XGBoost Regression

**Evaluation Metrics:** RMSE and R²

The project includes model comparison during development, with XGBoost achieving approximately **0.96 R²** in the reported evaluation.

The deployed application allows users to:

* Explore laptops matching their requirements.
* View the top 5 recommendations.
* Compare predicted ratings.
* Export recommendations as CSV.

## Technology Stack

| Category          | Technologies          |
| ----------------- | --------------------- |
| Programming       | Python                |
| Data Analysis     | Pandas, NumPy         |
| Visualization     | Matplotlib, Seaborn   |
| Machine Learning  | Scikit-learn, XGBoost |
| Model Persistence | Joblib                |
| Application       | Streamlit             |

## Skills Demonstrated

* Data Cleaning & Preprocessing
* Exploratory Data Analysis (EDA)
* Feature Engineering
* Regression Modeling
* Model Evaluation
* Machine Learning Pipelines
* Recommendation Systems
* Model Deployment

## Future Enhancements

* Multi-factor recommendation scoring.
* SHAP-based model explainability.
* PostgreSQL integration for structured data retrieval.
* FastAPI backend development.
* MLflow for experiment tracking.
* Docker and CI/CD automation.
* LLM-powered natural-language laptop recommendations.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/mathan-ponraj/Laptop-Price-And-Recommendation-System.git

# Navigate to the project
cd Laptop-Price-And-Recommendation-System

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

## Developer

<div align="center">

### Mathan Ponraj

**M.E. Computer Science | Python | Data Science | Machine Learning**

<a href="https://github.com/mathan-ponraj">
  <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" />
</a>
<a href="https://www.linkedin.com/in/mathan03/">
  <img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" />
</a>

*Built with data, curiosity, and continuous learning.*

</div>
