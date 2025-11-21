import io
from pypdf import PdfReader

def extract_text_from_pdf(uploaded_file):
    """
    Extracts text from an uploaded PDF file.
    Works for Streamlit uploaded files AND normal file paths.
    """
    if isinstance(uploaded_file, str):
        # If file path given
        reader = PdfReader(uploaded_file)
    else:
        # If Streamlit uploaded file
        file_bytes = io.BytesIO(uploaded_file.read())
        reader = PdfReader(file_bytes)

    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"

    return text
