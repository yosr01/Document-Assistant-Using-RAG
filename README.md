# Document-Assistant-Using-RAG

This project implements a chat application that uses a RAG system with the pre-trained **Mistral-7B** model and an interactive user interface built using **Streamlit**.

## Prerequisites
Before starting, make sure you have installed the required libraries. You can install the dependencies using `requirements.txt`.

    ```bash
    pip install -r requirements.txt
    ```

## Steps :

1. **Set up your Hugging Face API key** :
    - Go to the [Hugging Face ](https://huggingface.co) website and log in to your account.
    - Click on your profile in the top right corner then navigate to **Settings -> Access Tokens** and generate a new API key

2. **Add the API key to the code** :
    Open the  `generation.py` file (stored under /scripts) and insert your API key in the designated place (line 7) :
    
    ```python
    api_key = 'INSERT_API_KEY'
    ```
3. **Running the project** :
    To start the application, run the following command in your terminal: :
   
    ```bash
    python -m streamlit run generation.py
    ```
    
    This will launch your browser and you'll be all set to start chatting with the bot about French laws!

---

