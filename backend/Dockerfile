# Imagem base Python
FROM python:3.11-slim

# Diretório de trabalho
WORKDIR /app

# Copia e instala dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o projeto
COPY . .

# Expõe a porta que o Render define via variável $PORT
EXPOSE $PORT

# Comando para iniciar o app
# main.py deve ter "app = Flask(__name__)"
CMD ["sh", "-c", "gunicorn main:app --bind 0.0.0.0:$PORT"]
