import pytest
from app.whatssap import enviar_whatsapp
from app.celular import enviar_sms
from app.correo import enviar_correo

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))
def test_enviar_notificacion():
    
# Prueba unificada para las notificaciones
def test_enviar_notificaciones():
    # Probar el envío de notificaciones por WhatsApp
    numero_whatsapp = '123456789'
    mensaje_whatsapp = 'Este es un mensaje de prueba'
    resultado_whatsapp = enviar_whatsapp(numero_whatsapp, mensaje_whatsapp)
    assert resultado_whatsapp == f'Mensaje enviado a {numero_whatsapp}: {mensaje_whatsapp}'

    # Probar el envío de notificaciones por SMS
    numero_sms = '987654321'
    mensaje_sms = 'Este es un mensaje SMS'
    resultado_sms = enviar_sms(numero_sms, mensaje_sms)
    assert resultado_sms == f'SMS enviado a {numero_sms}: {mensaje_sms}'

    # Probar el envío de notificaciones por correo
    direccion_correo = 'test@example.com'
    asunto = 'Asunto'
    mensaje_correo = 'Mensaje de prueba'
    resultado_correo = enviar_correo(direccion_correo, asunto, mensaje_correo)
    assert resultado_correo == f'Correo enviado a {direccion_correo} - Asunto: {asunto} - Mensaje: {mensaje_correo}'