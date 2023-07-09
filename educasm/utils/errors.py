from rest_framework.exceptions import NotFound, AuthenticationFailed, ParseError
from rest_framework import status


class NotFoundError(NotFound):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'No encontrado.'
    default_code = 'not_found'

    def __init__(self, detail):
        self.detail = {
            'msg': detail
        }

class NotAuthError(AuthenticationFailed):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'No autorizado.'
    default_code = 'authentication_failed'

    def __init__(self, detail):
        self.detail = {
            'msg': detail
        }

class ServerError(ParseError):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'Error inesperado.'
    default_code = 'server_error'

    def __init__(self, detail):
        self.detail = {
            'msg': detail
        }