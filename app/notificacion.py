# notificacion.py
from .whatssap import enviar_whatsapp
from .celular import enviar_sms
from .correo import enviar_correo

class Notificacion:
    def enviar_notificacion(self, metodo, mensaje, numero_o_correo):
        """Envía notificación usando el método especificado (whatsapp, correo, llamada/SMS)."""
        if metodo == "correo":
            return enviar_correo(numero_o_correo, "Asunto: Notificación", mensaje)
        elif metodo == "whatsapp":
            return enviar_whatsapp(numero_o_correo, mensaje)  # Cambiar a usar numero_o_correo
        elif metodo == "llamada":
            return enviar_sms(numero_o_correo, mensaje)
        else:
            print(f"Método {metodo} no soportado.")
