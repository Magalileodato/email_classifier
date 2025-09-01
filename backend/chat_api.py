"""
Módulo para integração com a API do ChatGPT (OpenAI)
Gera respostas automáticas usando inteligência artificial.
"""

import os
import openai
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env (por exemplo, OPENAI_API_KEY)
load_dotenv()

# Configura a chave da API a partir da variável de ambiente
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_chat_response(email_text: str, model: str = "gpt-3.5-turbo") -> str:
    """
    Gera uma resposta usando a API ChatGPT.

    Args:
        email_text (str): Texto do email para gerar a resposta
        model (str): Modelo a ser usado (padrão "gpt-3.5-turbo")

    Returns:
        str: Texto da resposta gerada pelo ChatGPT
    """
    if not openai.api_key:
        # Caso a chave não esteja configurada
        return "API Key não configurada. Configure OPENAI_API_KEY no arquivo .env"

    try:
        # Chamando a API de chat
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "Você é um assistente que responde emails de forma clara e cordial."},
                {"role": "user", "content": email_text}
            ],
            temperature=0.5,  # Grau de criatividade da resposta
            max_tokens=200    # Limite de tamanho da resposta
        )

        # Extrai a mensagem do ChatGPT
        message = response.choices[0].message.content.strip()
        return message

    except Exception as e:
        # Retorna erro em formato legível
        return f"Falha ao gerar resposta via ChatGPT: {e}"

