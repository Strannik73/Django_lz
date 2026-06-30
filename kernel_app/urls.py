from django.urls import path

from app.views import (
    create_song,
    rate_song,
    register,
    song_cover,
    song_details,
    songs,
    to_login,
)

urlpatterns = [
    path("", to_login),
    path("song/<int:song_id>/", song_details, name="song_detail"),
    path("songs/", songs, name="songs"),
    path("cover/<int:song_id>/", song_cover, name="song_cover"),
    path("register/", register, name="register"),
    path("rate/<int:song_id>/", rate_song, name="rate_song"),
    path("create/", create_song, name="create_song"),
]