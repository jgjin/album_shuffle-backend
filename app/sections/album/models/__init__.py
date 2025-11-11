from pydantic import BaseModel


class Album(BaseModel):
    image_url: str
    name: str
    artist: str

    album_url: str
    artist_url: str


class ListAlbumResponse(BaseModel):
    albums: list[Album]
