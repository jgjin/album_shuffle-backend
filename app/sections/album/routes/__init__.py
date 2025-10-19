from random import shuffle
import time
from typing import Sequence

import aiohttp
from async_lru import alru_cache
from fastapi import APIRouter, Request, HTTPException

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
            spotify_url=item["album"]["external_urls"]["spotify"],
        )
        for item in (
            await list_albums(access_token, get_ttl_hash(ttl_seconds=(24 * 60 * 60)))
        )
    ]
    shuffle(albums)

    return ListAlbumResponse(albums=albums)


@alru_cache()
async def list_albums(access_token: str, ttl_hash: int) -> Sequence[dict]:
    del ttl_hash

    albums = []
    async with aiohttp.ClientSession(
        headers={"Authorization": f"Bearer {access_token}"}
    ) as session:
        while chunk := (await get_saved_albums(session, limit=20, offset=len(albums)))[
            "items"
        ]:
            albums.extend(chunk)

    return albums


async def get_saved_albums(
    session: aiohttp.ClientSession,
    limit: int,
    offset: int,
) -> Sequence[dict]:
    async with session.get(
        "https://api.spotify.com/v1/me/albums",
        params={
            "limit": limit,
            "offset": offset,
        },
    ) as response:
        return await response.json()


def get_ttl_hash(ttl_seconds: int) -> int:
    return round(time.time() / ttl_seconds)
