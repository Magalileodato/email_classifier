"""
Módulo responsável por gerar respostas automáticas para emails.
Suporta duas opções:
1) Fallback com respostas pré-definidas.
2) Integração com ChatGPT (opcional) via API.
"""

import os
import random

# Se desejar usar ChatGPT, importa a função do módulo chat_api
try:
    from chat_api import generate_chat_response
    CHATGPT_AVAILABLE = True
except ImportError:
    CHATGPT_AVAILABLE = False

# Respostas pré-definidas por categoria (fallback)
PREDEFINED_RESPONSES = {
    "Produtivo": [
        "Olá, obrigado pelo contato! Estamos analisando sua solicitação e retornaremos em breve.",
        "Recebemos seu email e já estamos trabalhando na sua demanda. Entraremos em contato com atualizações."
    ],
    "Improdutivo": [
        "Obrigado pelo seu email! Tenha um ótimo dia!",
        "Agradecemos a mensagem. Estamos à disposição sempre que precisar."
    ]
}

def generate_response(category: str, original_text: str = "", use_chatgpt: bool = False) -> str:
    """
    Gera uma resposta automática baseada na categoria do email.

    Args:
        category (str): Categoria do email ("Produtivo" ou "Improdutivo").
        original_text (str): Texto original do email (opcional, usado se ChatGPT estiver ativo).
        use_chatgpt (bool): Se True, tenta gerar resposta via ChatGPT; se False, usa fallback.

    Returns:
        str: Resposta automática apropriada.
    """

    # --- 1) Checa se categoria é válida ---
    if category not in PREDEFINED_RESPONSES:
        return "Não foi possível gerar uma resposta automática para este email."

    # --- 2) Tenta usar ChatGPT se estiver disponível e habilitado ---
    if use_chatgpt and CHATGPT_AVAILABLE and original_text.strip():
        try:
            # Passa apenas o texto do email para a função do chat_api
            reply = generate_chat_response(original_text)
            if reply:
                return reply
        except Exception as e:
            # Caso falhe, cai para fallback e loga o erro
            print(f"[response_generator] Falha ao gerar resposta via ChatGPT: {e}")

    # --- 3) Fallback: seleciona aleatoriamente uma resposta pré-definida ---
    response = random.choice(PREDEFINED_RESPONSES[category])
    return response


# -------------------------------
# Testes rápidos do módulo
# -------------------------------
if __name__ == "__main__":
    print("Teste fallback Produtivo:", generate_response("Produtivo", "Exemplo de email"))
    print("Teste fallback Improdutivo:", generate_response("Improdutivo", "Exemplo de email"))
    print("Teste categoria inválida:", generate_response("Outro", "Exemplo de email"))
