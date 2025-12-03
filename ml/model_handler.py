import os
import time
import joblib
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

from ml.data_louder import load_and_preprocess_data

def train_model(selected_features, algorithm_choice, hyperparameters):
    """
    Trains a real machine learning model and saves it.
    """
    print("--- Starting Real Model Training ---")
    
    # 1. Load Data
    df = load_and_preprocess_data()
    if df is None:
        return {"error": "Failed to load data."}

    # 2. Define Features (X) and Target (y)
    features = ['Year', 'Month', 'Quarter', 'MarketingSpend', 'IsHoliday']
    target = 'Sales'
    
    X = df[features]
    y = df[target]

    # Split data for validation
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    # 3. Initialize and Train Model
    # Here you could have logic to switch between algorithms based on algorithm_choice
    model = GradientBoostingRegressor(
        n_estimators=hyperparameters.get('n_estimators', 100),
        random_state=42
    )
    
    model.fit(X_train, y_train)
    print("Model fitting complete.")

    # 4. Evaluate Model
    predictions = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    print(f"Model evaluation RMSE: {rmse:.2f}")

    # 5. Save the Trained Model
    model_dir = 'models'
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    model_filename = f"sales_model_{timestamp}.joblib"
    model_path = os.path.join(model_dir, model_filename)
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")

    # 6. Return results for the UI
    return {
        "rmse": f"{rmse:,.2f}",
        "model_id": model_filename,
        "features_used": features
    }