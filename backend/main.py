"""
Backend principal usando Flask.
Funciona localmente e no Render, com suporte a CORS e lazy loading do classificador.
Funcionalidades:
- Health check (/health)
- Processamento de texto (/process)
- Processamento de arquivos (/process-file)
- Rota de teste simples (/)
- Rota para frontend (/app)
- Integração opcional com ChatGPT
- Fallback simulado caso a API falhe
"""

import os
import logging
from flask import Flask, request, jsonify, send_from_directory, abort
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
# Carrega variáveis de ambiente
# -------------------------------
load_dotenv()

# -------------------------------
# Importa módulos internos
# -------------------------------
from response_generator import generate_response
from utils import preprocess_text, extract_text_from_file

# -------------------------------
# Detecta se está rodando no Render
# -------------------------------
RENDER_PORT = os.getenv("PORT")
IS_RENDER = RENDER_PORT is not None

# -------------------------------
# Inicializa Flask
# -------------------------------
app = Flask(__name__)

# Limite global de upload (protege CPU/memória)
app.config["MAX_CONTENT_LENGTH"] = int(os.getenv("MAX_CONTENT_LENGTH_MB", "5")) * 1024 * 1024

# -------------------------------
# Configura CORS (ajuste mínimo, correto)
# - Sem credenciais (você não usa cookies/sessão)
# - Origens comuns em dev + produção
# - Você pode sobrescrever por env: FRONTEND_ORIGINS="https://seu-front.onrender.com,https://outro"
# -------------------------------
FRONTEND_ORIGINS_ENV = os.getenv("FRONTEND_ORIGINS", "")
frontend_origins = [o.strip() for o in FRONTEND_ORIGINS_ENV.split(",") if o.strip()] or [
    "http://127.0.0.1:5000",
    "http://localhost:5000",
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "https://email-classificacao.onrender.com"
]

CORS(
    app,
    resources={
        r"/process": {"origins": frontend_origins},
        r"/process-file": {"origins": frontend_origins},
        r"/health": {"origins": frontend_origins},
        r"/": {"origins": frontend_origins},
        r"/app*": {"origins": frontend_origins},
    },
    supports_credentials=False,  # importante: desativa modo "credenciais"
    allow_headers=["Content-Type", "Authorization"],
    methods=["GET", "POST", "OPTIONS"],
    max_age=600,  # cache do preflight
)

# Log útil para depurar origem real recebida
@app.before_request
def _debug_origin():
    if request.method == "OPTIONS":
        logger.info(f"[CORS] Preflight de {request.headers.get('Origin')} -> {request.path}")
    elif request.path in ("/process", "/process-file", "/health"):
        logger.info(f"[CORS] Origin recebido: {request.headers.get('Origin')} -> {request.path}")

# -------------------------------
# Caminho para frontend
# -------------------------------
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../frontend"))
logger.info(f"Frontend dir: {FRONTEND_DIR} (exists={os.path.isdir(FRONTEND_DIR)})")

# -------------------------------
# Favicon (opcional)
# -------------------------------
@app.get("/favicon.ico")
def favicon():
    if not os.path.isdir(FRONTEND_DIR):
        abort(404)
    return send_from_directory(FRONTEND_DIR, "favicon.ico")

# -------------------------------
# Lazy loading do classificador
# -------------------------------
classifier = None
def get_classifier():
    """
    Retorna instância do EmailClassifier.
    Carrega apenas na primeira requisição para reduzir uso de memória/CPU no Render.
    """
    global classifier
    if classifier is None:
        from classifier import EmailClassifier
        # Mantém seu modelo padrão (se for pesado, considere variável de ambiente p/ alternar)
        classifier = EmailClassifier(model_name="facebook/distilbart-large-mnli")
    return classifier

# -------------------------------
# Rota de teste simples
# -------------------------------
@app.get("/")
def index():
    """Rota de teste para verificar se o backend está ativo."""
    return "Backend ativo! Use /process, /process-file ou /app.", 200

# -------------------------------
# Rotas do frontend
# -------------------------------
@app.get("/app")
def app_index():
    """Retorna página principal do frontend"""
    if not os.path.isdir(FRONTEND_DIR):
        return "Frontend não encontrado.", 404
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.get("/app/<path:path>")
def serve_front(path):
    """Retorna arquivos estáticos do frontend"""
    if not os.path.isdir(FRONTEND_DIR):
        return "Frontend não encontrado.", 404
    return send_from_directory(FRONTEND_DIR, path)

# -------------------------------
# Health check
# -------------------------------
@app.get("/health")
def health():
    """
    Verifica status do backend e se o modelo está carregado.
    Útil para monitoramento e testes.
    """
    cls = get_classifier()
    return jsonify({"status": "ok", "model_loaded": cls.model_loaded}), 200

# -------------------------------
# Endpoint para processar texto
# -------------------------------
@app.post("/process")
def process_text():
    """
    Recebe JSON com campo 'text', pré-processa, classifica
    e retorna categoria, scores e resposta sugerida.
    """
    data = request.get_json(force=True) or {}
    text = (data.get("text") or "").strip()

    if not text:
        return jsonify({"error": "Campo 'text' vazio ou ausente."}), 400

    # Pré-processamento leve
    processed = preprocess_text(text)

    # Classificação lazy
    cls = get_classifier()
    label, scores = cls.classify(text)

    # Gera resposta (ChatGPT ou simulado)
    try:
        reply = generate_response(label, original_text=text, use_chatgpt=True)
    except Exception:
        reply = f"[SIMULADO] Seu texto foi classificado como '{label}'."

    return jsonify({
        "category": label,
        "scores": scores,
        "suggested_response": reply,
        "preprocessed": processed
    }), 200

# -------------------------------
# Endpoint para processar arquivos
# -------------------------------
@app.post("/process-file")
def process_file():
    """
    Recebe arquivo, extrai texto, pré-processa, classifica
    e retorna categoria, scores e resposta sugerida.
    """
    if 'file' not in request.files:
        return jsonify({"error": "Envie um arquivo no campo 'file'."}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nome de arquivo vazio."}), 400

    # Extrai texto do arquivo
    try:
        text = extract_text_from_file(file)
    except Exception as e:
        return jsonify({"error": f"Falha ao ler arquivo: {e}"}), 500

    if not text.strip():
        return jsonify({"error": "Não foi possível extrair texto do arquivo."}), 400

    # Pré-processamento
    processed = preprocess_text(text)

    # Classificação lazy
    cls = get_classifier()
    label, scores = cls.classify(text)

    # Gera resposta (ChatGPT ou simulado)
    try:
        reply = generate_response(label, original_text=text, use_chatgpt=True)
    except Exception:
        reply = f"[SIMULADO] Seu texto foi classificado como '{label}'."

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
    debug = not IS_RENDER
    logger.info(f"Rodando backend em {host}:{port} (Render={IS_RENDER})")
    app.run(host=host, port=port, debug=debug)
