class AppException(Exception):
    status_code = 500
    detail = "Application error"
    headers: dict[str, str] | None = None


class ObjectNotFoundError(AppException):
    status_code = 404
    detail = "Object not found"


class HotelNotFoundError(ObjectNotFoundError):
    detail = "Hotel not found"


class RoomNotFoundError(ObjectNotFoundError):
    detail = "Room not found"


class AmenityNotFoundError(ObjectNotFoundError):
    detail = "Amenity not found"


class ObjectAlreadyExistsError(AppException):
    status_code = 409
    detail = "Object already exists"


class HotelAlreadyExistsError(ObjectAlreadyExistsError):
    detail = "Hotel with this name already exists"


class UserAlreadyExistsError(ObjectAlreadyExistsError):
    detail = "User with this email already exists"


class AmenityAlreadyExistsError(ObjectAlreadyExistsError):
    detail = "Amenity with this name already exists"


class RoomNotAvailableError(AppException):
    status_code = 409
    detail = "Room is not available for the requested dates"


class UnauthorizedError(AppException):
    status_code = 401
    detail = "Unauthorized"
    headers = {"WWW-Authenticate": "Bearer"}


class ForbiddenError(AppException):
    status_code = 403
    detail = "Admin privileges required"


class InvalidTokenError(UnauthorizedError):
    detail = "Could not validate credentials"


class InvalidCredentialsError(UnauthorizedError):
    detail = "Invalid email or password"
