import numpy as np

def generate_prediction_data():
    """
    Simulates loading a model and generating a forecast.
    In a real app, this would load a saved model (e.g., from a .joblib file)
    and use it to predict on new data.
    """
    
    # 1. Simulate historical sales data (the blue line)
    historical_dates = np.arange(1, 16) # Represents past 15 time periods
    historical_sales = historical_dates * 2.5 + np.random.rand(15) * 10
    
    # 2. Simulate a forecast (the green line)
    # The forecast line should connect to the end of the historical line
    forecast_dates = np.arange(15, 21) # Represents current period + 5 future periods
    forecast_sales = (historical_sales[-1] - 5) + (forecast_dates - 14) * 3 + np.random.rand(6) * 5
    
    # 3. Simulate the KPI panel data
    next_quarter_prediction = forecast_sales[-1] * 1_000_000 # Example scaling
    
    # 4. Simulate model and data quality metrics
    model_performance = {
        'Accuracy': '95%', # Using string for simplicity, could be float
        'RMSE': '320',
        'F1 Score': '0.88'
    }
    
    feature_weights = {
        'Economic Indicators': '45%',
        'Historical Sales': '35%',
        'Competitor Activity': '20%'
    }
    
    data_quality_score = 92 # As a percentage
    
    # 5. Package everything into a single dictionary for easy transport
    return {
        "historical_x": historical_dates,
        "historical_y": historical_sales,
        "predicted_x": forecast_dates,
        "predicted_y": forecast_sales,
        "next_quarter_prediction": f"{next_quarter_prediction/1_000_000:.1f}M",
        "model_performance": model_performance,
        "feature_weights": feature_weights,
        "data_quality_score": data_quality_score
    }