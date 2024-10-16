# test_medico.py
import pytest
from app.medico import Medico

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

def test_crear_medico():
    medico = Medico("M001", "Dr. Smith", "smith@example.com", "Cardiología")
    assert medico.id == "M001"
    assert medico.nombre == "Dr. Smith"
    assert medico.correo == "smith@example.com"
    assert medico.especialidad == "Cardiología"

def test_asignar_especialidad():
    medico = Medico("M001", "Dr. Smith", "smith@example.com", "Cardiología")
    medico.especialidad = "Neurología"
    assert medico.especialidad == "Neurología"
