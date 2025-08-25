from fastapi import APIRouter, Request, HTTPException
from spotipy import Spotify

from app.sections.album.models import Album, ListAlbumResponse

router = APIRouter()


@router.get("/list")
async def list(request: Request) -> ListAlbumResponse:
    access_token = request.session.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401)
    spotify = Spotify(auth=access_token)

    albums = []
    while chunk := spotify.current_user_saved_albums(offset=len(albums))["items"]:
        albums.extend(
            Album(
                image_url=item["album"]["images"][0]["url"],
                name=item["album"]["name"],
                artist=item["album"]["artists"][0]["name"],
            )
            for item in chunk
        )

    return ListAlbumResponse(albums=albums)
