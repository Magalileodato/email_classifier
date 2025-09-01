# 📨 Classificador de E-mails – AutoU Challenge

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Flask](https://img.shields.io/badge/Flask-Backend-orange)
![Status](https://img.shields.io/badge/Status-Concluído-brightgreen)
![License](https://img.shields.io/badge/License-MIT-green)

Classificação de e-mails em **Produtivo / Improdutivo**, com **resposta automática**, interface web interativa e deploy em nuvem.  
Funciona **localmente** e em **Render**.


## 🎬 Demonstração Visual

![GIF Demonstração](assets/demo.gif)  
> GIF ilustrativo mostrando upload de e-mails e exibição da categoria/resposta.

> ⚠️ Caso a OpenAI API não esteja disponível ou a quota seja excedida, o backend usa **resposta simulada** garantindo funcionalidade completa.


## 🔹 Funcionalidades Principais

- 📄 Upload de arquivos `.txt` ou `.pdf` ou inserção direta de texto  
- ⚡ Classificação automática: **Produtivo / Improdutivo**  
- 🤖 Resposta automática via ChatGPT ou **fallback simulado**  
- 💻 Interface web simples e intuitiva  
- ☁️ Deploy público funcional em Render  


## 🧪 Teste Rápido do Backend

### 1️⃣ Testar texto direto

```bash
curl -X POST http://localhost:5000/process \
-H "Content-Type: application/json" \
-d '{"text": "Preciso de ajuda com o relatório"}'
2️⃣ Testar arquivo .txt ou .pdf
bash
Copiar código
curl -X POST http://localhost:5000/process-file \
-F "file=@/c/Users/magal/Desktop/exemplo.txt"
Exemplo de resposta (simulada):

json
Copiar código
{
  "category": "Produtivo",
  "preprocessed": "texto limpo",
  "scores": {"Improdutivo": 0.34, "Produtivo": 0.66},
  "suggested_response": "[SIMULADO] Seu texto foi classificado como 'Produtivo'."
}
⚙️ Configuração Rápida
bash
Copiar código
# Criar e ativar ambiente virtual
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Configurar chave OpenAI (opcional)
echo "OPENAI_API_KEY=sua_chave_openai_aqui" > .env

# Executar backend
python main.py
Acesse: http://localhost:5000

☁️ Deploy Render
🔒 SSL automático e subdomínio próprio

🔄 Deploy contínuo via GitHub

🌐 Link funcional: https://seu-projeto.onrender.com

📝 Boas Práticas
❌ Não versionar .env ou venv

🧩 Modularidade no backend

📚 README claro e organizado

🔄 Projeto reprodutível por qualquer usuário

🤝 Como Contribuir
bash
Copiar código
# Fork do repositório
git clone <seu-repo>
cd <seu-repo>

# Criar branch para nova feature
git checkout -b minha-feature

# Commit e push
git commit -m "Minha feature"
git push origin minha-feature

# Abrir Pull Request
📚 Referências
Documentação Python

OpenAI API

Hugging Face Transformers

GitHub Secret Scanning

🏆 Entregáveis
Código fonte completo (.py, .ipynb)

HTML/CSS/JS do frontend

requirements.txt


README detalhado e organizado

Link da aplicação hospedada em nuvem (Render)