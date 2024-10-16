# test_cita.py
import pytest
from datetime import datetime
from app.cita import Cita
from app.paciente import Paciente
from app.medico import Medico

def test_crear_cita():
    paciente = Paciente("123456", "Juan Perez", "123456789", "juan@example.com")
    medico = Medico("M001", "Dr. Smith", "smith@example.com", "Cardiología")
    fecha_hora = datetime(2024, 10, 17, 15, 30)

    cita = Cita(paciente, medico, fecha_hora)
    assert cita.paciente == paciente
    assert cita.medico == medico
    assert cita.fecha_hora == fecha_hora

def test_cancelar_cita():
    paciente = Paciente("123456", "Juan Perez", "123456789", "juan@example.com")
    medico = Medico("M001", "Dr. Smith", "smith@example.com", "Cardiología")
    fecha_hora = datetime(2024, 10, 17, 15, 30)

    cita = Cita(paciente, medico, fecha_hora)
    cita.cancelar("No puedo asistir")
    assert cita.cancelada is True
    assert cita.motivo_cancelacion == "No puedo asistir"
