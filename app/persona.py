class Persona:
    def __init__(self, identificacion, nombre_completo, celular, correo):
        self.identificacion = identificacion  # INT
        self.nombre_completo = nombre_completo  # STR
        self.celular = celular  # INT
        self.correo = correo  # STR (opcional, puede ser None)

    def __str__(self):
        return f"Persona(ID: {self.identificacion}, Nombre Completo: {self.nombre_completo}, Celular: {self.celular}, Correo: {self.correo})"
