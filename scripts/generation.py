import streamlit as st
from huggingface_hub import InferenceClient
from preprocess import preprocess_document
from embedding import create_embeddings
from retrieve import retrieve_chunks

api_key = 'Api_key'
model_name = 'mistralai/Mistral-7B-Instruct-v0.3'
client = InferenceClient(model=model_name, token=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Posez votre question ou donnez une instruction:")

if prompt is not None and prompt.strip() == "":
    st.warning("Vous ne pouvez pas envoyer un message vide. Veuillez entrer un texte.")
else:
    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)

        st.session_state.messages.append({"role": "user", "content": prompt})

        try:
            retrieved_chunks = retrieve_chunks(prompt, "embeddings/index.faiss", "data/chunks")
            if not retrieved_chunks:
                retrieved_context = "Aucune information pertinente n'a été trouvée pour votre requête."
            else:
                retrieved_context = "\n\n".join(retrieved_chunks[:3])  # Combine the top 3 retrieved chunks
        except Exception as e:
            retrieved_context = f"Erreur lors de la récupération des informations : {str(e)}"

        prompt_input = f"""
        <s>[INST]
        You are an AI assistant specialized in French legal texts. The user has asked the following question:
        "{prompt}"
        Here is the relevant context from the legal document:
        {retrieved_context}
        
        Please generate a helpful and accurate response based on the provided context.
        [/INST]
        """

        result = client.text_generation(
            prompt=prompt_input,
            max_new_tokens=500,  
            temperature=0.1,     
            top_p=0.9,
            top_k=40
        )

        assistant_response = result if isinstance(result, str) else "Désolé, je n'ai pas pu générer une réponse."

        with st.chat_message("assistant"):
            st.markdown(assistant_response)

        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
