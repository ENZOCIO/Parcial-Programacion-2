from datetime import datetime
import pytest
from app.agenda import Agenda
from app.cita import Cita  # Asegúrate de que importas la clase Cita correctamente

def test_agenda_disponibilidad():
    agenda = Agenda()
    fecha_hora = datetime(2024, 10, 17, 15, 30)

    # Verificar que inicialmente la agenda está vacía
    assert agenda.verificar_disponibilidad(fecha_hora.date(), fecha_hora.time()) is True

    # Agregar una cita y verificar disponibilidad nuevamente
    cita = Cita(paciente="Paciente 1", medico="Medico 1", fecha_hora=fecha_hora)
    agenda.agregar_cita(cita)
    
    assert agenda.verificar_disponibilidad(fecha_hora.date(), fecha_hora.time()) is False

def test_obtener_horas_disponibles():
    agenda = Agenda()
    fecha = datetime(2024, 10, 17).date()
    
    # Agregar una cita
    hora1 = datetime(2024, 10, 17, 9, 0)  # Cita a las 9:00
    cita1 = Cita(paciente="Paciente 1", medico="Medico 1", fecha_hora=hora1)
    agenda.agregar_cita(cita1)

    # Verificar que la hora1 no está disponible pero hora2 sí lo está
    horas_disponibles = agenda.obtener_horas_disponibles(fecha)

    assert hora1.time() not in horas_disponibles  # Debe estar ocupada
    assert datetime(2024, 10, 17, 10, 0).time() in horas_disponibles  # Debe estar libre
