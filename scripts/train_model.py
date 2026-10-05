import sys
from pathlib import Path

import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


# Add project folder to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))


# File paths
DATA_FILE = PROJECT_ROOT / "data" / "training_documents.csv"
MODEL_FILE = PROJECT_ROOT / "models" / "fraud_model.pkl"


print("Loading training dataset...")

# Read dataset
data = pd.read_csv(DATA_FILE)

print(f"Training documents: {len(data)}")


# Input text and labels
X = data["text"]
y = data["label"]


# Create machine learning pipeline
model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2)
        )
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=1000
        )
    )
])


print("Training AI model...")

# Train the model
model.fit(X, y)


# Create models folder if it doesn't exist
MODEL_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)


# Save trained model
joblib.dump(model, MODEL_FILE)


print("✅ Model training completed!")
print(f"✅ Model saved to: {MODEL_FILE}")