import os

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.constants import SESSION_MAX_AGE
from app.sections.auth.routes import router as auth_router
from app.sections.album.routes import router as album_router


app = FastAPI()
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET_KEY"),
    max_age=SESSION_MAX_AGE,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router, prefix="/auth")
app.include_router(album_router, prefix="/album")


@app.get("/")
async def home(request: Request):
    if request.session.get("access_token"):
        return RedirectResponse(os.getenv("FRONTEND_URL"))

    return RedirectResponse("/auth/login")
