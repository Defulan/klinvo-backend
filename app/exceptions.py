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
