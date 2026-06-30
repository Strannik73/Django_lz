from django.test import TestCase
from .models import Song

class SongModelTest(TestCase):
    def test_song_creation(self):
        song = Song.objects.create(title="Test Song", artist="Test Artist")
        self.assertEqual(song.title, "Test Song")
        self.assertTrue(isinstance(song, Song))

    def test_songs_list_view(self):
        response = self.client.get('/songs/')
        self.assertEqual(response.status_code, 200)