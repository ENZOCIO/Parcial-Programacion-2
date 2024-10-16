import pytest
from app.hospital import Hospital
from app.paciente import Paciente
from app.medico import Medico

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))


def test_agregar_paciente():
    hospital = Hospital.get_instance()
    paciente = Paciente("123456", "Juan Perez", "123456789", "juan@example.com")
    hospital.agregar_paciente(paciente)
    assert len(hospital.pacientes) == 1
    assert hospital.pacientes[0] == paciente

def test_agregar_medico():
    hospital = Hospital.get_instance()
    medico = Medico("M001", "Dr. Smith", "smith@example.com", "Cardiología")
    hospital.agregar_medico(medico)
    assert len(hospital.medicos) == 1
    assert hospital.medicos[0] == medico

def test_buscar_paciente():
    hospital = Hospital.get_instance()
    paciente = Paciente("123456", "Juan Perez", "123456789", "juan@example.com")
    hospital.agregar_paciente(paciente)
    assert hospital.buscar_paciente("123456") == paciente
    assert hospital.buscar_paciente("999999") is None  # Paciente no existente
