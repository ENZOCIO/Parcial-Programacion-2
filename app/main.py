from datetime import datetime
import csv
import json
from hospital import Hospital
from paciente import Paciente
from medico import Medico
from cita import Cita
from whatssap import enviar_whatsapp
from correo import enviar_correo
from celular import enviar_sms
from reporte import Reporte
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel
from rich import box

# Crear una instancia de Console de Rich
console = Console()

def cargar_datos_iniciales(hospital):
    console.print(Panel("[bold cyan]Cargando datos iniciales...[/bold cyan]"))
    
    # Cargar pacientes desde CSV
    try:
        with open('datos/pacientes.csv', 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                paciente = Paciente(
                    row['identificacion'], 
                    row['nombre_completo'],
                    row['celular'],
                    row['correo']
                )
                hospital.agregar_paciente(paciente)
        console.print("[green]Pacientes cargados correctamente.[/green]")
    except FileNotFoundError:
        console.print("[bold red]El archivo de pacientes no se encontró.[/bold red]")
    except KeyError as e:
        console.print(f"[bold red]Error: Falta la clave {e} en el archivo de pacientes.[/bold red]")
    except Exception as e:
        console.print(f"[bold red]Error al cargar pacientes: {e}[/bold red]")

    # Cargar médicos desde JSON
    try:
        with open('datos/medicos.json', 'r', encoding='utf-8') as file:
            medicos_data = json.load(file)
            for medico_data in medicos_data:
                medico = Medico(
                    medico_data['id'], 
                    medico_data['nombre'], 
                    medico_data['correo'], 
                    medico_data['especialidad']
                )
                hospital.agregar_medico(medico)
        console.print("[green]Médicos cargados correctamente.[/green]")
    except FileNotFoundError:
        console.print("[bold red]El archivo de médicos no se encontró.[/bold red]")
    except json.JSONDecodeError:
        console.print("[bold red]Error al decodificar el archivo JSON de médicos.[/bold red]")
    except Exception as e:
        console.print(f"[bold red]Error al cargar médicos: {e}[/bold red]")

    # Cargar citas desde CSV
    try:
        with open('datos/citas.csv', 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                paciente = hospital.buscar_paciente(row['paciente'])
                medico = hospital.buscar_medico(row['medicos'])
                if paciente and medico:
                    fecha_hora = datetime.strptime(row['fecha_hora'], '%Y-%m-%d %H:%M:%S')
                    cita = Cita(paciente, medico, fecha_hora)
                    hospital.agregar_cita(cita)
                else:
                    console.print(f"[yellow]Cita no se pudo agendar para el paciente {row['paciente']} o médico {row['medicos']}.[/yellow]")
        console.print("[green]Citas cargadas correctamente.[/green]")
    except FileNotFoundError:
        console.print("[bold red]El archivo de citas no se encontró.[/bold red]")
    except Exception as e:
        console.print(f"[bold red]Error al cargar citas: {e}[/bold red]")

# Menú principal
def menu_principal():
    table = Table(title="Sistema de Gestión de Citas Médicas", box=box.SQUARE)
    table.add_column("Opción", justify="center")
    table.add_column("Descripción", justify="center")
    
    table.add_row("1", "Registrar Paciente")
    table.add_row("2", "Registrar Médico")
    table.add_row("3", "Solicitar Cita")
    table.add_row("4", "Cancelar Cita")
    table.add_row("5", "Consultar Especialidades")
    table.add_row("6", "Consultar Disponibilidad de Médicos")
    table.add_row("7", "Ver Reportes")
    table.add_row("8", "Registrar Asistencia de Citas")
    table.add_row("9", "Salir")
    
    console.print(table)

# Función para registrar asistencia
def registrar_asistencia(hospital):
    identificacion = Prompt.ask("Ingrese la identificación del paciente")
    fecha_input = Prompt.ask("Ingrese la fecha de la cita (YYYY-MM-DD)")

    try:
        fecha = datetime.strptime(fecha_input, "%Y-%m-%d").date()
        paciente = hospital.buscar_paciente(identificacion)
        if paciente:
            cita = next((c for c in hospital.citas if c.paciente == paciente and c.fecha_hora.date() == fecha), None)
            
            if cita:
                asistencia = Prompt.ask("¿El paciente asistió a la cita? (s/n)").lower()
                if asistencia == 's':
                    cita.marcar_asistencia(True)
                    console.print(f"[green]Asistencia registrada para {paciente.nombre_completo}[/green]")
                else:
                    cita.marcar_asistencia(False)
                    console.print(f"[yellow]Ausencia registrada para {paciente.nombre_completo}[/yellow]")
            else:
                console.print("[bold red]No se encontró la cita en esa fecha.[/bold red]")
        else:
            console.print("[bold red]Paciente no encontrado.[/bold red]")
    
    except ValueError:
        console.print("[bold red]Formato de fecha no válido.[/bold red]")

# Función para consultar especialidades
def consultar_especialidades(hospital):
    especialidades = {medico.especialidad for medico in hospital.medicos}
    table = Table(title="Especialidades disponibles", box=box.SIMPLE)
    table.add_column("Especialidades", justify="center", style="cyan")
    
    for especialidad in especialidades:
        table.add_row(especialidad)
        
    console.print(table)

# Función para verificar disponibilidad
def verificar_disponibilidad(hospital):
    especialidad = Prompt.ask("Ingrese la especialidad a consultar")
    fecha_input = Prompt.ask("Ingrese la fecha (YYYY-MM-DD)")
    hora_input = Prompt.ask("Ingrese la hora (HH:MM)")

    try:
        fecha = datetime.strptime(fecha_input, '%Y-%m-%d').date()
        hora = datetime.strptime(hora_input, '%H:%M').time()
        disponibles = hospital.verificar_disponibilidad(especialidad, fecha, hora)

        if disponibles:
            console.print(f"[green]Médicos disponibles para {especialidad} el {fecha} a las {hora}:[/green]")
            for medico in disponibles:
                console.print(f"- Dr. {medico.nombre}")
        else:
            console.print(f"[bold red]No hay médicos disponibles para {especialidad} el {fecha} a las {hora}.[/bold red]")
    except ValueError:
        console.print("[bold red]Formato de fecha u hora no válido.[/bold red]")

# Función para registrar paciente
def registrar_paciente(hospital):
    identificacion = Prompt.ask("Ingrese la identificación del paciente")
    nombre_completo = Prompt.ask("Ingrese el nombre completo del paciente")
    celular = Prompt.ask("Ingrese el número de celular")
    correo = Prompt.ask("Ingrese el correo electrónico")
    
    paciente = Paciente(identificacion, nombre_completo, celular, correo)
    hospital.agregar_paciente(paciente)
    console.print(f"[green]Paciente {nombre_completo} registrado con éxito.[/green]")

# Función para registrar médico
def registrar_medico(hospital):
    identificacion = Prompt.ask("Ingrese la identificación del médico")
    nombre = Prompt.ask("Ingrese el nombre del médico")
    celular = Prompt.ask("Ingrese el número de celular")
    especialidad = Prompt.ask("Ingrese la especialidad del médico")
    
    medico = Medico(identificacion, nombre, celular, especialidad)
    hospital.agregar_medico(medico)
    console.print(f"[green]Médico {nombre} registrado con éxito.[/green]")

# Función para solicitar cita
def solicitar_cita(hospital):
    identificacion = input("Ingrese la identificación del paciente: ")
    paciente = hospital.buscar_paciente(identificacion)

    if paciente:
        especialidad = input("Ingrese la especialidad del médico: ")
        fecha = input("Ingrese la fecha de la cita (YYYY-MM-DD): ")

        # Mostrar los cupos disponibles
        fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
        hospital.mostrar_cupos_disponibles(especialidad, fecha_obj)

        # Preguntar si desea un médico de preferencia
        preferencia = input("¿Desea un médico de preferencia? (s/n): ").strip().lower()
        medico_seleccionado = None

        if preferencia == 's':
            medico_id = input("Ingrese la identificación del médico de preferencia: ")
            medico_seleccionado = hospital.buscar_medico(medico_id)
            if not medico_seleccionado:
                print("Médico no encontrado. Procediendo a buscar médicos disponibles.")
        
        # Si no se especifica médico de preferencia, continuar con la solicitud
        if not medico_seleccionado:
            hora = input("Ingrese la hora de la cita (HH:MM): ")
            fecha_hora = datetime.combine(fecha_obj, datetime.strptime(hora, '%H:%M').time())

            # Verificar disponibilidad de médicos
            medicos_disponibles = hospital.verificar_disponibilidad(especialidad, fecha_hora.date(), fecha_hora.time())

            if medicos_disponibles:
                # Mostrar los médicos disponibles
                for idx, medico in enumerate(medicos_disponibles):
                    print(f"{idx + 1}. Dr. {medico.nombre} ({medico.especialidad})")

                seleccion = int(input("Seleccione el médico (número): ")) - 1
                medico_seleccionado = medicos_disponibles[seleccion]

        if medico_seleccionado:
            # Mueve la entrada de hora aquí
            hora = input("Ingrese la hora de la cita (HH:MM): ")
            fecha_hora = datetime.combine(fecha_obj, datetime.strptime(hora, '%H:%M').time())

            if medico_seleccionado.agenda.verificar_disponibilidad(fecha_hora.date(), fecha_hora.time()):
                cita = Cita(paciente, medico_seleccionado, fecha_hora)
                hospital.agregar_cita(cita)
                medico_seleccionado.agenda.agregar_cita(cita)
                print(f"Cita agendada para el paciente {paciente.nombre_completo} con el Dr. {medico_seleccionado.nombre} a las {fecha_hora}.")
                notificar_cita(cita)
            else:
                print(f"El médico {medico_seleccionado.nombre} no está disponible a esa hora.")
        else:
            print("No hay médicos disponibles para la especialidad y hora solicitadas.")
    else:
        print("Paciente no encontrado.")

# Función para cancelar cita
def cancelar_cita(hospital):
    identificacion = Prompt.ask("Ingrese la identificación del paciente")
    fecha_input = Prompt.ask("Ingrese la fecha de la cita a cancelar (YYYY-MM-DD)")

    try:
        fecha = datetime.strptime(fecha_input, "%Y-%m-%d").date()
        hospital.cancelar_cita(identificacion, fecha)
        console.print("[green]Cita cancelada con éxito.[/green]")
    except ValueError:
        console.print("[bold red]Formato de fecha no válido. Asegúrese de usar el formato YYYY-MM-DD.[/bold red]")

# Función para mostrar reportes
def mostrar_reportes(hospital):
    reporte = Reporte("ausentismo")
    console.print(Panel("[bold cyan]Selecciona el tipo de reporte que deseas ver:[/bold cyan]"))
    print("\n1. Reporte de demanda de médicos")
    print("2. Reporte de tendencias de citas")
    print("3. Reporte de causas de cancelación")
    print("4. Reporte de ausentismo")
    print("5. Volver al menú principal")

    opcion = input("Seleccione una opción: ")
    if opcion == "1":
        medico, cantidad = reporte.reporte_medico_con_mas_demandas(hospital)
        console.print(f"[green]El médico con más demanda es {medico.nombre} con {cantidad} citas.[/green]")
    elif opcion == "2":
        tendencias = reporte.reporte_tendencias_citas(hospital)
        table = Table(title="Tendencias de Citas", box=box.SIMPLE)
        table.add_column("Fecha", justify="center")
        table.add_column("Cantidad de Citas", justify="center")

        for fecha, cantidad in tendencias.items():
            # Convierte la fecha a string para evitar errores de renderizado
            fecha_str = fecha.strftime("%Y-%m-%d")
            table.add_row(fecha_str, str(cantidad))
        console.print(table)
    elif opcion == "3":
        causas = reporte.reporte_causas_cancelacion(hospital)
        table = Table(title="Causas de Cancelación", box=box.SIMPLE)
        table.add_column("Causa", justify="left")
        table.add_column("Cantidad", justify="center")

        for causa, cantidad in causas.items():
            table.add_row(causa, str(cantidad))
        console.print(table)
    elif opcion == "4":
        ausentismo = reporte.reporte_ausentismo(hospital)
        console.print(f"[green]Porcentaje de ausentismo: {ausentismo}[/green]")
    elif opcion == "5":
        return

    reporte.exportar_reportes(hospital)
    console.print("[green]Los reportes han sido exportados a 'datos/reporteexportaciones.csv'.[/green]")

    reporte.exportar_reportes(hospital)
    console.print("[green]Los reportes han sido exportados a 'datos/reporteexportaciones.csv'.[/green]")

def notificar_cita(cita):
    mensaje = f"Tienes una cita programada con el Dr. {cita.medico.nombre} el {cita.fecha_hora.date()} a las {cita.fecha_hora.time()}."
    
    # Enviar por WhatsApp
    enviar_whatsapp(cita.paciente.celular, mensaje)
    
    # Enviar por correo electrónico
    enviar_correo(cita.paciente.correo, "Confirmación de cita", mensaje)
    
    # Enviar por SMS
    enviar_sms(cita.paciente.celular, mensaje)

# Función principal
def main():
    hospital = Hospital.get_instance()
    
    # Rutas de los archivos
    ruta_pacientes_csv = 'datos/pacientes.csv'
    ruta_medicos_json = 'datos/medicos.json'
    ruta_citas_csv = 'datos/citas.csv'
    
    # Cargar datos iniciales
    cargar_datos_iniciales(hospital)
    
    # Llamar a la función de notificación
    hospital.notificar_citas()
    
    while True:
        menu_principal()
        opcion = input("Seleccione una opción: ")

        # Opciones del menú
        if opcion == "1":
            registrar_paciente(hospital)
        elif opcion == "2":
            registrar_medico(hospital)
        elif opcion == "3":
            solicitar_cita(hospital)
        elif opcion == "4":
            cancelar_cita(hospital)
        elif opcion == "5":
            consultar_especialidades(hospital)
        elif opcion == "6":
            verificar_disponibilidad(hospital)
        elif opcion == "7":
            mostrar_reportes(hospital)
        elif opcion == "8":
            registrar_asistencia(hospital)
        elif opcion == "9":
            console.print("[bold cyan]Saliendo del sistema...[/bold cyan]")
            hospital.guardar_pacientes(ruta_pacientes_csv)
            hospital.guardar_medicos(ruta_medicos_json)
            hospital.guardar_citas(ruta_citas_csv)
            break
        else:
            console.print("[bold red]Opción no válida. Intente nuevamente.[/bold red]")

# Llamar a la función main
if __name__ == "__main__":
    main()
