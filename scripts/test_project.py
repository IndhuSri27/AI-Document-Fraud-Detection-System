import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parents[1])
)

from src.model import predict_document


sample_document = """
This is a forged certificate with altered marks
and a fake registration number.
"""


result, probability = predict_document(
    sample_document
)


print("Document Analysis")
print("------------------")
print("Result:", result)
print(f"Fraud Probability: {probability:.2f}%")
