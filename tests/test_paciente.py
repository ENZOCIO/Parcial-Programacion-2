import pytest
from app.paciente import Paciente

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))


def test_crear_paciente():
    paciente = Paciente("123456", "Juan Perez", "123456789", "juan@example.com")
    assert paciente.identificacion == "123456"
    assert paciente.nombre_completo == "Juan Perez"
    assert paciente.celular == "123456789"
    assert paciente.correo == "juan@example.com"

def test_modificar_paciente():
    paciente = Paciente("123456", "Juan Perez", "123456789", "juan@example.com")
    paciente.nombre_completo = "Juan Carlos Perez"
    assert paciente.nombre_completo == "Juan Carlos Perez"
