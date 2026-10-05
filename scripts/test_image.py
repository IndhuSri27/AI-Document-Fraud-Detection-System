import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parents[1])
)

from src.image_analysis import analyze_image


# Change this to an image file if you have one
image_path = "test_document.png"


result = analyze_image(image_path)


print("Image Analysis")
print("----------------")

for name, value in result.items():
    print(f"{name}: {value}")