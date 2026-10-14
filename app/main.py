from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.config import settings
from app.exceptions import AppException
from app.routers import users, auth, languages, notes


app = FastAPI(
    title="klinvo-backend",
    version="0.3.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY
)

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exception: AppException):
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "detail": exception.detail
        }
    )

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(languages.router)
app.include_router(notes.router)
