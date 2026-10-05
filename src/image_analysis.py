import cv2
import numpy as np


def analyze_image(image_path):
    """
    Analyze a document image for basic
    tampering-related signals.
    """

    image = cv2.imread(str(image_path))

    if image is None:
        return {
            "status": "Unable to read image",
            "tampering_score": 0
        }

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Calculate image noise
    noise = np.std(gray)

    # Detect edges
    edges = cv2.Canny(gray, 100, 200)

    edge_pixels = np.sum(edges > 0)

    total_pixels = edges.shape[0] * edges.shape[1]

    edge_ratio = edge_pixels / total_pixels

    # Calculate a simple tampering score
    score = 0

    if noise > 50:
        score += 20

    if edge_ratio > 0.15:
        score += 20

    score = min(score, 100)

    return {
        "status": "Image analyzed successfully",
        "noise_level": round(float(noise), 2),
        "edge_ratio": round(float(edge_ratio), 4),
        "tampering_score": score
    }
