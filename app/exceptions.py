class AppException(Exception):
    status_code = 500
    detail = "Application error"


class ObjectNotFound(AppException):
    status_code = 404
    detail = "Object not found"


class HotelNotFound(ObjectNotFound):
    detail = "Hotel not found"
