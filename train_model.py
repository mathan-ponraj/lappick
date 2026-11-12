import pandas as pd
import numpy as np
import joblib
import os
import logging
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, r2_score

# --- Logging Configuration ---
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def train_model():
    # 1. Data Ingestion
    try:
        data = pd.read_csv("data/data.csv")
        logger.info("Dataset loaded successfully.")
    except FileNotFoundError:
        logger.error("Data file not found at 'data/data.csv'")
        return

    # 2. Feature Selection & Target Alignment
    # Ensuring features match the inference script requirements
    features = ['Brand', 'RAM_GB', 'Storage', 'Price', 'Processor_name', 'OS']
    X = data[features].copy()
    y = data['Rating'].copy()

    # Drop missing values and align target
    initial_count = len(X)
    X = X.dropna()
    y = y.loc[X.index]
    logger.info(f"Dropped {initial_count - len(X)} rows with missing values.")

    # 3. Feature Engineering: Outlier Management
    # Capping 'Price' using Winsorization (1st and 99th percentiles)
    q1, q99 = X['Price'].quantile([0.01, 0.99])
    X['Price'] = X['Price'].clip(lower=q1, upper=q99)

    # Log Transformation for target stabilization
    y_transformed = np.log1p(y)

    # 4. Pipeline Architecture
    categorical_cols = X.select_dtypes(include='object').columns.tolist()
    numerical_cols = X.select_dtypes(include='number').columns.tolist()

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_cols),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
        ])

    # Model definition using XGBoost Regressor
    model_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('xgb', XGBRegressor(
            n_estimators=100, 
            learning_rate=0.1, 
            max_depth=5, 
            random_state=42,
            n_jobs=-1  # Utilize all CPU cores
        ))
    ])

    # 5. Model Training
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_transformed, test_size=0.2, random_state=42
    )

    logger.info("Commencing model training...")
    model_pipeline.fit(X_train, y_train)
    logger.info("Model training complete.")

    # 6. Evaluation on Original Scale
    y_pred_log = model_pipeline.predict(X_test)
    y_pred = np.expm1(y_pred_log)
    y_test_original = np.expm1(y_test)

    rmse = np.sqrt(mean_squared_error(y_test_original, y_pred))
    r2 = r2_score(y_test_original, y_pred)

    logger.info(f"Evaluation Metrics:")
    logger.info(f"-> RMSE: {rmse:.4f}")
    logger.info(f"-> R2 Score: {r2:.4f}")

    # 7. Model Persistence
    os.makedirs('model', exist_ok=True)
    joblib.dump(model_pipeline, 'model/model.pkl')
    logger.info("Model pipeline serialized to 'model/model.pkl'")

if __name__ == "__main__":
    train_model()
