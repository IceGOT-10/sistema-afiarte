# 🛠️ Sistema Afiarte

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/ORM-SQLAlchemy-D71F00?style=flat-square&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![JavaScript](https://img.shields.io/badge/Frontend-JS%20%7C%20HTML5%20%7C%20CSS3-F7DF1E?style=flat-square&logo=javascript&logoColor=black)](https://developer.mozilla.org/)

O **Sistema Afiarte** é uma aplicação Full Stack desenvolvida para gestão operacional e controle de serviços/produtos da Afiarte. O sistema oferece uma API RESTful robusta construída com FastAPI e SQLAlchemy no backend, acompanhada por uma interface web simples, responsiva e dinâmica no frontend.

---

## 📌 Sumário
- [Recursos Principais](#-recursos-principais)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Como Executar o Projeto](#-como-executar-o-projeto)
  - [Pré-requisitos](#pré-requisitos)
  - [Passo 1: Configuração do Backend](#passo-1-configuração-do-backend)
  - [Passo 2: Populando o Banco de Dados (Seed)](#passo-2-populando-o-banco-de-dados-seed)
  - [Passo 3: Execução do Frontend](#passo-3-execução-do-frontend)
- [Documentação da API](#-documentação-da-api)
- [Autor](#-autor)

---

## ✨ Recursos Principais

- 🚀 **API RESTful de Alta Performance:** Desenvolvida com FastAPI e validação de dados via Pydantic.
- 🗄️ **Mapeamento Objeto-Relacional (ORM):** Gerenciamento e persistência de dados com SQLAlchemy.
- 🌾 **População Automatizada (Seed Data):** Script inclusivo para popular o banco de dados com dados iniciais de teste/produção.
- 💻 **Interface Web Dinâmica:** Frontend construído com HTML5, CSS3 e JavaScript assíncrono (`fetch` API).
- 📑 **Documentação Interativa:** Documentação OpenAPI/Swagger gerada automaticamente.

---

## 🛠️ Tecnologias Utilizadas

### **Backend**
- **Linguagem:** Python 3.9+
- **Framework Web:** [FastAPI](https://fastapi.tiangolo.com/)
- **Servidor ASGI:** [Uvicorn](https://www.uvicorn.org/)
- **ORM:** [SQLAlchemy](https://www.sqlalchemy.org/)
- **Validação de Dados:** [Pydantic](https://docs.pydantic.dev/)
- **Banco de Dados:** SQLite (padrão de desenvolvimento) / PostgreSQL

### **Frontend**
- **Estrutura & Estilização:** HTML5 & CSS3
- **Lógica de Cliente:** JavaScript (ES6+)

---

## 📁 Estrutura do Projeto

```text
sistema-afiarte/
│
├── backend/
│   ├── database.py       # Configuração e conexão com o Banco de Dados
│   ├── main.py           # Ponto de entrada da aplicação FastAPI e rotas
│   ├── models.py         # Modelos das tabelas do ORM (SQLAlchemy)
│   ├── schemas.py        # Schemas de validação e conversão (Pydantic)
│   ├── seed.py           # Script para inserção de dados iniciais no banco
│   └── requirements.txt  # Dependências do projeto Python
│
├── frontend/
│   ├── app.js            # Lógica de integração com a API Backend
│   ├── index.html        # Página principal da interface de usuário
│   └── styles.css        # Estilização visual do sistema
│
└── .gitignore            # Arquivos e pastas ignorados pelo Git
```
🚀 Como Executar o Projeto
Pré-requisitos
Certifique-se de ter instalado em sua máquina:

Python 3.9+

Git

Um navegador web moderno (Chrome, Firefox, Edge, Safari)

Passo 1: Configuração do Backend
Clone o repositório:

Bash
git clone [https://github.com/IceGOT-10/sistema-afiarte.git](https://github.com/IceGOT-10/sistema-afiarte.git)
cd sistema-afiarte
Acesse o diretório do backend:

Bash
cd backend
Crie e ative um ambiente virtual (recomendado):

Linux/macOS:

Bash
python3 -m venv venv
source venv/bin/activate
Windows:

Bash
python -m venv venv
.\venv\Scripts\activate
Instale as dependências:

Bash
pip install -r requirements.txt
Inicie o servidor de desenvolvimento:

Bash
uvicorn main:app --reload
O backend estará rodando em: http://127.0.0.1:8000

Passo 2: Populando o Banco de Dados (Seed)
Para popular o banco de dados com dados iniciais/fictícios para testes, execute o script seed.py no terminal (com o ambiente virtual ativado e dentro da pasta backend):

Bash
python seed.py
Passo 3: Execução do Frontend
Como o frontend é composto por arquivos estáticos (HTML, CSS, JS), você pode executá-lo de duas formas:

Via Extensão Live Server (VS Code):

Abra a pasta frontend no VS Code.

Clique com o botão direito no arquivo index.html e selecione "Open with Live Server".

Diretamente no Navegador:

Abra a pasta frontend no seu navegador de preferência clicando duas vezes no arquivo index.html.

📖 Documentação da API
Com o servidor backend rodando, a documentação interativa da API estará disponível nos seguintes links:

Swagger UI: http://127.0.0.1:8000/docs

ReDoc: http://127.0.0.1:8000/redoc

👤 Autor
Desenvolvido por Luan Rocha.

GitHub: @IceGOT-10

LinkedIn: in/luanrocha-dev

E-mail: luanfonsecarocha7@gmail.com
