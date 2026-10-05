import streamlit as st
import tempfile
import fitz
import sys
from pathlib import Path

# Add project folder to Python path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.append(str(PROJECT_ROOT))

from src.model import predict_document


st.set_page_config(
    page_title="AI Document Fraud Detection",
    page_icon="📄",
    layout="wide"
)


st.title("📄 AI-Based Document Fraud Detection System")

st.write(
    "Upload a PDF document to analyze its possible fraud risk."
)


uploaded_file = st.file_uploader(
    "Upload PDF Document",
    type=["pdf"]
)


def extract_text_from_pdf(pdf_path):

    document = fitz.open(pdf_path)

    all_text = []

    for page in document:

        text = page.get_text()

        if text.strip():
            all_text.append(text)

    document.close()

    return "\n".join(all_text)


if uploaded_file:

    st.success(
        f"File uploaded: {uploaded_file.name}"
    )

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as temp_file:

        temp_file.write(
            uploaded_file.getbuffer()
        )

        temp_pdf_path = temp_file.name


    st.info("Reading document...")


    try:

        extracted_text = extract_text_from_pdf(
            temp_pdf_path
        )


        if extracted_text.strip():

            st.success(
                "✅ Document text extracted successfully!"
            )


            st.subheader("📄 Extracted Text")

            st.text_area(
                "Document Content",
                extracted_text,
                height=300
            )


            # AI prediction
            result, probability = predict_document(
                extracted_text
            )


            st.subheader("🤖 AI Analysis")


            if result == "Fraud Risk":

                st.error(
                    f"⚠️ {result}"
                )

            else:

                st.success(
                    f"✅ {result}"
                )


            st.metric(
                "Fraud Probability",
                f"{probability:.2f}%"
            )


            st.progress(
                min(int(probability), 100)
            )


        else:

            st.warning(
                "⚠️ No selectable text found in this PDF."
            )

            st.info(
                "This may be a scanned PDF. "
                "OCR support will be added later."
            )


    except Exception as e:

        st.error(
            f"Error: {e}"
        )