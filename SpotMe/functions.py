import requests
import json
import streamlit as st
import pandas as pd
import re
import plotly.express as px
import nltk
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

nltk.download('punkt')
nltk.download('stopwords')


def save_to_file(data, filename):
    with open(filename, 'w') as write_file:
        json.dump(data, write_file, indent=2)


def read_from_file(filename):
    with open(filename, 'r') as read_file:
        data = json.load(read_file)
    return data


def validate(message):
    if type(message) != type('string'):
        return message["message"]["header"]["status_code"] == 200

    return False


# Music-Match API Requests
# Get Top Artists
def request_top_artists(country_code):
    top_artists_url = "https://api.musixmatch.com/ws/1.1/" \
                      "chart.artists.get?country={0}&page_size=10" \
                      "&apikey=2906e8d0e6af754ab7f5a94505268889".format(country_code)
    top_artists = requests.get(top_artists_url).json()
    return top_artists


# Get Top Tracks
def request_top_tracks(country_code, chart_name):
    top_tracks_url = "https://api.musixmatch.com/ws/1.1/" \
                     "chart.tracks.get?country={0}&chart_name={1}&page_size=10" \
                     "&apikey=2906e8d0e6af754ab7f5a94505268889".format(country_code, chart_name)
    top_tracks = requests.get(top_tracks_url).json()
    return top_tracks


# Get Artist Country
def request_artist_country(artist_id):
    artist_country_url = "https://api.musixmatch.com/ws/1.1/" \
                         "artist.get?artist_id={0}" \
                         "&apikey=2906e8d0e6af754ab7f5a94505268889".format(artist_id)
    artist_country = requests.get(artist_country_url).json()
    return artist_country


def request_artist_albums(artist_ids):
    artist_album_url = "https://api.musixmatch.com/ws/1.1/" \
                       "artist.albums.get?artist_id={0}" \
                       "&apikey=2906e8d0e6af754ab7f5a94505268889".format(artist_ids)

    artist_albums = requests.get(artist_album_url).json()
    return artist_albums


def request_album_tracks(album_ids):
    album_track_url = "https://api.musixmatch.com/ws/1.1/" \
                      "album.tracks.get?album_id={0}" \
                      "&apikey=2906e8d0e6af754ab7f5a94505268889".format(album_ids)

    album_tracks = requests.get(album_track_url).json()
    return album_tracks


def request_track_lyrics(track_ids):
    track_lyrics_url = "https://api.musixmatch.com/ws/1.1/" \
                       "track.lyrics.get?track_id={0}" \
                       "&apikey=2906e8d0e6af754ab7f5a94505268889".format(track_ids)

    track_lyrics = requests.get(track_lyrics_url).json()
    return track_lyrics


def lyricsCleaner(lyrics: str) -> str:
    """ This function takes a string as input and returns the same
    string (lower case) without [] including what's inside, () keeping
    what is inside, and \n """
    modified_lyrics = re.sub(r"\[.*?\]", "", lyrics)
    modified_lyrics2 = modified_lyrics.replace("(", "").replace(")", "")
    return modified_lyrics2.replace("\n", " ").lower()


def lyricsToList(lyrics: str) -> list:
    """ This function takes a string as input, removes [] including
    what is inside, () keeping what is inside, and \n, and returns a
    list of words (lower case) """
    modified_lyrics = re.sub(r"\[.*?\]", "", lyrics)
    modified_lyrics2 = modified_lyrics.replace("(", "").replace(")", "")
    verses = modified_lyrics2.split('\n')
    words = [word.lower() for i in verses for word in i.split()]
    return words


def trackHelper(album_id) -> list:
    all_lyrics = ""
    track_names = []
    track_ratings = []
    lyrics_array = []
    output = []

    tracks = request_album_tracks(album_id)
    for i in tracks["message"]["body"]["track_list"]:
        track_ids = i["track"]["track_id"]
        track_names.append(i["track"]["track_name"])
        track_ratings.append(i["track"]["track_rating"])
        lyrics = request_track_lyrics(track_ids)
        if validate(lyrics):
            lyrics = lyrics["message"]["body"]["lyrics"]["lyrics_body"]
            lyrics = lyrics[:-73]
            all_lyrics += lyrics

    lyrics_array.append(all_lyrics)
    output.append(lyrics_array)
    output.append(track_names)
    output.append(track_ratings)

    return output


def clean_lyrics(tokens, stopwords, pronouns=None):
    clean_tokens = []
    if pronouns:
        stopwords = stopwords + pronouns
    for word in tokens:
        if word not in stopwords:
            clean_tokens.append(word)
    return clean_tokens


def filter_by_length(list_of_tuples, l):
    filtered_list = [t for t in list_of_tuples if len(t[0]) >= l]
    return filtered_list


def generate_frequency_distribution(lyrics):
    stopwords = ["\'s", ",", "to", "and", "a", "an", "so", "not",
                 "through", "the", "of", "that", "out", "at",
                 "from", "by", "for", "off", "on", "in", "'ve",
                 "are", "is", "n't", "'ll", "do", "will", "did",
                 "would", "can", "could", "'re", "'m", "na", "no",
                 "ca", "wo", "was", "were", "got", "even", "gon",
                 "it", "?", "but", "oh", "ooh", "da", "'", "with",
                 "what", "when", "which", "just", "yeah", "up",
                 "down", "be", "ha", "uh", "huh", "about", "ta",
                 "this", "that", "those", "these", "'d"]
    pronouns = ["they", "them", "their", "theirs",
                "you", "your", "yours",
                "i", "me", "my", "mine",
                "he", "him", "his",
                "she", "her", "hers",
                "we", "our", "ours",
                "it", "its"]

    # Separate the string into a list of strings
    tokens = word_tokenize(lyricsCleaner(lyrics))

    # Remove stopwords and pronouns
    clean_tokens = clean_lyrics(tokens, stopwords, pronouns)

    # Generate the frequency distribution
    fdist = FreqDist(clean_tokens)
    most_common_words = fdist.most_common()
    return most_common_words


def generate_plot(tuples_freq_dist):
    # Notice that we have several words, let's show the first 10
    data = pd.DataFrame(tuples_freq_dist[:10])
    dataframe = pd.DataFrame({
        'Words': data[0],
        'Count': data[1]
    })

    fig = px.line(dataframe, x="Count", y="Words", title='')
    fig['layout']['yaxis']['autorange'] = "reversed"

    st.plotly_chart(fig)
