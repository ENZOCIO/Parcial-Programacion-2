class Paciente:
     
    def __init__(self, identificacion, nombre_completo, celular, correo):
        self.identificacion = identificacion
        self.nombre_completo = nombre_completo
        self.celular = celular
        self.correo = correo

    def to_dict(self):
        return {
            'identificacion': self.identificacion,
            'nombre_completo': self.nombre_completo,
            'celular': self.celular,
            'correo': self.correo
        }

    @staticmethod
    def from_dict(data):
        return Paciente(
            data['identificacion'], 
            data['nombre_completo'], 
            data['celular'], 
            data['correo']
        )

    def __eq__(self, other):
        if isinstance(other, Paciente):
            return (self.identificacion == other.identificacion and
                    self.nombre_completo == other.nombre_completo and
                    self.celular == other.celular and
                    self.correo == other.correo)
        return False
