# Imagem base Python
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia e instala dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o projeto para o container
COPY . .

# Expõe a porta (Render define $PORT automaticamente)
EXPOSE 10000

# Comando para iniciar o aplicativo
CMD ["sh", "-c", "gunicorn main:app --bind 0.0.0.0:$PORT"]

