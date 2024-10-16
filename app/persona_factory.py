
from .paciente import Paciente
from .medico import Medico

class PersonaFactory:
    @staticmethod
    def crear_persona(tipo_persona, **kwargs):
        if tipo_persona == "paciente":
            return Paciente(**kwargs)
        elif tipo_persona == "medico":
            return Medico(**kwargs)
