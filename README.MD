# Saude Mental no Ambiente de Trabalho — MVP

Aplicacao web para predicao de necessidade de tratamento de saude mental em profissionais de tecnologia, utilizando um modelo de Machine Learning treinado com dados reais.

## Sobre o Projeto

Este MVP foi desenvolvido como parte da disciplina **Qualidade de Software, Seguranca e Sistemas Inteligentes** da **PUC-Rio**. A aplicacao permite cadastrar perfis de profissionais e, com base em fatores como historico familiar, ambiente de trabalho e percepcoes sobre saude mental, prever se a pessoa pode se beneficiar de tratamento.

## Arquitetura

```
mvp/
├── api/                        # Back-end (Flask)
│   ├── app.py                  # Rotas e logica da API
│   ├── logger.py               # Configuracao de logging
│   ├── requirements.txt        # Dependencias Python
│   ├── model/                  # Modelos SQLAlchemy e pipeline de ML
│   ├── schemas/                # Schemas de validacao (Pydantic)
│   ├── MachineLearning/        # Notebooks, pipelines e modelos treinados
│   └── test_modelos.py         # Testes do modelo de ML
├── database/                   # Banco de dados SQLite (usuarios.sqlite3)
├── front/                      # Front-end (HTML, CSS, JS)
│   ├── index.html
│   ├── styles.css
│   ├── scripts.js
│   └── img/
└── log/                        # Logs da aplicacao
```

## Tecnologias Utilizadas

- **Back-end:** Python, Flask, Flask-OpenAPI3, SQLAlchemy
- **Front-end:** HTML, CSS, JavaScript
- **Machine Learning:** scikit-learn, pandas, numpy
- **Banco de Dados:** SQLite

## Como Executar

### Pre-requisitos

- Python 3.10+

### Instalacao

1. Clone o repositorio:
   ```bash
   git clone <url-do-repositorio>
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/Mac
   .venv\Scripts\activate      # Windows
   ```

3. Instale as dependencias:
   ```bash
   pip install -r api/requirements.txt
   ```

### Execucao

```bash
cd api
python app.py
```

A aplicacao estara disponivel em `http://127.0.0.1:5000`.

## Funcionalidades

- **Cadastro de perfis** com informacoes demograficas, profissionais e de percepcao sobre saude mental
- **Predicao automatica** via modelo de ML indicando se o profissional pode se beneficiar de tratamento
- **Listagem** de todos os registros cadastrados
- **Busca** de registro por nome
- **Remocao** de registros

## API Endpoints

| Metodo   | Rota         | Descricao                          |
|----------|--------------|-------------------------------------|
| `GET`    | `/`          | Interface web principal             |
| `POST`   | `/paciente`  | Cadastra paciente e realiza predicao|
| `GET`    | `/pacientes` | Lista todos os pacientes            |
| `GET`    | `/paciente`  | Busca paciente por nome             |
| `DELETE` | `/paciente`  | Remove paciente por nome            |

## Testes

```bash
cd api
pytest test_modelos.py
```
