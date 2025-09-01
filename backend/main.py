# backend/main.py

"""
Backend principal usando Flask.
Funciona tanto localmente quanto no Render.

Funcionalidades:
- Health check (/health)
- Processamento de texto (/process)
- Processamento de arquivos (/process-file)
- Rota de teste simples (/)
- Integração com ChatGPT via OpenAI API (usando variável de ambiente)
- Suporte a CORS para permitir chamadas do frontend
"""

import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv       # Para carregar variáveis do arquivo .env
from flask_cors import CORS          # Para permitir requisições do frontend

# -------------------------------
# Carrega variáveis do arquivo .env
# -------------------------------
# Certifique-se de ter OPENAI_API_KEY definida
load_dotenv()

# -------------------------------
# Importa módulos internos
# -------------------------------
from classifier import EmailClassifier            # Classe para classificação de emails
from response_generator import generate_response  # Função que gera resposta automática
from utils import preprocess_text, extract_text_from_file  # Funções auxiliares

# -------------------------------
# Inicializa Flask e o classificador
# -------------------------------
app = Flask(__name__)
classifier = EmailClassifier()  # Cria instância da classe EmailClassifier

# -------------------------------
# Detecta ambiente de execução
# -------------------------------
RENDER_PORT = os.getenv("PORT")   # Se existir, estamos no Render
IS_RENDER = RENDER_PORT is not None

# -------------------------------
# Configura CORS UNIVERSAL
# ===============================
# Permite que qualquer frontend acesse o backend
# Evita erro de CORS tanto local quanto no Render
# OBS: Para produção, você pode restringir a origens específicas
# Ex: origins=["https://meu_frontend.onrender.com"]
CORS(app, resources={r"/*": {"origins": "*"}})

# ===========================
# Rota de teste /
# ===========================
@app.get("/")
def index():
    """
    Rota principal para teste.
    Permite abrir a URL principal no navegador sem dar Not Found.
    """
    return "Backend ativo! Use /process ou /process-file para enviar dados.", 200

# ===========================
# Health check
# ===========================
@app.get("/health")
def health():
    """
    Endpoint para verificar se o backend está ativo.
    Retorna JSON indicando se o classificador está carregado.
    """
    return jsonify({
        "status": "ok",
        "model_loaded": classifier.model_loaded
    }), 200

# ===========================
# Endpoint para processar texto
# ===========================
@app.post("/process")
def process_text():
    """
    Recebe JSON no formato: {"text": "..."}
    
    Passos:
    1) Valida se o campo 'text' existe e não está vazio
    2) Pré-processa o texto (limpeza, normalização, tokenização)
    3) Classifica como "Produtivo" ou "Improdutivo"
    4) Gera resposta automática via ChatGPT (ou fallback)
    5) Retorna JSON com categoria, scores, resposta sugerida e texto pré-processado
    """
    # DEBUG: imprime o corpo recebido
    print("Request data:", request.data)

    # Captura JSON enviado pelo frontend
    data = request.get_json(force=True) or {}
    text = (data.get("text") or "").strip()

    if not text:
        return jsonify({"error": "Campo 'text' vazio ou ausente."}), 400

    # Pré-processa texto
    processed = preprocess_text(text)

    # Classifica texto
    label, scores = classifier.classify(text)

    # Gera resposta
    reply = generate_response(label, original_text=text, use_chatgpt=True)

    # Retorna resultado em JSON
    return jsonify({
        "category": label,
        "scores": scores,
        "suggested_response": reply,
        "preprocessed": processed
    }), 200

# ===========================
# Endpoint para processar arquivos (.txt ou .pdf)
# ===========================
@app.post("/process-file")
def process_file():
    """
    Recebe arquivo via multipart/form-data (campo 'file').
    Suporta arquivos .txt e .pdf.

    Passos:
    1) Valida presença do arquivo
    2) Extrai texto do arquivo
    3) Pré-processa e classifica
    4) Gera resposta via ChatGPT
    5) Retorna JSON com categoria, scores, resposta sugerida e texto pré-processado
    """
    if 'file' not in request.files:
        return jsonify({"error": "Envie um arquivo no campo 'file'."}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nome de arquivo vazio."}), 400

    try:
        # Extrai texto do arquivo
        text = extract_text_from_file(file)
    except Exception as e:
        return jsonify({"error": f"Falha ao ler arquivo: {e}"}), 500

    if not text.strip():
        return jsonify({"error": "Não foi possível extrair texto do arquivo."}), 400

    # Pré-processamento
    processed = preprocess_text(text)

    # Classificação
    label, scores = classifier.classify(text)

    # Geração de resposta
    reply = generate_response(label, original_text=text, use_chatgpt=True)

    # Retorna resultado
    return jsonify({
        "category": label,
        "scores": scores,
        "suggested_response": reply,
        "preprocessed": processed
    }), 200

# ===========================
# Inicialização do servidor
# ===========================
if __name__ == "__main__":
    if IS_RENDER:
        # Produção no Render
        port = int(RENDER_PORT)
        host = "0.0.0.0"
        debug = False
    else:
        # Local
        port = 5000
        host = "127.0.0.1"
        debug = True

    # Executa Flask
    app.run(host=host, port=port, debug=debug)
