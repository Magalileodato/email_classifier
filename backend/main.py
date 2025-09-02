"""
Backend principal usando Flask.
Funciona tanto localmente quanto no Render.

Funcionalidades:
- Health check (/health)
- Processamento de texto (/process)
- Processamento de arquivos (/process-file)
- Rota de teste simples (/)
- Rota para frontend (/app)
- Integração com ChatGPT via OpenAI API (usando variável de ambiente)
- Fallback simulado caso a API falhe
- Suporte a CORS para permitir chamadas do frontend
"""

import os
import logging
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv
from flask_cors import CORS

# -------------------------------
# Configuração de logging
# -------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# -------------------------------
# Carrega variáveis do arquivo .env
# -------------------------------
load_dotenv()  # Certifique-se de ter OPENAI_API_KEY definida

# -------------------------------
# Importa módulos internos
# -------------------------------
from response_generator import generate_response
from utils import preprocess_text, extract_text_from_file

# -------------------------------
# Inicializa Flask
# -------------------------------
app = Flask(__name__)

# -------------------------------
# Lazy loading do classificador
# -------------------------------
classifier = None

def get_classifier():
    """
    Retorna a instância do EmailClassifier.
    Carrega apenas na primeira requisição (lazy loading)
    e usa modelo menor para reduzir memória.
    """
    global classifier
    if classifier is None:
        from classifier import EmailClassifier
        classifier = EmailClassifier(model_name="facebook/distilbart-large-mnli")  # modelo leve
    return classifier

# -------------------------------
# Detecta ambiente de execução
# -------------------------------
RENDER_PORT = os.getenv("PORT")   # Se existir, estamos no Render
IS_RENDER = RENDER_PORT is not None

# -------------------------------
# Configura CORS para frontend local e produção
# -------------------------------
frontend_origins = [
    "http://127.0.0.1:5500",          # Frontend local
    "https://SEU_FRONTEND_DOMINIO.com" # Frontend produção
]

CORS(
    app,
    resources={r"/*": {"origins": frontend_origins}},
    supports_credentials=True,
    methods=["GET", "POST", "OPTIONS"]
)

# -------------------------------
# Rotas OPTIONS para preflight (CORS)
# -------------------------------
@app.route("/process", methods=["OPTIONS"])
@app.route("/process-file", methods=["OPTIONS"])
def handle_options():
    """Responde às requisições OPTIONS enviadas pelo navegador."""
    return "", 200

# -------------------------------
# Rota de teste simples /
# -------------------------------
@app.get("/")
def index():
    return "Backend ativo! Use /process, /process-file ou /app para frontend.", 200

# -------------------------------
# Rota para servir frontend
# -------------------------------
@app.get("/app")
def app_index():
    """
    Serve arquivo index.html do frontend.
    Caminho relativo: backend/main.py -> ../front/index.html
    """
    return send_from_directory("../front", "index.html")

# -------------------------------
# Health check
# -------------------------------
@app.get("/health")
def health():
    cls = get_classifier()
    return jsonify({
        "status": "ok",
        "model_loaded": cls.model_loaded
    }), 200

# -------------------------------
# Endpoint para processar texto
# -------------------------------
@app.post("/process")
def process_text():
    logger.info(f"Request data: {request.data}")

    data = request.get_json(force=True) or {}
    text = (data.get("text") or "").strip()

    if not text:
        logger.warning("Campo 'text' vazio ou ausente.")
        return jsonify({"error": "Campo 'text' vazio ou ausente."}), 400

    processed = preprocess_text(text)
    cls = get_classifier()
    label, scores = cls.classify(text)

    try:
        reply = generate_response(label, original_text=text, use_chatgpt=True)
    except Exception as e:
        reply = f"[SIMULADO] Seu texto foi classificado como '{label}'."
        logger.warning(f"Falha ao gerar resposta via ChatGPT: {e}")

    return jsonify({
        "category": label,
        "scores": scores,
        "suggested_response": reply,
        "preprocessed": processed
    }), 200

# -------------------------------
# Endpoint para processar arquivos (.txt ou .pdf)
# -------------------------------
@app.post("/process-file")
def process_file():
    if 'file' not in request.files:
        logger.warning("Arquivo não enviado no campo 'file'.")
        return jsonify({"error": "Envie um arquivo no campo 'file'."}), 400

    file = request.files['file']
    if file.filename == '':
        logger.warning("Nome de arquivo vazio.")
        return jsonify({"error": "Nome de arquivo vazio."}), 400

    try:
        text = extract_text_from_file(file)
    except Exception as e:
        logger.error(f"Falha ao ler arquivo: {e}")
        return jsonify({"error": f"Falha ao ler arquivo: {e}"}), 500

    if not text.strip():
        logger.warning("Não foi possível extrair texto do arquivo.")
        return jsonify({"error": "Não foi possível extrair texto do arquivo."}), 400

    processed = preprocess_text(text)
    cls = get_classifier()
    label, scores = cls.classify(text)

    try:
        reply = generate_response(label, original_text=text, use_chatgpt=True)
    except Exception as e:
        reply = f"[SIMULADO] Seu texto foi classificado como '{label}'."
        logger.warning(f"Falha ao gerar resposta via ChatGPT: {e}")

    return jsonify({
        "category": label,
        "scores": scores,
        "suggested_response": reply,
        "preprocessed": processed
    }), 200

# -------------------------------
# Inicialização do servidor
# -------------------------------
if __name__ == "__main__":
    port = int(RENDER_PORT) if IS_RENDER else 5000
    host = "0.0.0.0" if IS_RENDER else "127.0.0.1"
    debug = False if IS_RENDER else True

    logger.info(f"Rodando backend em {host}:{port} (Render={IS_RENDER})")
    app.run(host=host, port=port, debug=debug)

