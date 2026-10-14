from fastapi import status
from app.enums import ErrorCode

class AppException(Exception):
    def __init__(self, status_code: int, detail: ErrorCode):
        self.status_code = status_code
        self.detail = detail
        super().__init__()


class NotFoundUserException(AppException):
    """User doesn't exist"""
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=ErrorCode.USER_DOESNT_EXIST)


class UnauthorizedException(AppException):
    """User is unauthorized"""
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=ErrorCode.UNAUTHORIZED)


class AuthorizedException(AppException):
    """User is authorized"""
    def __init__(self):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=ErrorCode.AUTHORIZED)


class NoPermissionsException(AppException):
    """User don't have permissions for this action"""
    def __init__(self):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=ErrorCode.NO_PERMISSIONS)


class NotFoundLanguageException(AppException):
    """Language doesn't exist or it's private"""
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=ErrorCode.LANGUAGE_DOESNT_EXIST)


class NotFoundNoteException(AppException):
    """Note doesn't exist or it's language is private"""
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=ErrorCode.NOTE_DOESNT_EXIST)

