import os
import re
import pdfplumber

def preprocess_document(input_file, output_dir):
    with pdfplumber.open(input_file) as pdf:
        text = ""
        for i, page in enumerate(pdf.pages):
            if i >= 11: 
                text += page.extract_text()

    def clean_text(text):
        # Remove promotional and irrelevant metadata
        text = re.sub(r"Edition\s*:.*?articles.*?liens", "", text, flags=re.DOTALL)
        text = re.sub(r"Pensez à actualiser.*?HAL-CNRS\.", "", text, flags=re.DOTALL)
        text = re.sub(r"Traitements effectués.*?Conseil constitutionnel,", "", text, flags=re.DOTALL)
        text = re.sub(r"p\.\d+\s+Code civil", "", text, flags=re.MULTILINE)

        # Remove table of contents, including Titre, Sous-titre, Paragraphe, etc.
        # text = re.sub(r"(?i)(Titre|Sous-titre|Chapitre|Section|Paragraphe|Sous-Sous-Sous-Sous-Sous-Sous-Sous-Sous-Sous-Sous-Paragraphe)\s+[^\n]*\s*(\d{1,4})?[\.\-]*", "", text, flags=re.DOTALL)

        # Remove page number references (e.g., . . . 268, 304, etc.)
        text = re.sub(r"\.+\s*\d+", "", text)

        # Remove any remaining unwanted references to pages or citations
        text = re.sub(r"\(\d+\)", "", text)

        # Normalize whitespace
        text = re.sub(r"\n\s*\n", "\n", text).strip()

        return text

    # Remove content before the specific title
    title_pattern = r"Titre préliminaire\s*:.*?de l'application des lois en général"
    match = re.search(title_pattern, text)
    if match:
        # Keep everything from the title onward
        cleaned_text = text[match.start():]
    else:
        cleaned_text = clean_text(text)

    # Define a pattern for the combined identifiers: Legif., Plan, Jp.C.Cass., Jp.Appel, Jp.Admin., Juricaf
    combined_pattern = r"(Legif\.|Plan|Jp\.C\.Cass\.|Jp\.Appel|Jp\.Admin\.|Juricaf)\s*"

    # Remove the individual identifiers as separate markers and combine them into one block
    cleaned_text = re.sub(combined_pattern, "COMBINED_IDENTIFIER_BLOCK ", cleaned_text)

    # Split the text into parts based on the combined block identifier
    law_parts = cleaned_text.split("COMBINED_IDENTIFIER_BLOCK")
    law_parts = [part.strip() for part in law_parts if part.strip()]

    # Create a chunk for each law
    os.makedirs(output_dir, exist_ok=True)
    for i, content in enumerate(law_parts):
        file_path = os.path.join(output_dir, f"chunk_{i}.txt")

        # Save chunks
        with open(file_path, 'w', encoding='utf-8') as law_file:
            law_file.write(content)


