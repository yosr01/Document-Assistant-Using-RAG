import os
import re
import pdfplumber
import nltk
from nltk.corpus import stopwords
from sentence_transformers import SentenceTransformer
import chromadb

# Download the French stopwords list
nltk.download('stopwords')

def preprocess_document(input_file, output_dir, collection_name="law_chunks"):
    # Initialize ChromaDB client
    client = chromadb.Client()

    # Check if the collection exists, if not, create it
    try:
        collection = client.get_collection(collection_name)
    except chromadb.errors.InvalidCollectionException:
        # If the collection does not exist, create a new one
        print(f"Collection {collection_name} does not exist, creating a new one.")
        collection = client.create_collection(collection_name)

    # Load the model for embeddings
    model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

    with pdfplumber.open(input_file) as pdf:
        text = ""
        for i, page in enumerate(pdf.pages):
            if i >= 11:  # Skip the first 11 pages
                text += page.extract_text()

    def clean_text(text):
        # Remove promotional and irrelevant metadata
        text = re.sub(r"Edition\s*:.*?articles.*?liens", "", text, flags=re.DOTALL)
        text = re.sub(r"Pensez à actualiser.*?HAL-CNRS\.", "", text, flags=re.DOTALL)
        text = re.sub(r"Traitements effectués.*?Conseil constitutionnel,", "", text, flags=re.DOTALL)
        text = re.sub(r"p\.\d+\s+Code civil", "", text, flags=re.MULTILINE)

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
        cleaned_text = text[match.start():]
    else:
        cleaned_text = clean_text(text)

    # Define a pattern for the combined identifiers
    combined_pattern = r"(Legif\.|Plan|Jp\.C\.Cass\.|Jp\.Appel|Jp\.Admin\.|Juricaf)\s*"

    # Remove the individual identifiers
    cleaned_text = re.sub(combined_pattern, "COMBINED_IDENTIFIER_BLOCK ", cleaned_text)

    # Remove French stopwords
    stop_words = set(stopwords.words('french'))
    words = cleaned_text.split()
    filtered_words = [word for word in words if word.lower() not in stop_words]
    cleaned_text = " ".join(filtered_words)

    # Split text into parts
    law_parts = cleaned_text.split("COMBINED_IDENTIFIER_BLOCK")
    law_parts = [part.strip() for part in law_parts if part.strip()]

    # Add embeddings to ChromaDB collection
    for i, content in enumerate(law_parts):
        # Generate embeddings for each chunk
        embedding = model.encode([content])
        
        # Add the chunk and embedding to ChromaDB
        collection.add(
            documents=[content],
            embeddings=embedding,
            metadatas=[{"chunk_id": i}],
            ids=[str(i)]
        )

        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, f"chunk_{i}.txt")
        with open(file_path, 'w', encoding='utf-8') as law_file:
            law_file.write(content)

    print(f"Chunks and embeddings stored in ChromaDB collection: {collection_name}")
