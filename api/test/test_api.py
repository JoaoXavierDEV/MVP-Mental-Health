import pytest
from app import app
from model import Session, Paciente


PACIENTE_PAYLOAD = {
    "name": "__test_paciente_api",
    "age": 30,
    "gender": "Male",
    "self_employed": "No",
    "family_history": "No",
    "work_interfere": "Sometimes",
    "no_employees": "6-25",
    "remote_work": "No",
    "tech_company": "Yes",
    "benefits": "Yes",
    "care_options": "Not sure",
    "wellness_program": "No",
    "seek_help": "Yes",
    "anonymity": "Yes",
    "leave": "Somewhat easy",
    "mental_health_consequence": "No",
    "phys_health_consequence": "No",
    "coworkers": "Some of them",
    "supervisor": "Yes",
    "mental_health_interview": "No",
    "phys_health_interview": "Maybe",
    "mental_vs_physical": "Yes",
    "obs_consequence": "No",
}


@pytest.fixture
def client():
    """Cria um cliente de teste para a aplicacao Flask."""
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


@pytest.fixture(autouse=True)
def limpar_dados_teste():
    """Remove registros de teste do banco apos cada teste."""
    yield
    session = Session()
    session.query(Paciente).filter(
        Paciente.name.like("__test_%")
    ).delete(synchronize_session=False)
    session.commit()
    session.close()


class TestPostPaciente:
    """Testes para o endpoint POST /paciente."""

    def test_cadastrar_paciente_com_sucesso(self, client):
        """Verifica se um paciente e cadastrado e a predicao e retornada."""
        resp = client.post("/paciente", json=PACIENTE_PAYLOAD)
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["name"] == PACIENTE_PAYLOAD["name"]
        assert data["age"] == PACIENTE_PAYLOAD["age"]
        assert "outcome" in data
        assert data["outcome"] in ["Yes", "No"]

    def test_cadastrar_paciente_duplicado_retorna_409(self, client):
        """Verifica se cadastrar um paciente com nome duplicado retorna 409."""
        client.post("/paciente", json=PACIENTE_PAYLOAD)
        resp = client.post("/paciente", json=PACIENTE_PAYLOAD)
        assert resp.status_code == 409
        data = resp.get_json()
        assert "message" in data


class TestGetPacientes:
    """Testes para o endpoint GET /pacientes."""

    def test_listar_pacientes_retorna_200(self, client):
        """Verifica se a listagem retorna status 200."""
        resp = client.get("/pacientes")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "pacientes" in data

    def test_listar_pacientes_contem_cadastrado(self, client):
        """Verifica se um paciente cadastrado aparece na listagem."""
        client.post("/paciente", json=PACIENTE_PAYLOAD)
        resp = client.get("/pacientes")
        assert resp.status_code == 200
        data = resp.get_json()
        nomes = [p["name"] for p in data["pacientes"]]
        assert PACIENTE_PAYLOAD["name"] in nomes


class TestGetPaciente:
    """Testes para o endpoint GET /paciente."""

    def test_buscar_paciente_existente(self, client):
        """Verifica se a busca por nome retorna o paciente correto."""
        client.post("/paciente", json=PACIENTE_PAYLOAD)
        resp = client.get(f"/paciente?name={PACIENTE_PAYLOAD['name']}")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["name"] == PACIENTE_PAYLOAD["name"]

    def test_buscar_paciente_inexistente_retorna_404(self, client):
        """Verifica se buscar um paciente inexistente retorna 404."""
        resp = client.get("/paciente?name=__test_nao_existe")
        assert resp.status_code == 404
        data = resp.get_json()
        assert "message" in data


class TestDeletePaciente:
    """Testes para o endpoint DELETE /paciente."""

    def test_remover_paciente_existente(self, client):
        """Verifica se um paciente e removido com sucesso."""
        client.post("/paciente", json=PACIENTE_PAYLOAD)
        resp = client.delete(f"/paciente?name={PACIENTE_PAYLOAD['name']}")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["name"] == PACIENTE_PAYLOAD["name"]

    def test_remover_paciente_inexistente_retorna_404(self, client):
        """Verifica se remover um paciente inexistente retorna 404."""
        resp = client.delete("/paciente?name=__test_nao_existe")
        assert resp.status_code == 404
        data = resp.get_json()
        assert "message" in data

    def test_paciente_removido_nao_aparece_na_listagem(self, client):
        """Verifica se apos a remocao o paciente nao aparece mais."""
        client.post("/paciente", json=PACIENTE_PAYLOAD)
        client.delete(f"/paciente?name={PACIENTE_PAYLOAD['name']}")
        resp = client.get(f"/paciente?name={PACIENTE_PAYLOAD['name']}")
        assert resp.status_code == 404
