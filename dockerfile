FROM python:3.9

RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501
CMD ["streamlit", "run", "scripts/generation.py", "--server.port=8501", "--server.enableCORS=false"]
