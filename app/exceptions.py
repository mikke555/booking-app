class AppException(Exception):
    status_code = 500
    detail = "Application error"
    headers: dict[str, str] | None = None


class ObjectNotFound(AppException):
    status_code = 404
    detail = "Object not found"


class HotelNotFound(ObjectNotFound):
    detail = "Hotel not found"


class RoomNotFound(ObjectNotFound):
    detail = "Room not found"


class InvalidToken(AppException):
    status_code = 401
    detail = "Could not validate credentials"
    headers = {"WWW-Authenticate": "Bearer"}
