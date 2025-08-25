import os

from authlib.integrations.starlette_client import OAuth


oauth = OAuth()
spotify = oauth.register(
    name="spotify",
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    authorize_url="https://accounts.spotify.com/authorize",
    access_token_url="https://accounts.spotify.com/api/token",
    client_kwargs={"scope": "user-library-read"},
)
