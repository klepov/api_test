from rest_framework.exceptions import APIException


class OnlyHr(APIException):
    status_code = 403
    default_detail = 'только HR могут менять этот параметр'
    default_code = 'ошибка доступа'
