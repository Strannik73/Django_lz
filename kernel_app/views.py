from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Avg, Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from app.forms import Song_Form
from app.models import Song, Song_Rating


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})


def to_login(request):
    return redirect("login")


@login_required
def song_details(request, song_id):
    song = get_object_or_404(Song, song_id=song_id)
    avg_rating = Song_Rating.objects.filter(song=song).aggregate(Avg("rating"))[
        "rating__avg"
    ]
    votes_count = Song_Rating.objects.filter(song=song).count()
    my_rating = Song_Rating.objects.filter(song=song, user=request.user).first()
    context = {
        "song": song,
        "avg_rating": avg_rating,
        "votes_count": votes_count,
        "my_rating": my_rating.rating if my_rating else None,
    }
    return render(request, "song.html", context)


@login_required
def songs(request):
    songs = Song.objects.annotate(
        avg_rating=Avg("song_rating__rating"),
        votes_count=Count("song_rating", distinct=True),
    )
    ratings = Song_Rating.objects.filter(user=request.user)
    user_ratings = {str(r.song.song_id): r.rating for r in ratings}
    for song in songs:
        song.my_rating = next((r.rating for r in ratings if r.song.song_id == song.song_id), None)
    return render(request, "songs.html", {"songs": songs, "user_ratings": user_ratings})


def song_cover(request, song_id):
    song = Song.objects.get(song_id=song_id)
    return HttpResponse(song.song_cover, content_type="image/jpeg")


@login_required
def rate_song(request, song_id):
    song = get_object_or_404(Song, song_id=song_id)
    exists = Song_Rating.objects.filter(song=song, user=request.user).exists()
    if not exists:
        Song_Rating.objects.create(
            song=song, user=request.user, rating=int(request.POST["rating"])
        )
    return redirect("songs")


@staff_member_required
def create_song(request):
    if request.method == "POST":
        form = Song_Form(request.POST, request.FILES)
        if form.is_valid():
            cover_file = form.cleaned_data["song_cover"]
            song = Song(
                song_name=form.cleaned_data["song_name"],
                song_lyrics=form.cleaned_data["song_lyrics"],
                song_artist=form.cleaned_data["song_artist"],
                song_genre=form.cleaned_data["song_genre"],
                creation_date=form.cleaned_data["creation_date"],
            )
            if cover_file:
                song.song_cover = cover_file.read()
            song.save()
            return redirect("songs")
    else:
        form = Song_Form()
    return render(request, "create_song.html", {"form": form})