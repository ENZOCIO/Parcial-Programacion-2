from app.notificacion import Notificacion

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

def test_enviar_notificacion():
    notificacion = Notificacion()

    # Probar el envío de notificaciones por WhatsApp
    resultado = notificacion.enviar_notificacion('whatsapp', 'Mensaje por WhatsApp', None)
    assert resultado == "Mensaje enviado a None: Mensaje por WhatsApp"  # Ajustar aquí

    # Probar el envío de notificaciones por correo
    resultado = notificacion.enviar_notificacion('correo', 'Mensaje por correo', 'test@example.com')
    assert resultado == "Correo enviado a test@example.com - Asunto: Notificación - Mensaje: Mensaje por correo"  # Ajustar aquí

    # Probar el envío de notificaciones por SMS
    resultado = notificacion.enviar_notificacion('llamada', 'Mensaje por llamada', '123456789')
    assert resultado == "SMS enviado a 123456789: Mensaje por llamada"  # Ajustar aquí