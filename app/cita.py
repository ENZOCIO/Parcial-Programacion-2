from datetime import datetime

class Cita:
    def __init__(self, paciente, medico, fecha_hora):
        self.paciente = paciente
        self.medico = medico
        self.fecha_hora = fecha_hora
        self.cancelada = False
        self.motivo_cancelacion = None  # Inicializa el motivo de cancelación como None
        self.esta_cancelada = False
        self.asistida = None  # Inicializa el estado de asistencia como None

    def to_dict(self):
        return {
            'fecha_hora': self.fecha_hora.strftime("%Y-%m-%d %H:%M:%S"),
            'paciente': self.paciente.identificacion,
            'medicos': self.medico.id,
            'motivo_cancelacion': self.motivo_cancelacion  # Añade el motivo de cancelación aquí
        }

    @staticmethod
    def from_dict(data, hospital):
        paciente = hospital.buscar_paciente(data['paciente'])
        medico = hospital.buscar_medico(data['medicos'])
        fecha_hora = datetime.strptime(data['fecha_hora'], '%Y-%m-%d %H:%M:%S')
        cita = Cita(paciente, medico, fecha_hora)
        cita.motivo_cancelacion = data.get('motivo_cancelacion')  # Recupera el motivo de cancelación
        return cita

    def cancelar(self, motivo):
        """Marca la cita como cancelada y establece el motivo de cancelación."""
        self.cancelada = True
        self.motivo_cancelacion = motivo
        self.esta_cancelada = True

    def marcar_asistencia(self, asistida):
        """Marca si el paciente asistió o no a la cita."""
        self.asistida = asistida


# Función externa para registrar asistencia, debería estar en main.py o en la lógica de interacción con el sistema
def registrar_asistencia(hospital):
    identificacion = input("Ingrese la identificación del paciente: ")
    fecha_input = input("Ingrese la fecha de la cita (YYYY-MM-DD): ")

    try:
        fecha = datetime.strptime(fecha_input, "%Y-%m-%d").date()
        paciente = hospital.buscar_paciente(identificacion)
        if paciente:
            cita = next((c for c in hospital.citas if c.paciente == paciente and c.fecha_hora.date() == fecha), None)
            
            if cita:
                asistencia = input("¿El paciente asistió a la cita? (s/n): ").lower()
                if asistencia == 's':
                    cita.marcar_asistencia(True)
                    print(f"Asistencia registrada para {paciente.nombre_completo}")
                else:
                    cita.marcar_asistencia(False)
                    print(f"Ausencia registrada para {paciente.nombre_completo}")
            else:
                print("No se encontró la cita en esa fecha.")
        else:
            print("Paciente no encontrado.")
    
    except ValueError:
        print("Formato de fecha no válido.")
