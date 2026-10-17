from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.config import settings
from app.exceptions import AppException
from app.routers import users, auth, languages, notes


app = FastAPI(
    title="klinvo-backend",
    description=(
        "**Klinvo** - web application for making artificial languages (conlangs)."
        "The application is set of tools for it"
    ),
    version="0.4.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",

    contact={
        "name": "Defulan",
        "url": "https://github.com/Defulan"
    },

    license_info={
        "name": "MIT License",
        "url": "https://github.com/Defulan/klinvo-frontend/blob/main/LICENSE"
    }
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

@app.get("/")
def health_function():
    return {
        "message": f"{app.title} | {app.version} | {app.docs_url}",
        "contact": f"{app.contact.name}, {app.contact.url}"
    }

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(languages.router)
app.include_router(notes.router)
