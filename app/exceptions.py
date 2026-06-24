class AppException(Exception):
    status_code = 500
    detail = "Application error"


class ObjectNotFoundException(AppException):
    status_code = 404
    detail = "Object not found"


class HotelNotFoundException(ObjectNotFoundException):
    detail = "Hotel not found"
