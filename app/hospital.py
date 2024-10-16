from datetime import datetime, timedelta
import csv
import json
from paciente import Paciente
from medico import Medico
from cita import Cita
from agenda import Agenda
from whatssap import enviar_whatsapp
from correo import enviar_correo
from celular import enviar_sms


class Hospital:
    _instance = None

    def __init__(self):
        self.pacientes = []  # Lista para almacenar pacientes
        self.medicos = []    # Lista para almacenar médicos
        self.citas = []      # Lista para almacenar citas

    @staticmethod
    def get_instance():
        """Método para obtener la instancia única del hospital."""
        if Hospital._instance is None:
            Hospital._instance = Hospital()
        return Hospital._instance

    # ==========================
    # Métodos para agregar datos
    # ==========================

    def agregar_paciente(self, paciente):
        """Agrega un paciente a la lista de pacientes."""
        self.pacientes.append(paciente)

    def agregar_medico(self, medico):
        """Agrega un médico a la lista de médicos."""
        self.medicos.append(medico)

    def agregar_cita(self, cita):
        """Agrega una cita a la lista de citas."""
        self.citas.append(cita)

    # ==========================
    # Métodos de búsqueda
    # ==========================

    def buscar_paciente(self, identificacion):
        """Busca un paciente por su identificación."""
        for paciente in self.pacientes:
            if paciente.identificacion == identificacion:
                print(f"Paciente encontrado: {paciente.nombre_completo}")
                return paciente
        print(f"Paciente no encontrado: {identificacion}")
        return None  # Retorna None si no se encuentra el paciente

    def buscar_medico(self, identificacion):
        """Busca un médico por su identificación."""
        for medico in self.medicos:
            if medico.id == identificacion:
                return medico
        return None  # Retorna None si no se encuentra el médico

    # ==========================
    # Métodos de disponibilidad
    # ==========================

    def verificar_disponibilidad(self, especialidad, fecha, hora):
        """Verifica la disponibilidad de médicos según la especialidad y la fecha/hora solicitadas."""
        medicos_disponibles = []
        for medico in self.medicos:
            if medico.especialidad == especialidad:
                if medico.agenda.verificar_disponibilidad(fecha, hora):
                    medicos_disponibles.append(medico)
        return medicos_disponibles

    def obtener_medicos_por_especialidad(self, especialidad):
        """Obtiene una lista de médicos que pertenecen a una especialidad específica."""
        return [medico for medico in self.medicos if medico.especialidad == especialidad]

    def mostrar_cupos_disponibles(self, especialidad, fecha):
        """Muestra los cupos disponibles para médicos de una especialidad en una fecha dada."""
        for medico in self.medicos:
            if medico.especialidad == especialidad:
                horas_disponibles = medico.agenda.obtener_horas_disponibles(fecha)
                if horas_disponibles:
                    print(f"\nMédico: Dr. {medico.nombre} (Especialidad: {especialidad})")
                    print("Cupos disponibles:")
                    for hora in horas_disponibles:
                        print(f"- {hora.strftime('%H:%M')}")
                else:
                    print(f"\nMédico: Dr. {medico.nombre} (Especialidad: {especialidad})")
                    print("No hay cupos disponibles.")

    # ==========================
    # Método de cancelación
    # ==========================

    def cancelar_cita(self, identificacion_paciente, fecha):
        """Cancela citas de un paciente en la fecha especificada y mueve las citas próximas."""
        paciente = self.buscar_paciente(identificacion_paciente)
        if not paciente:
            print("Paciente no encontrado.")
            return

        print(f"Buscando citas para el paciente {paciente.nombre_completo} en la fecha {fecha}.")
        citas_a_cancelar = [cita for cita in self.citas if cita.paciente == paciente and cita.fecha_hora.date() == fecha]

        if not citas_a_cancelar:
            print("No se encontraron citas para cancelar en esa fecha.")
            return

        motivo_cancelacion = input("Ingrese el motivo de la cancelación: ")

        for cita in citas_a_cancelar:
            cita.cancelar(motivo_cancelacion)  # Marca la cita como cancelada
            cita.esta_cancelada = True  # Asegúrate de marcar la cita como cancelada
            print(f"Cita cancelada para el paciente {cita.paciente.nombre_completo} a las {cita.fecha_hora.time()}.")

            self.solicitar_feedback(cita)

        # Mover citas próximas
        self.mover_citas_proximas(paciente, fecha)

    def solicitar_feedback(self, cita):
        """Solicita feedback al paciente después de su cita."""
        mensaje = f"¿Cómo fue su experiencia en la cita con el Dr. {cita.medico.nombre} el {cita.fecha_hora.date()}? Responda con su evaluación (1-5) y cualquier comentario."
        # Aquí podrías enviar un mensaje al paciente por WhatsApp o correo
        enviar_whatsapp(cita.paciente.celular, mensaje)

    def guardar_feedback(self, paciente_id, evaluacion, comentario):
        """Guarda el feedback del paciente en un archivo."""
        with open('datos/feedback.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([paciente_id, evaluacion, comentario])  # Guarda el ID del paciente, evaluación y comentario

    def mover_citas_proximas(self, paciente, fecha_cancelada):
        """Mueve las citas que están próximas a la cita cancelada."""
        fecha_limite = fecha_cancelada + timedelta(days=2)  # Puedes ajustar el rango de días
        citas_proximas = [cita for cita in self.citas if cita.paciente == paciente and fecha_cancelada < cita.fecha_hora.date() <= fecha_limite]

        for cita in citas_proximas:
            nueva_fecha = fecha_cancelada + timedelta(days=1)  # Por ejemplo, mover la cita un día después
            cita.fecha_hora = cita.fecha_hora.replace(year=nueva_fecha.year, month=nueva_fecha.month, day=nueva_fecha.day)
            print(f"Cita movida para el paciente {cita.paciente.nombre_completo} a la nueva fecha {cita.fecha_hora}.")

    # ==========================
    # Métodos de notificación
    # ==========================

    def notificar_citas(self):
        """Notifica a los pacientes sobre sus citas programadas dentro de dos días."""
        hoy = datetime.now().date()
        for cita in self.citas:
            if cita.fecha_hora.date() == hoy + timedelta(days=2):
                print(f"Notificando al paciente {cita.paciente.nombre_completo}:")
                print(f"Tienes una cita programada con el Dr. {cita.medico.nombre} el {cita.fecha_hora.date()} a las {cita.fecha_hora.time()}.")

    # ==========================
    # Métodos de carga de datos
    # ==========================

    def cargar_pacientes(self, ruta_archivo):
        """Carga pacientes desde un archivo CSV."""
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    paciente = Paciente(
                        row['identificacion'],
                        row['nombre_completo'],
                        row['celular'],
                        row['correo']
                    )
                    self.agregar_paciente(paciente)
        except FileNotFoundError:
            print("El archivo de pacientes no se encontró.")
        except KeyError as e:
            print(f"Error: Falta la clave {e} en el archivo de pacientes.")
        except Exception as e:
            print(f"Error al cargar pacientes: {e}")

        print("Pacientes cargados:", [p.nombre_completo for p in self.pacientes])

    def cargar_medicos(self, ruta_archivo):
        """Carga médicos desde un archivo JSON."""
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as file:
                medicos_data = json.load(file)
                for medico_data in medicos_data:
                    medico = Medico(
                        medico_data['id'],
                        medico_data['nombre'],
                        medico_data['correo'],
                        medico_data['especialidad']
                    )
                    self.agregar_medico(medico)
        except FileNotFoundError:
            print("El archivo de médicos no se encontró.")
        except json.JSONDecodeError:
            print("Error al decodificar el archivo JSON de médicos.")
        except Exception as e:
            print(f"Error al cargar médicos: {e}")

        print("Médicos cargados:", [m.nombre for m in self.medicos])

    def cargar_citas(self, ruta_archivo):
        """Carga citas desde un archivo CSV."""
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    paciente = self.buscar_paciente(row['paciente'])
                    medico = self.buscar_medico(row['medicos'])
                    print(f"Buscando paciente: {row['paciente']} y médico: {row['medicos']}.")  # Diagnóstico
                    if paciente and medico:
                        # Convertir la cadena de fecha y hora a un objeto datetime
                        fecha_hora = datetime.strptime(row['fecha_hora'], '%Y-%m-%d %H:%M:%S')
                        cita = Cita(paciente, medico, fecha_hora)
                        self.agregar_cita(cita)
                    else:
                        print(f"Cita no se pudo agendar para el paciente {row['paciente']} o médico {row['medicos']}.")
        except FileNotFoundError:
            print("El archivo de citas no se encontró.")
        except Exception as e:
            print(f"Error al cargar citas: {e}")

    # ==========================
    # Métodos de guardado de datos
    # ==========================

    def guardar_pacientes(self, ruta_archivo):
        """Guarda la lista de pacientes en un archivo CSV."""
        with open(ruta_archivo, 'w', newline='', encoding='utf-8') as file:
            fieldnames = ['identificacion', 'nombre_completo', 'celular', 'correo']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()
            for paciente in self.pacientes:
                writer.writerow({
                    'identificacion': paciente.identificacion,
                    'nombre_completo': paciente.nombre_completo,
                    'celular': paciente.celular,
                    'correo': paciente.correo
                })

    def guardar_medicos(self, ruta_archivo):
        """Guarda la lista de médicos en un archivo JSON."""
        with open(ruta_archivo, 'w', encoding='utf-8') as file:
            json.dump([medico.__dict__ for medico in self.medicos], file, ensure_ascii=False, indent=4)

    def guardar_citas(self, ruta_archivo):
        """Guarda la lista de citas en un archivo CSV."""
        with open(ruta_archivo, 'w', newline='', encoding='utf-8') as file:
            fieldnames = ['fecha_hora', 'paciente', 'medicos']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()
            for cita in self.citas:
                writer.writerow({
                    'fecha_hora': cita.fecha_hora.strftime('%Y-%m-%d %H:%M:%S'),
                    'paciente': cita.paciente.identificacion,
                    'medicos': cita.medico.id
                })

    # ==========================
    # Nuevas funcionalidades
    # ==========================

    def enviar_recordatorios(self):
        """Envía recordatorios a los pacientes sobre sus citas programadas."""
        hoy = datetime.now().date()
        for cita in self.citas:
            # Verificar si el recordatorio debe ser enviado
            if cita.fecha_hora.date() == hoy + timedelta(days=1):  # 1 día antes
                mensaje = f"Recordatorio: Tienes una cita programada con el Dr. {cita.medico.nombre} el {cita.fecha_hora.date()} a las {cita.fecha_hora.time()}."
                # Llama a la función de notificación (WhatsApp, correo, SMS)
                enviar_whatsapp(cita.paciente.celular, mensaje)
                enviar_correo(cita.paciente.correo, "Recordatorio de cita", mensaje)
                enviar_sms(cita.paciente.celular, mensaje)


# Ejemplo de uso
if __name__ == "__main__":
    hospital = Hospital.get_instance()
    hospital.cargar_pacientes('datos/pacientes.csv')
    hospital.cargar_medicos('datos/medicos.json')
    hospital.cargar_citas('datos/citas.csv')

    hospital.enviar_recordatorios()

    # Mostrar los médicos de una especialidad
    especialidad_a_buscar = 'Cardiología'  # Cambiar según se necesite
    medicos_en_especialidad = hospital.obtener_medicos_por_especialidad(especialidad_a_buscar)
    print(f"Médicos en la especialidad {especialidad_a_buscar}: {[medico.nombre for medico in medicos_en_especialidad]}")
