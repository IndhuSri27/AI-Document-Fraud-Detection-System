import joblib
from pathlib import Path


# Find the trained model
PROJECT_ROOT = Path(__file__).resolve().parents[1]

MODEL_PATH = PROJECT_ROOT / "models" / "fraud_model.pkl"


# Load trained model
model = joblib.load(MODEL_PATH)


def predict_document(text):
    """
    Predict whether a document is genuine or fraudulent.
    """

    prediction = model.predict([text])[0]

    probability = model.predict_proba([text])[0]

    fraud_probability = probability[1] * 100

    if prediction == 1:
        result = "Fraud Risk"
    else:
        result = "Genuine"

    return result, fraud_probability