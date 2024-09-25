# Unemi Audit Kafka

`unemi-audi-kafka` es una aplicación reutilizable de Django que audita automáticamente los cambios en los modelos (creación, actualización, eliminación) en todos los modelos de tu proyecto Django. Se integra con Kafka para el envío de logs y permite una auditoría configurable para los modelos importantes. La aplicación captura metadatos útiles como el usuario que realizó los cambios, la IP de la solicitud, la URL y más.

## Características

- **Auditoría Automática**: Registra automáticamente todos los modelos de Django para el registro de auditoría.
- **Integración con Kafka**: Utiliza `confluent_kafka` para enviar los registros de auditoría a los temas de Kafka..
- **Auditoría de Configuración**: Registra manualmente modelos importantes para la auditoría de configuración..
- **Middleware de Contexto de Usuario**: Captura información sobre el usuario, la IP de la solicitud y el agente de usuario a través de middleware.
- **Personalizable**: Puedes extender o sobrescribir middleware, y controlar el comportamiento del productor de Kafka.

## Instalación

1. **INSTALAR la librería usando pip**:

   ```bash
   pip install unemi-audi-kafka
   
2. **Agregar la libreria en Django INSTALLED_APPS**:

    En tu `settings.py`, configura las aplicaciones:
    ```python
   INSTALLED_APPS = [
       # Other installed apps
       'audit_logger',
   ]

3. **Agregar el MIDDLEWARE**:

    En tu `settings.py`, configura las middlewares:
    ```python
   MIDDLEWARE = [
       # Other middlewares
       'audit_logger.middlewares.AuditUserMiddleware',
   ]

4. **Agregar CONFIGURACIONES DE KAFKA**:
    
    En tu `settings.py`, configurar los Kafka broker y topics:
    ```python
    KAFKA_BROKER_URL = 'localhost:9092'  # Replace with your Kafka broker URL
    KAFKA_TOPIC_LOGS = 'audit_logs'      # Topic for log auditing
    KAFKA_TOPIC_ERRORS = 'audit_errors'  # Topic for error logging
    KAFKA_TOPIC_CONFIG = 'audit_config'  # Topic for configuration auditing


## Opcional
Si deseas guardar las configuraciones de tu aplicacion, la puedes separar de los otras tablas con:

En tu `models.py`, agregar modelo manualmente:
   
   ```python
   from audit_logger import AuditLogger
   
    class Configuracion(ModelBase):
    nombre = models.CharField(unique=True, max_length=100, verbose_name=u'Nombre')
   
   # Registrar Configuracion
   AuditLogger.register_auditoria_config(Configuracion)