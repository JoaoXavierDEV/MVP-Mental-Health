from pydantic import BaseModel
from typing import Optional, List


class PacienteSchema(BaseModel):
    """Define como um novo paciente deve ser representado ao ser inserido."""
    name: str = "Joao Silva"
    age: int = 30
    gender: str = "Male"
    self_employed: str = "No"
    family_history: str = "No"
    work_interfere: str = "Sometimes"
    no_employees: str = "6-25"
    remote_work: str = "No"
    tech_company: str = "Yes"
    benefits: str = "Yes"
    care_options: str = "Not sure"
    wellness_program: str = "No"
    seek_help: str = "Yes"
    anonymity: str = "Yes"
    leave: str = "Somewhat easy"
    mental_health_consequence: str = "No"
    phys_health_consequence: str = "No"
    coworkers: str = "Some of them"
    supervisor: str = "Yes"
    mental_health_interview: str = "No"
    phys_health_interview: str = "Maybe"
    mental_vs_physical: str = "Yes"
    obs_consequence: str = "No"


class PacienteViewSchema(BaseModel):
    """Define como um paciente sera retornado."""
    id: int = 1
    name: str = "Joao Silva"
    age: int = 30
    gender: str = "Male"
    self_employed: str = "No"
    family_history: str = "No"
    work_interfere: str = "Sometimes"
    no_employees: str = "6-25"
    remote_work: str = "No"
    tech_company: str = "Yes"
    benefits: str = "Yes"
    care_options: str = "Not sure"
    wellness_program: str = "No"
    seek_help: str = "Yes"
    anonymity: str = "Yes"
    leave: str = "Somewhat easy"
    mental_health_consequence: str = "No"
    phys_health_consequence: str = "No"
    coworkers: str = "Some of them"
    supervisor: str = "Yes"
    mental_health_interview: str = "No"
    phys_health_interview: str = "Maybe"
    mental_vs_physical: str = "Yes"
    obs_consequence: str = "No"
    outcome: str = "Yes"


class PacienteBuscaSchema(BaseModel):
    """Define a estrutura para busca de paciente por nome."""
    name: str = "Joao Silva"


class PacienteDelSchema(BaseModel):
    """Define a estrutura de retorno apos remocao."""
    message: str
    name: str


class ListagemPacientesSchema(BaseModel):
    """Define como uma lista de pacientes sera retornada."""
    pacientes: List[PacienteViewSchema]


def apresenta_paciente(paciente):
    """Retorna uma representacao do paciente seguindo o schema definido."""
    return {
        "id": paciente.id,
        "name": paciente.name,
        "age": paciente.age,
        "gender": paciente.gender,
        "self_employed": paciente.self_employed,
        "family_history": paciente.family_history,
        "work_interfere": paciente.work_interfere,
        "no_employees": paciente.no_employees,
        "remote_work": paciente.remote_work,
        "tech_company": paciente.tech_company,
        "benefits": paciente.benefits,
        "care_options": paciente.care_options,
        "wellness_program": paciente.wellness_program,
        "seek_help": paciente.seek_help,
        "anonymity": paciente.anonymity,
        "leave": paciente.leave,
        "mental_health_consequence": paciente.mental_health_consequence,
        "phys_health_consequence": paciente.phys_health_consequence,
        "coworkers": paciente.coworkers,
        "supervisor": paciente.supervisor,
        "mental_health_interview": paciente.mental_health_interview,
        "phys_health_interview": paciente.phys_health_interview,
        "mental_vs_physical": paciente.mental_vs_physical,
        "obs_consequence": paciente.obs_consequence,
        "outcome": paciente.outcome,
    }


def apresenta_pacientes(pacientes):
    """Retorna uma lista de pacientes."""
    result = []
    for p in pacientes:
        result.append(apresenta_paciente(p))
    return {"pacientes": result}
