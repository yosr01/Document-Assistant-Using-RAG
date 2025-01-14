from preprocess import preprocess_document
from embedding import create_embeddings
from retrieve import retrieve_chunks


preprocess_document("Code_civil-1-20.pdf", "data/chunks")
create_embeddings("data/chunks", "embeddings/index.faiss")
query = "empreintes génétiques"
results = retrieve_chunks(query, "embeddings/index.faiss", "data/chunks")
print("Query Results:")
for i, result in enumerate(results):
    print(f"\nResult {i + 1}:\n{result}")
