from typing import Generic, TypeVar, Any
from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    success: bool = True
    message: str = "Success"
    data: T | None = None

    @classmethod
    def ok(cls, data: T | None = None, message: str = "Success") -> "ApiResponse":
        return cls(success=True, message=message, data=data)

    @classmethod
    def fail(cls, message: str = "Something went wrong") -> "ApiResponse":
        return cls(success=False, message=message, data=None)
