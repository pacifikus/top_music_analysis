import click
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from top_music_analysis.config import (
    PLAYLIST_IDS,
    SPOTIFY_CLIENT_ID,
    SPOTIFY_SECRET,
)


def init_spotify():
    auth_manager = SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_SECRET,
    )

    return spotipy.Spotify(auth_manager=auth_manager)


SPOTIFY = init_spotify()


def get_100_tracks_from_playlist(playlist_id):
    playlist_info = SPOTIFY.playlist(playlist_id=playlist_id)
    result = playlist_info["tracks"]["items"]
    result = [
        {
            "id": item["track"]["id"],
            "name": item["track"]["name"],
            "artist": item["track"]["artists"][0]["name"],
            "popularity": item["track"]["popularity"],
        }
        for item in result
    ]
    return playlist_info["name"], result


def get_track_features(tracks):
    track_features = SPOTIFY.audio_features(tracks=tracks)
    return track_features


def get_data():
    data = {}
    for item in PLAYLIST_IDS:
        key, value = get_100_tracks_from_playlist(item)
        tracks_features = get_track_features([item["id"] for item in value])
        for i in range(len(value)):
            value[i]["audio_features"] = tracks_features[i]
        data[key] = value
    return data


def to_dataframe(data):
    df = pd.concat({k: pd.DataFrame(v) for k, v in data.items()})
    df = pd.concat(
        [
            df.drop(["audio_features"], axis=1),
            df["audio_features"].apply(pd.Series),
        ],
        axis=1,
    )
    df.drop(
        ["id", "uri", "analysis_url", "time_signature", "type", "track_href"],
        axis=1,
        inplace=True,
    )
    return df


@click.command()
@click.option("--out", default="spotify_res.csv", help="Output data path")
def start(out):
    data = get_data()
    df = to_dataframe(data)
    df.to_csv(out)


if __name__ == "__main__":
    start()
