#  Classificador de E-mails – AutoU Challenge

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Licença](https://img.shields.io/badge/Licença-MIT-green)
![Status](https://img.shields.io/badge/Status-Concluído-brightgreen)

Classificação de e-mails em **Produtivo** ou **Improdutivo**, com **resposta automática** e interface web interativa.  
Demonstração de **IA aplicada a texto**, boas práticas de desenvolvimento e deploy em nuvem.


##  Demonstração

![Demonstração do Classificador](https://media.giphy.com/media/3o7TKy0LzZpRXgQy3O/giphy.gif)  
> GIF ilustrativo do upload de e-mails e exibição da categoria/resposta.


## 🔹 Funcionalidades

- Upload de arquivos `.txt` ou `.pdf` ou inserção direta de texto.
- Classificação automática: *Produtivo* / *Improdutivo*.
- Sugestão de resposta automática baseada na categoria.
- Interface web simples e intuitiva.
- Deploy em nuvem com link público funcional (Render).


## 🛠 Tecnologias Utilizadas

- Python 3.10+
- Flask (ou FastAPI) para backend web
- HTML/CSS/JS para frontend
- OpenAI GPT ou Hugging Face Transformers para NLP
- Pip / Virtualenv
- Deploy em [Render](https://render.com)


### Estrutura de Arquivos

```text
email_classifier/
│
├─ main.py                  # Arquivo principal do backend
├─ email_classifier/        # Módulos de processamento e classificação
│   └─ classifier.py
├─ templates/               # HTML da interface
│   └─ index.html
├─ static/                  # CSS, JS, imagens
├─ requirements.txt         # Dependências do projeto
├─ .gitignore               # Ignora arquivos sensíveis e venv
├─ README.md                # Este arquivo
├─ .env                     # Variáveis de ambiente (não versionar)
└─ venv/                    # Ambiente virtual (não versionar)

Pré-requisitos

Python 3.10+

Pip

Chave da OpenAI

Navegador moderno

### Configuração do Ambiente
1. Criar e ativar ambiente virtual
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

2. Instalar dependências
pip install -r requirements.txt

3. Configurar chave da OpenAI

Crie .env na raiz do projeto:

OPENAI_API_KEY=sua_chave_openai_aqui


Nunca versionar .env no GitHub.

Alternativamente, configurar como variável de ambiente:

# Windows
setx OPENAI_API_KEY "sua_chave_openai_aqui"
# Mac/Linux
export OPENAI_API_KEY="sua_chave_openai_aqui"

###Executando o Projeto Localmente
python main.py


Abra no navegador http://localhost:5000.

Faça upload ou insira o texto do e-mail.

Confira categoria e sugestão de resposta automática.

#### Deploy em Nuvem (Render)

A aplicação está hospedada na plataforma Render, que permite deploy rápido, seguro e gratuito, com integração contínua ao GitHub.

Plataforma: Render

Link funcional:

https://seu-projeto.onrender.com

Vantagens do Deploy no Render

SSL automático e subdomínio próprio.

Deploy contínuo via GitHub.

Fácil escalabilidade e manutenção.

Ambiente seguro sem exposição de variáveis sensíveis.

### Atualizando Dependências
pip install <pacote>
pip freeze > requirements.txt

### Boas Práticas

Não versionar .env ou venv.

Modularidade no backend.

README completo e claro.

Projeto reprodutível por qualquer usuário.
### Como Contribuir

Faça fork do repositório.

Crie uma branch para sua feature:

git checkout -b minha-feature


Faça commit das alterações:

git commit -m "Minha feature"


Envie para o repositório remoto:

git push origin minha-feature


Abra um Pull Request detalhando a alteração.

###Referências

Documentação Python

OpenAI API

Hugging Face Transformers

GitHub Secret Scanning

~###Licença

MIT License. Consulte o arquivo LICENSE no repositório.

#### Entregáveis

Código Fonte completo no GitHub:

Scripts Python (.py, .ipynb)

HTML/CSS/JS

requirements.txt

Dados de exemplo (se necessário)

README detalhado

Estrutura organizada

Link da aplicação hospedada em nuvem (Render), funcional e acessível publicamente
