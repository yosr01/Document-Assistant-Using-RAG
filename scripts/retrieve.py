import chromadb
from sentence_transformers import SentenceTransformer

def retrieve_chunks(query, db_collection_name, top_k=5):
    # Initialize ChromaDB client
    client = chromadb.Client()
    collection = client.get_or_create_collection(db_collection_name)

    model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
    query_embedding = model.encode([query])

    # Query ChromaDB for the top K closest results
    results = collection.query(
        query_embeddings=query_embedding.tolist(),  
        n_results=top_k 
    )

    # Retrieve the corresponding chunks
    chunks = results['documents']

    return chunks
