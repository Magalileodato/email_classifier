# backend/utils.py

"""
Funções auxiliares para manipulação de emails e pré-processamento de texto.
Inclui:
- preprocess_text: limpeza e normalização de texto
- extract_text_from_file: extrai texto de arquivos .txt e .pdf
"""

import re
import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from PyPDF2 import PdfReader

# -------------------------------
# Inicialização de ferramentas
# -------------------------------

# Stemmer (reduz palavras à raiz)
stemmer = PorterStemmer()

# Stopwords em inglês (palavras comuns a remover)
stop_words = set(stopwords.words('english'))

# -------------------------------
# Função de pré-processamento
# -------------------------------
def preprocess_text(text: str) -> str:
    """
    Pré-processa o texto do email:
    - Converte para minúsculas
    - Remove pontuação
    - Remove números
    - Remove stopwords
    - Aplica stemming (reduz palavras à raiz)

    Args:
        text (str): Texto do email

    Returns:
        str: Texto processado
    """
    # 1) Converte para minúsculas
    text = text.lower()

    # 2) Remove pontuação
    text = text.translate(str.maketrans("", "", string.punctuation))

    # 3) Remove números
    text = re.sub(r"\d+", "", text)

    # 4) Tokeniza, remove stopwords e aplica stemming
    words = text.split()
    processed = [stemmer.stem(word) for word in words if word not in stop_words]

    # 5) Reconstrói o texto processado
    return " ".join(processed)

# -------------------------------
# Função para extrair texto de arquivos
# -------------------------------
def extract_text_from_file(file) -> str:
    """
    Extrai texto de arquivos .txt e .pdf enviados via Flask (FileStorage).
    Args:
        file: objeto do Flask (request.files['file'])

    Returns:
        str: texto extraído

    Raises:
        ValueError: se tipo de arquivo não suportado
    """
    filename = file.filename.lower()

    if filename.endswith(".txt"):
        # Arquivo .txt
        content = file.read().decode("utf-8", errors="ignore")
        return content

    elif filename.endswith(".pdf"):
        # Arquivo PDF
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text

    else:
        raise ValueError("Formato de arquivo não suportado. Use .txt ou .pdf")
