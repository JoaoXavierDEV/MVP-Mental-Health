from pathlib import Path

from flask_openapi3 import OpenAPI, Info, Tag
from flask import send_from_directory
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Paciente, Pipeline, PreProcessador
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Mental Health API", version="1.0.0")
app = OpenAPI(__name__, info=info, doc_ui=False)
CORS(app)

FRONT_DIR = Path(__file__).resolve().parents[1] / "front"

# Tags para documentacao
home_tag = Tag(name="Documentacao",
               description="Selecao de documentacao: Swagger, Redoc ou RapiDoc")
paciente_tag = Tag(name="Paciente",
                   description="Adicao, visualizacao e remocao de pacientes")

# Carrega o modelo e os preprocessadores
pipeline = Pipeline()
modelo = pipeline.carrega_pipeline("MachineLearning/pipelines/pipeline.pkl")

preprocessador = PreProcessador()
preprocessador.carrega_encoders(
    "MachineLearning/models/encoders.pkl",
    "MachineLearning/models/features.pkl"
)


@app.route("/", methods=["GET"])
def home():
    """Serve a interface web principal."""
    return send_from_directory(FRONT_DIR, "index.html")


@app.route("/front/<path:asset_path>", methods=["GET"])
def front_assets(asset_path):
    """Serve arquivos estaticos do front-end."""
    return send_from_directory(FRONT_DIR, asset_path)


@app.route("/styles.css", methods=["GET"])
def styles():
    """Compatibilidade para assets referenciados na raiz."""
    return send_from_directory(FRONT_DIR, "styles.css")


@app.route("/scripts.js", methods=["GET"])
def scripts():
    """Compatibilidade para assets referenciados na raiz."""
    return send_from_directory(FRONT_DIR, "scripts.js")


@app.post("/paciente", tags=[paciente_tag],
          responses={"200": PacienteViewSchema, "409": ErrorSchema,
                     "400": ErrorSchema})
def add_paciente(body: PacienteSchema):
    """Adiciona um novo paciente e realiza a predicao de tratamento.

    Retorna o paciente com o resultado da predicao.
    """
    dados = {
        "Age": body.age,
        "Gender": body.gender,
        "self_employed": body.self_employed,
        "family_history": body.family_history,
        "work_interfere": body.work_interfere,
        "no_employees": body.no_employees,
        "remote_work": body.remote_work,
        "tech_company": body.tech_company,
        "benefits": body.benefits,
        "care_options": body.care_options,
        "wellness_program": body.wellness_program,
        "seek_help": body.seek_help,
        "anonymity": body.anonymity,
        "leave": body.leave,
        "mental_health_consequence": body.mental_health_consequence,
        "phys_health_consequence": body.phys_health_consequence,
        "coworkers": body.coworkers,
        "supervisor": body.supervisor,
        "mental_health_interview": body.mental_health_interview,
        "phys_health_interview": body.phys_health_interview,
        "mental_vs_physical": body.mental_vs_physical,
        "obs_consequence": body.obs_consequence,
    }

    # Preprocessa e realiza a predicao
    X_input = preprocessador.preparar_form(dados)
    predicao = modelo.predict(X_input)[0]
    outcome = preprocessador.decodificar_target(predicao)

    paciente = Paciente(
        name=body.name,
        age=body.age,
        gender=body.gender,
        self_employed=body.self_employed,
        family_history=body.family_history,
        work_interfere=body.work_interfere,
        no_employees=body.no_employees,
        remote_work=body.remote_work,
        tech_company=body.tech_company,
        benefits=body.benefits,
        care_options=body.care_options,
        wellness_program=body.wellness_program,
        seek_help=body.seek_help,
        anonymity=body.anonymity,
        leave=body.leave,
        mental_health_consequence=body.mental_health_consequence,
        phys_health_consequence=body.phys_health_consequence,
        coworkers=body.coworkers,
        supervisor=body.supervisor,
        mental_health_interview=body.mental_health_interview,
        phys_health_interview=body.phys_health_interview,
        mental_vs_physical=body.mental_vs_physical,
        obs_consequence=body.obs_consequence,
        outcome=outcome,
    )
    logger.info(f"Adicionando paciente: '{paciente.name}' | predicao: {outcome}")

    try:
        session = Session()
        session.add(paciente)
        session.commit()
        logger.info("Paciente adicionado com sucesso.")
        return apresenta_paciente(paciente), 200
    except IntegrityError:
        session.rollback()
        error_msg = "Paciente com esse nome ja existe na base."
        logger.warning(f"Erro ao adicionar paciente: {error_msg}")
        return {"message": error_msg}, 409
    except Exception as e:
        session.rollback()
        error_msg = "Nao foi possivel salvar o paciente."
        logger.error(f"Erro ao adicionar paciente: {str(e)}")
        return {"message": error_msg}, 400


@app.get("/pacientes", tags=[paciente_tag],
         responses={"200": ListagemPacientesSchema, "404": ErrorSchema})
def get_pacientes():
    """Lista todos os pacientes cadastrados."""
    logger.info("Buscando todos os pacientes.")
    session = Session()
    pacientes = session.query(Paciente).all()

    if not pacientes:
        return {"pacientes": []}, 200

    logger.info(f"{len(pacientes)} pacientes encontrados.")
    return apresenta_pacientes(pacientes), 200


@app.get("/paciente", tags=[paciente_tag],
         responses={"200": PacienteViewSchema, "404": ErrorSchema})
def get_paciente(query: PacienteBuscaSchema):
    """Busca um paciente pelo nome."""
    paciente_nome = unquote(query.name)
    logger.info(f"Buscando paciente: '{paciente_nome}'")

    session = Session()
    paciente = session.query(Paciente).filter(
        Paciente.name == paciente_nome
    ).first()

    if not paciente:
        error_msg = "Paciente nao encontrado."
        logger.warning(f"Paciente '{paciente_nome}' nao encontrado.")
        return {"message": error_msg}, 404

    logger.info(f"Paciente encontrado: '{paciente.name}'")
    return apresenta_paciente(paciente), 200


@app.delete("/paciente", tags=[paciente_tag],
            responses={"200": PacienteDelSchema, "404": ErrorSchema})
def del_paciente(query: PacienteBuscaSchema):
    """Remove um paciente pelo nome."""
    paciente_nome = unquote(query.name)
    logger.info(f"Removendo paciente: '{paciente_nome}'")

    session = Session()
    count = session.query(Paciente).filter(
        Paciente.name == paciente_nome
    ).delete()
    session.commit()

    if count:
        logger.info(f"Paciente '{paciente_nome}' removido com sucesso.")
        return {"message": "Paciente removido", "name": paciente_nome}, 200

    error_msg = "Paciente nao encontrado."
    logger.warning(f"Paciente '{paciente_nome}' nao encontrado para remocao.")
    return {"message": error_msg}, 404


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)
