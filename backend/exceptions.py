from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError

# ============================================
# CUSTOM EXCEPTION CLASS
# Your own error type for business logic errors
# ============================================
class DocuMindException(Exception):
    def __init__(self, status_code: int, message: str, details: str = None):
        self.status_code = status_code
        self.message = message
        self.details = details

# ============================================
# HANDLER — catches DocuMindException anywhere
# ============================================
async def documind_exception_handler(request: Request, exc: DocuMindException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.message,
            "details": exc.details
        }
    )

# ============================================
# HANDLER — catches Pydantic validation errors
# Makes them readable instead of technical
# ============================================
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        errors.append({
            "field": " → ".join(str(x) for x in error["loc"]),
            "issue": error["msg"]
        })
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status": "error",
            "message": "Validation failed",
            "details": errors
        }
    )

# ============================================
# HANDLER — catches database integrity errors
# Like duplicate email on registration
# ============================================
async def integrity_exception_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "status": "error",
            "message": "Database integrity error",
            "details": "A record with this data already exists"
        }
    )