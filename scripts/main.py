from preprocess import preprocess_document
from embedding import create_embeddings
from retrieve import retrieve_chunks

#if you want to run the preprocessing, chunking and retrival parts use the cmd line : python scripts/main.py
preprocess_document("Code_civil.pdf", "data/chunks")
create_embeddings("data/chunks", "embeddings/index.faiss")
query = "empreintes génétiques"
results = retrieve_chunks(query, "law_chunks", top_k=5)  
print("Query Results:")
for i, result in enumerate(results):
    print(f"\nResult {i + 1}:\n{result}")
