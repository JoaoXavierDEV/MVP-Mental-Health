from sqlalchemy import Column, String, Integer, DateTime, Float
from datetime import datetime
from model.base import Base


class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column("name", String(140), unique=True)

    # Dados demograficos
    age = Column(Integer)
    gender = Column(String(20))
    self_employed = Column(String(10))

    # Historico e trabalho
    family_history = Column(String(10))
    work_interfere = Column(String(20))
    no_employees = Column(String(20))
    remote_work = Column(String(10))
    tech_company = Column(String(10))

    # Beneficios do empregador
    benefits = Column(String(20))
    care_options = Column(String(20))
    wellness_program = Column(String(20))
    seek_help = Column(String(20))
    anonymity = Column(String(20))
    leave = Column(String(30))

    # Consequencias percebidas
    mental_health_consequence = Column(String(10))
    phys_health_consequence = Column(String(10))

    # Abertura para discussao
    coworkers = Column(String(20))
    supervisor = Column(String(20))
    mental_health_interview = Column(String(10))
    phys_health_interview = Column(String(10))
    mental_vs_physical = Column(String(20))
    obs_consequence = Column(String(10))

    # Resultado da predicao
    outcome = Column(String(50))
    data_insercao = Column(DateTime, default=datetime.now)

    def __init__(self, name, age, gender, self_employed, family_history,
                 work_interfere, no_employees, remote_work, tech_company,
                 benefits, care_options, wellness_program, seek_help,
                 anonymity, leave, mental_health_consequence,
                 phys_health_consequence, coworkers, supervisor,
                 mental_health_interview, phys_health_interview,
                 mental_vs_physical, obs_consequence, outcome):
        self.name = name
        self.age = age
        self.gender = gender
        self.self_employed = self_employed
        self.family_history = family_history
        self.work_interfere = work_interfere
        self.no_employees = no_employees
        self.remote_work = remote_work
        self.tech_company = tech_company
        self.benefits = benefits
        self.care_options = care_options
        self.wellness_program = wellness_program
        self.seek_help = seek_help
        self.anonymity = anonymity
        self.leave = leave
        self.mental_health_consequence = mental_health_consequence
        self.phys_health_consequence = phys_health_consequence
        self.coworkers = coworkers
        self.supervisor = supervisor
        self.mental_health_interview = mental_health_interview
        self.phys_health_interview = phys_health_interview
        self.mental_vs_physical = mental_vs_physical
        self.obs_consequence = obs_consequence
        self.outcome = outcome
