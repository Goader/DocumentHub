class ServiceException(RuntimeError):
    """Raised when the service responds with error code"""
    pass


class TranslatorException(ServiceException):
    """Raised when the translator service responds with error code"""


class TikaException(ServiceException):
    """Raised when the tika service responds with error code"""


class ElasticSearchException(ServiceException):
    """Raised when the ElasticSearch service responds with error code"""
