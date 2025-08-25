import os

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from app.oauth import spotify


router = APIRouter()


@router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("authorize")
    return await spotify.authorize_redirect(request, redirect_uri)


@router.get("/authorize")
async def authorize(request: Request):
    token = await spotify.authorize_access_token(request)
    request.session.update({"access_token": token["access_token"]})

    return RedirectResponse(os.getenv("FRONTEND_URL"))
