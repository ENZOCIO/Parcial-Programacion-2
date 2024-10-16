# Mejoras en el Sistema de Gestión de Citas Médicas

## Modificaciones Realizadas

1. **Corregir las Notificaciones**:
   - Se ajustó el método `enviar_notificacion()` para que los datos de contacto (correo, celular, etc.) pertenezcan a la clase `Persona`, no a la clase `Notificacion`.
   - Se implementó la herencia para el método `enviar_notificacion()` en las diferentes formas de notificación (correo, SMS, WhatsApp).

2. **Agregar WhatsApp como Forma de Notificación**:
   - Se implementó la funcionalidad para enviar notificaciones a través de WhatsApp, integrando la función correspondiente.

3. **Corregir Agenda - Cita**:
   - Se revisó la estructura de la clase `Agenda` para asegurar que cada médico tenga su propia agenda o, alternativamente, una agenda general en el hospital.

4. **Corregir Usuarios**:
   - Se eliminó la noción de "usuarios" en el sistema, reemplazándola con la terminología adecuada de "pacientes".

5. **Crear Métodos de Búsqueda**:
   - Se implementaron los métodos `buscar_paciente()` y `buscar_medico()` en la clase `Hospital` para facilitar la búsqueda de información.

6. **Corregir Agendar y Cancelar Cita**:
   - Se movieron los métodos de agendar y cancelar citas desde la clase `Paciente` a la clase `Agenda`, asegurando que la gestión de citas se maneje en el contexto adecuado.

7. **Buscar Datos de una Cita**:
   - Se implementaron mecanismos para buscar información de citas tanto desde el contexto del paciente como del hospital.

8. **Revisar Mover Citas**:
   - Se revisó la lógica de mover citas para asegurar que se manejen adecuadamente en la agenda.

9. **Mejorar la Interfaz de Texto**:
   - Se utilizó la biblioteca Rich para mejorar la presentación de menús y reportes en la interfaz de texto.

10. **Cargar Datos Iniciales desde Archivos**:
    - Se implementó la funcionalidad para cargar datos iniciales de pacientes, médicos y citas desde archivos en formato CSV y JSON.

11. **Manejo de Citas con Fecha y Hora**:
    - Se ajustó el sistema para que las citas incluyan tanto fecha como hora, permitiendo intervalos de 20 minutos.

12. **Selección de Especialidad para Citas**:
    - Se implementó un mecanismo que permite al paciente seleccionar una especialidad y muestra los médicos disponibles con esa especialidad.

## Mejoras Propias

1. **Implementación del Sistema de Feedback**:
   - Se añadió un sistema de feedback que permite a los pacientes proporcionar comentarios sobre su experiencia, facilitando mejoras continuas en el servicio.

2. ***Realizacion de un nuevo sistema de notificaciones**:
   - Se mejoro el anteriormente implementado por uno mas apto y correcto a la hora de notificar a un paciente cuando registra una cita correctamente
