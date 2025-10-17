from functools import lru_cache
from random import shuffle
import time
from typing import Sequence

from fastapi import APIRouter, Request, HTTPException
from spotipy import Spotify

from app.sections.album.models import Album, ListAlbumResponse

router = APIRouter()


@router.get("/list")
async def list(request: Request) -> ListAlbumResponse:
    access_token = request.session.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401)

    albums = [
        Album(
            image_url=item["album"]["images"][0]["url"],
            name=item["album"]["name"],
            artist=item["album"]["artists"][0]["name"],
        )
        for item in list_albums(access_token, get_ttl_hash(ttl_seconds=(12 * 60 * 60)))
    ]
    shuffle(albums)

    return ListAlbumResponse(albums=albums)


@lru_cache()
def list_albums(access_token: str, ttl_hash: int) -> Sequence[dict]:
    spotify = Spotify(auth=access_token)
    del ttl_hash

    albums = []
    while chunk := spotify.current_user_saved_albums(offset=len(albums))["items"]:
        albums.extend(chunk)

    return albums


def get_ttl_hash(ttl_seconds: int) -> int:
    return round(time.time() / ttl_seconds)
