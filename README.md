Fr_Detector: Real-Time Fraud Detection API
A machine learning-powered API to detect fraudulent credit card transactions in real-time based on behavioral patterns.

Table of Contents
About The Project

Built With

Getting Started

Prerequisites

Installation

Usage

1. Train the Model

2. Run the API Server

3. Send a Prediction Request

API Endpoints

Project Structure

Deployment with Docker

License

About The Project
Fr_Detector is a system designed to identify potentially fraudulent transactions as they happen. It does not verify card details (like CVV or expiry date) but instead analyzes the pattern of a transaction.

The core of the project is a machine learning model trained on historical data to recognize anomalies and behavioral patterns that are indicative of fraud, such as unusual transaction amounts, times, or frequencies. This model is served via a lightweight FastAPI application, making it easy to integrate into a larger payment processing workflow.

Built With
This project utilizes the following major libraries and frameworks:

FastAPI: For building the high-performance API.

Scikit-learn: For the machine learning model and data processing.

Pandas: For data manipulation.

Uvicorn: As the lightning-fast ASGI server.

Imbalanced-learn: To handle imbalanced datasets during training.

Joblib: For serializing and deserializing the trained model.

Getting Started
Follow these steps to get a local copy up and running.

Prerequisites
Make sure you have the following installed on your system:

Python 3.10 or newer

pip (Python package installer)

Installation
Clone the repository

git clone https://github.com/Panth09/Fr_Detector.git
cd Fr_Detector

Create and activate a virtual environment (recommended)

# For Windows
python -m venv venv
.\venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

Install the required packages

pip install -r requirements.txt

Usage
The project workflow is divided into two main parts: training the model and running the API.

1. Train the Model
Before you can run the API, you need to train the machine learning model and create the model.pkl and scaler.pkl files.

Run the training script from the root directory of the project:

python train_model.py

This will generate the necessary files inside the models/ directory.

2. Run the API Server
Once the model is trained, start the FastAPI server using Uvicorn.

uvicorn api.app:app --host 127.0.0.1 --port 8000 --reload

The --reload flag is great for development, as it automatically restarts the server when you make changes to the code.

3. Send a Prediction Request
With the server running, you can now send POST requests to the /predict endpoint.

Using PowerShell (Windows):

Invoke-WebRequest -Uri "http://127.0.0.1:8000/predict" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{
    "transaction_id": "txn_test_101",
    "user_id": "user_99",
    "merchant_id": "merchant_42",
    "transaction_amount": 550.75,
    "transaction_dt": "2025-07-26T03:10:00Z",
    "user_avg_amount": 120.50
}'

Using cURL (macOS/Linux):

curl -X POST "http://127.0.0.1:8000/predict" \
-H "Content-Type: application/json" \
-d '{
    "transaction_id": "txn_test_101",
    "user_id": "user_99",
    "merchant_id": "merchant_42",
    "transaction_amount": 550.75,
    "transaction_dt": "2025-07-26T03:10:00Z",
    "user_avg_amount": 120.50
}'

You can also test this endpoint interactively by visiting http://127.0.0.1:8000/docs in your browser.

API Endpoints
GET /

A root endpoint to check if the API is running.

Response: {"message": "Welcome to the Fr_Detector API..."}

POST /predict

The main endpoint for fraud detection.

Request Body: A JSON object containing the transaction details.

Success Response: A JSON object with the prediction and confidence score.

{
  "transaction_id": "txn_test_101",
  "is_fraud": 1,
  "confidence_score": "0.9992"
}

Project Structure
Fr_Detector/
├── api/
│   └── app.py          # FastAPI application script
├── models/
│   ├── model.pkl       # Trained machine learning model
│   └── scaler.pkl      # Trained data scaler
├── .gitignore
├── Dockerfile          # For containerizing the application
├── README.md           # This file
├── requirements.txt    # Python package dependencies
└── train_model.py      # Script to train the model

Deployment with Docker
This project includes a Dockerfile for easy containerization and deployment.

Build the Docker image:

docker build -t fr-detector-api .

Run the Docker container:

docker run -d -p 8000:8000 --name fr-detector-container fr-detector-api

The API will now be accessible at http://localhost:8000.

License
Distributed under the MIT License. See LICENSE for more information.