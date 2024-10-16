import pytest
from app.persona import Persona

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))


def test_crear_persona():
    persona = Persona("123456", "Juan Perez", "555-1234", "juan@example.com")
    assert persona.nombre_completo == "Juan Perez"

def test_modificar_nombre_persona():
    persona = Persona("123456", "Juan Perez", "555-1234", "juan@example.com")
    persona.nombre_completo = "Pedro Gomez"
    assert persona.nombre_completo == "Pedro Gomez"
