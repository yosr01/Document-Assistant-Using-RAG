import faiss
from sentence_transformers import SentenceTransformer

def retrieve_chunks(query, index_file, chunk_dir, top_k=10):
    model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
    index = faiss.read_index(index_file)
    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding, top_k)
    chunks = []
    for idx in indices[0]:
        if idx == -1:
            continue
        chunk_file = f"{chunk_dir}/chunk_{idx}.txt"
        with open(chunk_file, 'r', encoding='utf-8') as file:
            chunks.append(file.read())
    
    return chunks


        
