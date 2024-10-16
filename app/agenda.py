from datetime import datetime

class Agenda:
    def __init__(self):
        self.citas_pendientes = []  # Lista para almacenar las citas

    def agregar_cita(self, cita):
        """Agrega una cita a la agenda."""
        self.citas_pendientes.append(cita)

    def verificar_disponibilidad(self, fecha, hora):
        """Verifica si hay disponibilidad en la agenda."""
        for cita in self.citas_pendientes:
            # Acceder al atributo fecha_hora del objeto Cita
            if cita.fecha_hora.date() == fecha and cita.fecha_hora.time() == hora:
                return False  # No hay disponibilidad
        return True  # Hay disponibilidad

    def obtener_horas_disponibles(self, fecha):
        """Devuelve las horas disponibles para una fecha específica."""
        horas_disponibles = []
        for hour in range(8, 18):  # Horario de 8:00 a 17:00
            for minute in [0, 20, 40]:  # Intervalos de 20 minutos
                hora = datetime.strptime(f"{hour}:{minute:02d}", "%H:%M").time()
                if self.verificar_disponibilidad(fecha, hora):
                    horas_disponibles.append(hora)
        return horas_disponibles
