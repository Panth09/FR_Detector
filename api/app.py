import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import os

# --- 1. Application and Model Loading ---

# Create the FastAPI application instance
app = FastAPI(title="Fr_Detector API", version="1.0")

# Define paths to the model and scaler
# This assumes the script is run from the root directory of the project
# where 'api' and 'models' are subdirectories.
MODEL_PATH = os.path.join("models", "model.pkl")
SCALER_PATH = os.path.join("models", "scaler.pkl")

# Load the model and scaler at startup
try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    print("Model and scaler loaded successfully.")
except FileNotFoundError:
    print(f"Error: Model at {MODEL_PATH} or scaler at {SCALER_PATH} not found.")
    print("Please ensure you have run the training script to generate these files.")
    model = None
    scaler = None

# --- 2. Pydantic Data Model for Input Validation ---

# This model defines the structure and data types for the incoming request body.
# FastAPI will automatically validate the incoming data against this model.
class Transaction(BaseModel):
    transaction_id: str
    user_id: str
    merchant_id: str
    transaction_amount: float
    transaction_dt: datetime
    # These features would ideally be calculated by looking up user history in a database.
    # For this example, we'll expect them in the request.
    user_avg_amount: float = 85.50 # Providing a default value

# --- 3. API Endpoints ---

@app.get("/", tags=["General"])
def read_root():
    """A simple endpoint to check if the API is running."""
    return {"message": "Welcome to the Fr_Detector API. Use the /predict endpoint for fraud detection."}

@app.post("/predict", tags=["Prediction"])
def predict_fraud(transaction: Transaction):
    """
    Predicts whether a transaction is fraudulent.

    Receives transaction data, processes it to create features,
    and returns a fraud prediction with a confidence score.
    """
    if not model or not scaler:
        raise HTTPException(status_code=503, detail="Model is not available. Please check server logs.")

    try:
        # Create a DataFrame from the Pydantic model
        df = pd.DataFrame([transaction.dict()])
        
        # --- Feature Engineering (must match the training script) ---
        df['hour_of_day'] = df['transaction_dt'].dt.hour
        df['day_of_week'] = df['transaction_dt'].dt.dayofweek
        # Add a small epsilon to avoid division by zero, matching the training script
        df['amount_vs_avg_ratio'] = df['transaction_amount'] / (df['user_avg_amount'] + 1e-6)
        
        # Define and order features exactly as in training
        features_ordered = [
            'transaction_amount', 
            'hour_of_day', 
            'day_of_week',
            'amount_vs_avg_ratio'
        ]
        
        # Ensure the DataFrame has the features in the correct order
        df = df[features_ordered]
        
        # Scale the features
        scaled_features = scaler.transform(df)
        
        # Make prediction
        prediction = model.predict(scaled_features)
        prediction_proba = model.predict_proba(scaled_features)
        
        is_fraud = int(prediction[0])
        # Get the probability of the transaction being fraud (class 1)
        confidence_score = float(prediction_proba[0][1])

        # Return the result
        return {
            "transaction_id": transaction.transaction_id,
            "is_fraud": is_fraud,
            "confidence_score": f"{confidence_score:.4f}"
        }

    except Exception as e:
        # This will catch any errors during the prediction process
        raise HTTPException(status_code=500, detail=f"An error occurred during prediction: {str(e)}")

