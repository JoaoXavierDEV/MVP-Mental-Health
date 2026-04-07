# Saúde Mental no Ambiente de Trabalho — MVP

Aplicação web para predição de necessidade de tratamento de saúde mental em profissionais de tecnologia, utilizando um modelo de Machine Learning treinado com dados reais.

## Sobre o Projeto

Este MVP foi desenvolvido como parte da disciplina **Qualidade de Software, Segurança e Sistemas Inteligentes** da **PUC-Rio**. A aplicação permite cadastrar perfis de profissionais e, com base em fatores como histórico familiar, ambiente de trabalho e percepções sobre saúde mental, prever se a pessoa pode se beneficiar de tratamento.

## Arquitetura

```
mvp/
├── api/                        # Back-end (Flask)
│   ├── app.py                  # Rotas e lógica da API
│   ├── logger.py               # Configuração de logging
│   ├── requirements.txt        # Dependências Python
│   ├── model/                  # Modelos SQLAlchemy e pipeline de ML
│   ├── schemas/                # Schemas de validação (Pydantic)
│   ├── MachineLearning/        # Notebooks, pipelines e modelos treinados
│   └── test_modelos.py         # Testes do modelo de ML
├── database/                   # Banco de dados SQLite (usuarios.sqlite3)
├── front/                      # Front-end (HTML, CSS, JS)
│   ├── index.html
│   ├── styles.css
│   ├── scripts.js
│   └── img/
└── log/                        # Logs da aplicação
```

## Tecnologias Utilizadas

- **Back-end:** Python, Flask, Flask-OpenAPI3, SQLAlchemy
- **Front-end:** HTML, CSS, JavaScript
- **Machine Learning:** scikit-learn, pandas, numpy
- **Banco de Dados:** SQLite

## Como Executar

### Pré-requisitos

- Python 3.10+

### Instalação

1. Clone o repositório:
   ```bash
   git clone <url-do-repositorio>
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/Mac
   .venv\Scripts\activate      # Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r api/requirements.txt
   ```

### Execução

```bash
cd api
python app.py
```

A aplicação estará disponível em `http://127.0.0.1:5000`.

## Funcionalidades

- **Cadastro de perfis** com informações demográficas, profissionais e de percepção sobre saúde mental.
- **Predição automática** via modelo de ML indicando se o profissional pode se beneficiar de tratamento.
- **Listagem** de todos os registros cadastrados.
- **Busca** de registro por nome.
- **Remoção** de registros.

## API Endpoints

| Método   | Rota         | Descrição                           |
|----------|--------------|--------------------------------------|
| `GET`    | `/`          | Interface web principal              |
| `POST`   | `/paciente`  | Cadastra paciente e realiza predição |
| `GET`    | `/pacientes` | Lista todos os pacientes             |
| `GET`    | `/paciente`  | Busca paciente por nome              |
| `DELETE` | `/paciente`  | Remove paciente por nome             |

## Testes

```bash
cd api
pytest test_modelos.py
```
