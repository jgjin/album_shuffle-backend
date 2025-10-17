from pydantic import BaseModel


class Album(BaseModel):
    image_url: str
    name: str
    artist: str
    spotify_url: str


class ListAlbumResponse(BaseModel):
    albums: list[Album]
