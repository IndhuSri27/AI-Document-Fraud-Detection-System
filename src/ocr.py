import os
import tempfile
from pathlib import Path

import cv2
import pytesseract
from PIL import Image


# Windows Tesseract path
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

if os.path.exists(TESSERACT_PATH):
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


def preprocess_image(image_path):
    """Improve document image before OCR."""
    image = cv2.imread(str(image_path))

    if image is None:
        raise ValueError("Unable to read the image.")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Remove noise
    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    # Convert to black and white
    processed = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    return processed


def extract_text_from_image(image_path):
    """Extract text from an image using Tesseract OCR."""
    processed = preprocess_image(image_path)

    text = pytesseract.image_to_string(processed)

    return text.strip()


def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF by converting its pages to images.
    Requires PyMuPDF.
    """
    try:
        import fitz
    except ImportError:
        raise ImportError(
            "PyMuPDF is not installed. Run: "
            "python -m pip install pymupdf"
        )

    document = fitz.open(pdf_path)
    all_text = []

    with tempfile.TemporaryDirectory() as temp_dir:

        for page_number, page in enumerate(document):

            # Convert PDF page to image
            pixmap = page.get_pixmap(matrix=fitz.Matrix(2, 2))

            image_path = Path(temp_dir) / f"page_{page_number}.png"

            pixmap.save(str(image_path))

            # OCR
            text = extract_text_from_image(image_path)

            if text:
                all_text.append(text)

    document.close()

    return "\n\n".join(all_text)


def extract_text(file_path):
    """Automatically select image or PDF OCR."""
    file_path = str(file_path)

    extension = Path(file_path).suffix.lower()

    if extension == ".pdf":
        return extract_text_from_pdf(file_path)

    if extension in [".png", ".jpg", ".jpeg"]:
        return extract_text_from_image(file_path)

    raise ValueError(
        f"Unsupported file type: {extension}"
    )

