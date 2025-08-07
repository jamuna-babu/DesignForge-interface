import os
import fitz # !!! This is from PyMuPDF 

# Extract text from PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def process_pdf(file):
    filename = file.filename
    # TODO: Is uploading necessary?
    uploads_folder = os.path.join(os.getcwd(), "uploads")
    if not os.path.exists(uploads_folder):
        os.makedirs(uploads_folder)
    filepath = os.path.join(uploads_folder, filename)
    file.save(filepath)
    
    # Extract text from PDF
    text = extract_text_from_pdf(filepath)
    return text
