from django import forms

class Song_Form(forms.Form):
    song_name = forms.CharField(max_length=100)
    song_lyrics = forms.CharField(max_length=1000)
    song_artist = forms.CharField(max_length=100)
    song_genre = forms.CharField(max_length=100)
    creation_date = forms.DateTimeField(required=False)
    song_cover = forms.FileField(required=False)