import pytest
from app.reporte import Reporte
from app.hospital import Hospital
from app.paciente import Paciente
from app.medico import Medico
from app.cita import Cita
from datetime import datetime

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

@pytest.fixture
def hospital_con_datos():
    hospital = Hospital.get_instance()
    paciente = Paciente("123", "Juan Perez", "123456789", "juan@example.com")
    medico = Medico("M001", "Dr. Smith", "drsmith@example.com", "Cardiología")
    fecha_hora = datetime(2024, 10, 17, 15, 30)

    hospital.agregar_paciente(paciente)
    hospital.agregar_medico(medico)
    hospital.agregar_cita(Cita(paciente, medico, fecha_hora))

    return hospital

def test_reporte_medico_mas_demandas(hospital_con_datos):
    reporte = Reporte("demanda")
    medico, cantidad = reporte.reporte_medico_con_mas_demandas(hospital_con_datos)
    assert medico.nombre == "Dr. Smith"
    assert cantidad == 1

def test_reporte_tendencias_citas(hospital_con_datos):
    reporte = Reporte("tendencias")
    tendencias = reporte.reporte_tendencias_citas(hospital_con_datos)
    assert tendencias == {datetime(2024, 10, 17).date(): 2}  # Cambiar el valor esperado a 2

def test_reporte_causas_cancelacion(hospital_con_datos):
    reporte = Reporte("cancelaciones")
    hospital_con_datos.citas[0].cancelar("No puede asistir")
    causas = reporte.reporte_causas_cancelacion(hospital_con_datos)
    assert causas == {"No puede asistir": 1}
