from django.contrib.auth.models import User
from django.db import models

class Song(models.Model):
    song_id = models.AutoField(primary_key=True)
    song_name = models.CharField(max_length=20, verbose_name="Название", null=False)
    song_lyrics = models.TextField(verbose_name="Текст песни", null=True)
    song_artist = models.CharField(max_length=40, verbose_name="Исполнитель", null=False)
    song_genre = models.CharField(max_length=40, verbose_name="Жанры", null=False)
    creation_date = models.DateTimeField(verbose_name="Дата", auto_now_add=True)
    song_cover = models.BinaryField(verbose_name="Превью", null=False, default=b"")

    def __str__(self):
        return f"Песня: {self.song_name}"

class Song_Rating(models.Model):
    song = models.ForeignKey("Song", verbose_name="Песня", on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    rating = models.IntegerField(verbose_name="Оценка")

    class Meta:
        unique_together = ("song", "user")
        
    def __str__(self):
        return f"{self.user.username} оценил {self.song.song_name}: {self.rating}"