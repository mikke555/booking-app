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


class UserAlreadyExists(AppException):
    status_code = 409
    detail = "User with this email already exists"


class Unauthorized(AppException):
    status_code = 401
    detail = "Unauthorized"
    headers = {"WWW-Authenticate": "Bearer"}


class InvalidToken(Unauthorized):
    detail = "Could not validate credentials"


class InvalidCredentials(Unauthorized):
    detail = "Invalid email or password"
