## Arquitectura del Sistema

El sistema está diseñado con un enfoque modular, dividiendo la funcionalidad en varias clases y métodos. A continuación, se describe la estructura general:

### Clases Principales

1. **Paciente**: Representa la información del paciente, incluyendo métodos para gestionar citas.
2. **Medico**: Contiene información sobre los médicos y su especialidad, además de su agenda.
3. **Cita**: Maneja los detalles de una cita médica, incluyendo la fecha, hora y estado de asistencia.
4. **Agenda**: Gestiona las citas de cada médico, permitiendo agregar citas y verificar disponibilidad.
5. **Hospital**: Encapsula la lógica del sistema, incluyendo la gestión de pacientes y médicos, así como la programación de citas.
6. **Notificacion**: Maneja el envío de notificaciones a los pacientes.

### Flujo de Trabajo

1. **Solicitud de Cita**:
   - El paciente elige la especialidad y el sistema muestra los médicos disponibles.
   - Se selecciona un médico y se elige la fecha y hora de la cita.

2. **Confirmación de Cita**:
   - Se envían notificaciones de confirmación al paciente a través de correo o mensaje de texto.

3. **Gestión de Citas**:
   - Los pacientes pueden cancelar o reprogramar citas según sea necesario.
   - Las citas se agregan a la agenda del médico correspondiente.

4. **Reportes**:
   - Se generan reportes para evaluar la eficiencia del sistema, incluyendo datos de ausentismo y tendencias de citas.

## Uso de la Interfaz

Al ejecutar el sistema, se presentará un menú en la consola donde los usuarios pueden seleccionar diversas opciones, tales como:

- Solicitar una cita.
- Cancelar o reprogramar una cita.
- Ver reportes sobre médicos y citas.
- Consultar la disponibilidad de médicos.

### Ejemplo de Uso

Para solicitar una cita, sigue estos pasos:

1. Selecciona la opción "Solicitar Cita".
2. Elige una especialidad.
3. Selecciona un médico de la lista proporcionada.
4. Escoge la fecha y hora disponible.
5. Confirma tu cita y recibe la notificación correspondiente.

## Gestión de Datos

### Carga Inicial

Los datos de pacientes, médicos y citas pueden ser cargados desde archivos CSV o JSON al iniciar el sistema. Asegúrate de que los archivos sigan la estructura correcta:

- **pacientes.json**: Debe contener campos como `identificacion`, `nombre_completo`, `celular`, `correo`.
- **medicos.json**: Debe incluir `id`, `nombre`, `correo`, `especialidad`.
- **citas.csv**: Debe tener columnas para `fecha_hora`, `paciente`, `medicos`.

### Exportación de Reportes

Los reportes generados pueden ser exportados a un archivo Excel para facilitar su análisis. Se recomienda revisar los datos generados periódicamente para asegurar un servicio eficiente.

## Conclusiones

Este sistema de gestión de citas médicas busca mejorar la experiencia del paciente y optimizar la agenda de los médicos. Con funciones robustas y notificaciones automáticas, el sistema está diseñado para facilitar la programación y gestión de citas médicas.

Para más información o si tienes preguntas, no dudes en abrir un issue en el repositorio.

## Información Técnica

### Requisitos del Sistema

- **Python**: 3.12 o superior
- **Sistema Operativo**: Windows, Linux o macOS
- **Gestor de Paquetes**: pip

### Bibliotecas Utilizadas

Este proyecto utiliza varias bibliotecas para facilitar el desarrollo y mejorar la funcionalidad. A continuación se presenta una lista de las principales bibliotecas utilizadas:

1. **pytest**: 
   - Descripción: Un marco de pruebas que permite la creación y ejecución de pruebas de forma sencilla.
   - Instalación: `pip install pytest`

2. **Rich**:
   - Descripción: Una biblioteca para imprimir en la consola con colores y estilos, mejorando la interfaz de usuario.
   - Instalación: `pip install rich`

3. **Pandas** (si se utiliza para la manipulación de datos):
   - Descripción: Una biblioteca para la manipulación y análisis de datos, especialmente útil para trabajar con datos tabulares.
   - Instalación: `pip install pandas`

4. **OpenPyXL** (si se utiliza para la exportación a Excel):
   - Descripción: Una biblioteca para leer y escribir archivos Excel (XLSX).
   - Instalación: `pip install openpyxl`

   ### Entorno Virtual

Es recomendable usar un entorno virtual para gestionar las dependencias del proyecto. A continuación, se describen los pasos para crear y activar un entorno virtual.

1. **Crear un Entorno Virtual**:

   Navega al directorio raíz del proyecto y ejecuta el siguiente comando:

   ```bash
   python -m venv venv


 ### Clonar el Repositorio

Para comenzar a trabajar en el proyecto, primero necesitas clonar el repositorio. Usa el siguiente comando en tu terminal:

```bash
git clone <URL-del-repositorio>