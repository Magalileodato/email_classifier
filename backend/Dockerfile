# -------------------------------
# Imagem base Python
# -------------------------------
FROM python:3.11-slim

# -------------------------------
# Diretório de trabalho dentro do container
# -------------------------------
WORKDIR /app

# -------------------------------
# Instala pacotes mínimos do sistema necessários para build
# -------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# -------------------------------
# Copia e instala dependências Python
# -------------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# -------------------------------
# Instala stopwords do nltk (pode ser lazy no código para economizar memória)
# -------------------------------
RUN python -m nltk.downloader stopwords

# -------------------------------
# Copia todo o projeto para o container
# -------------------------------
COPY . .

# -------------------------------
# Expõe a porta que o Render define via variável $PORT
# -------------------------------
EXPOSE $PORT

# -------------------------------
# Comando para iniciar o app com Gunicorn
# - 1 worker e 1 thread para reduzir consumo de memória
# - main.py deve ter "app = Flask(__name__)"
# -------------------------------
CMD ["sh", "-c", "gunicorn main:app --bind 0.0.0.0:$PORT --workers 1 --threads 1"]
