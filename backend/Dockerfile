# Imagem base Python
FROM python:3.11-slim

# Define diretório de trabalho
WORKDIR /app

# Copia e instala dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o backend
COPY . .

# Porta usada pelo Gunicorn
EXPOSE 5000

# Comando para iniciar o app
CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:5000"]
nicorn", "-b", "0.0.0.0:10000", "main:app"]
