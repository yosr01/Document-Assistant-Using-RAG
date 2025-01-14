import os
import faiss
from sentence_transformers import SentenceTransformer

def create_embeddings(chunk_dir, index_file):
    os.makedirs(os.path.dirname(index_file), exist_ok=True)
    # Load embedding model
    model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
    # Read all chunks and create embeddings
    chunks = []
    chunk_files = sorted([os.path.join(chunk_dir, f) for f in os.listdir(chunk_dir) if f.startswith("chunk_")])
    if not chunk_files:
        raise ValueError(f"No chunk files found in the directory: {chunk_dir}")
    
    for chunk_file in chunk_files:
        with open(chunk_file, 'r', encoding='utf-8') as file:
            chunks.append(file.read())
    
    if not chunks:
        raise ValueError("No text data found in chunk files.")
    
    # Generate embeddings
    embeddings = model.encode(chunks)
    
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    faiss.write_index(index, index_file)
    
    print(f"FAISS index created with {len(chunks)} embeddings at {index_file}.")
