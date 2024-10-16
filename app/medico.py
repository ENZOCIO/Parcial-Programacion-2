from agenda import Agenda  # Asegúrate de que esta importación sea correcta

class Medico:
    def __init__(self, id, nombre, correo, especialidad):
        self.id = id
        self.nombre = nombre
        self.correo = correo
        self.especialidad = especialidad
        self.agenda = Agenda()  # Inicializa la agenda para el médico

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'correo': self.correo,
            'especialidad': self.especialidad
        }

    @staticmethod
    def from_dict(data):
        return Medico(
            data['id'], 
            data['nombre'], 
            data['correo'], 
            data['especialidad']
        )
