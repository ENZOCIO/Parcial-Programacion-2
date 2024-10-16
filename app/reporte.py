import pandas as pd
import csv

class Reporte:
    def __init__(self, tipo_reporte):
        self.tipo_reporte = tipo_reporte

    def reporte_medico_con_mas_demandas(self, hospital):
        """Devuelve el médico con más citas y la cantidad de citas."""
        conteo_citas = {}  # Cambiado a un diccionario

        for cita in hospital.citas:
            if cita.medico.id not in conteo_citas:
                conteo_citas[cita.medico.id] = {'medico': cita.medico, 'cantidad': 0}  # Usando un diccionario
            conteo_citas[cita.medico.id]['cantidad'] += 1  # Incrementa la cantidad de citas

        # Encuentra el médico con más citas
        medico_max = max(conteo_citas.values(), key=lambda x: x['cantidad'], default=(None, 0))
        return medico_max['medico'], medico_max['cantidad']  # Devuelve médico y cantidad

    def reporte_tendencias_citas(self, hospital):
        """Devuelve un reporte de tendencias de citas a lo largo del tiempo."""
        tendencias = {}

        for cita in hospital.citas:
            fecha = cita.fecha_hora.date()
            if fecha not in tendencias:
                tendencias[fecha] = 0
            tendencias[fecha] += 1  # Incrementa el conteo de citas para la fecha

        return tendencias

    def reporte_causas_cancelacion(self, hospital):
        """Genera un reporte de las causas de cancelación de citas."""
        causas = {}

        for cita in hospital.citas:
            if cita.motivo_cancelacion:  # Asegúrate de que el motivo no sea None
                if cita.motivo_cancelacion not in causas:
                    causas[cita.motivo_cancelacion] = 0
                causas[cita.motivo_cancelacion] += 1

        # Retornar el diccionario de causas
        return causas
    
    def reporte_ausentismo(self, hospital):
        """Calcula el porcentaje de ausentismo de citas."""
        total_citas = len(hospital.citas)
        citas_canceladas = sum(1 for cita in hospital.citas if cita.esta_cancelada)

        if total_citas == 0:
            print("No hay citas registradas.")
            return 0.0

        porcentaje_ausentismo = (citas_canceladas / total_citas) * 100
        return round(porcentaje_ausentismo, 2)
    
    def exportar_reportes(self, hospital):
        """Exporta los reportes a un archivo CSV."""
        with open('datos/reporteexportaciones.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            # Encabezados de los reportes
            writer.writerow(['Reporte de Ausentismo'])
            writer.writerow(['Total de Citas', 'Citas Ausentes', 'Porcentaje de Ausentismo'])

            # Exportar porcentaje de ausentismo
            total_citas = len(hospital.citas)
            citas_ausentes = sum(1 for cita in hospital.citas if not cita.asistida)
            porcentaje_ausentismo = (citas_ausentes / total_citas * 100) if total_citas > 0 else 0
            writer.writerow([total_citas, citas_ausentes, f"{porcentaje_ausentismo:.2f}%"])

            # Separador
            writer.writerow([])

            # Causas de cancelación
            writer.writerow(['Reporte de Causas de Cancelación'])
            writer.writerow(['Causa', 'Cantidad'])

            causas = self.reporte_causas_cancelacion(hospital)
            for causa, cantidad in causas.items():
                writer.writerow([causa, cantidad])

            # Separador
            writer.writerow([])

            # Tendencias
            writer.writerow(['Reporte de Tendencias de Citas'])
            writer.writerow(['Fecha', 'Cantidad'])

            tendencias = self.reporte_tendencias_citas(hospital)
            for fecha, cantidad in tendencias.items():
                writer.writerow([fecha, cantidad])

            # Separador
            writer.writerow([])

            # Médico con más citas
            writer.writerow(['Reporte del Médico con Más Citas'])
            writer.writerow(['Médico', 'Cantidad'])

            medico, cantidad = self.reporte_medico_con_mas_demandas(hospital)
            writer.writerow([medico.nombre, cantidad])

        print("Reportes exportados a datos/reporteexportaciones.csv")
