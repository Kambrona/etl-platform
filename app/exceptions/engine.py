"""
Excepciones del motor ETL.
"""


class ETLPlatformException(Exception):
    """Excepción base del proyecto."""


class PipelineException(ETLPlatformException):
    """Error relacionado con un pipeline."""


class PipelineNotFoundException(PipelineException):
    """No se encontró el pipeline."""


class InvalidPipelineException(PipelineException):
    """La definición del pipeline es inválida."""


class StepException(ETLPlatformException):
    """Error durante la ejecución de un paso."""


class StepNotRegisteredException(StepException):
    """El tipo de paso no está registrado."""


class StepExecutionException(StepException):
    """Un paso produjo un error durante su ejecución."""


class ConfigurationException(ETLPlatformException):
    """Configuración inválida."""