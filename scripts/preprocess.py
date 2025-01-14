import os
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter
import pdfplumber

def preprocess_document(input_file, output_dir):
    with pdfplumber.open(input_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()

    def clean_text(text):
        # Remove promotional and irrelevant metadata
        text = re.sub(r"Edition\s*:.*?articles.*?liens", "", text, flags=re.DOTALL)
        text = re.sub(r"Pensez à actualiser.*?HAL-CNRS\.", "", text, flags=re.DOTALL)
        text = re.sub(r"Traitements effectués.*?Conseil constitutionnel,", "", text, flags=re.DOTALL)
        text = re.sub(r"p\.\d+\s+Code civil", "", text, flags=re.MULTILINE)

        # Remove table of contents, including Titre, Sous-titre, Paragraphe, etc.
        text = re.sub(r"(?i)(Titre|Sous-titre|Chapitre|Section|Paragraphe|Sous-Sous-Sous-Sous-Sous-Sous-Sous-Sous-Sous-Sous-Paragraphe)\s+[^\n]*\s*(\d{1,4})?[\.\-]*", "", text, flags=re.DOTALL)

        # Remove page number references (e.g., . . . 268, 304, etc.)
        text = re.sub(r"\.+\s*\d+", "", text)

        # Remove any remaining unwanted references to pages or citations
        text = re.sub(r"\(\d+\)", "", text)

        # Normalize whitespace
        text = re.sub(r"\n\s*\n", "\n", text).strip()
        return text

    cleaned_text = clean_text(text)

    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_text(cleaned_text)
    
    os.makedirs(output_dir, exist_ok=True)
    for i, chunk in enumerate(chunks):
        with open(f"{output_dir}/chunk_{i}.txt", 'w', encoding='utf-8') as chunk_file:
            chunk_file.write(chunk)
    
