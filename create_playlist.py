import json
import os
import googleapiclient

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import requests
import youtube_dl

from exceptions import ResponseException

from secrets import spotify_token, spotify_user_id


class CreatePlaylist:

    def __init__(self) -> object:

        self.youtube_client = self.get_youtube_client()
        self.all_song_info = {}

    @property

    def get_youtube_client(self):

        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "client_secret.json"

        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()

        youtube_client = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        return youtube_client

    def get_liked_videos(self):

        request = self.youtube_client.videos().list(
            part="snippet,contentDetails,statistics",
            myRating="like"
        )
        response = request.execute()

        for item in response["items"]:

            video_title = item["snippet"]["title"]
            youtube_url = "https://www.youtube.com/watch?v={}".format(item["108482799333-3mh0recht4dhapuei40jimedc5o28vq8.apps.googleusercontent.com"])

            video = youtube_dl.YoutubeDL({}).extract_info(
                youtube_url, download=False)

            song_name = video["track"]

            artist = video["artist"]

            if song_name is not None and artist is not None:

                self.all_song_info[video_title] = {
                    "youtube_url": youtube_url,
                    "song_name": song_name,
                    "artist": artist,

                    "spotify_uri": self.get_spotify_uri(song_name, artist)

                }

    def create_playlist(self):

        request_body = json.dumps({
            "name": "Youtube Liked Vids",
            "description": "All Liked Youtube Videos",
            "public": True
        })

        query = "https://api.spotify.com/v1/users/{user_id}/playlists".format(
            spotify_user_id)

        response = requests.post(
            query,
            data=request_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(BQDgtesy-c5ZY3GLXcFjX7pcq7iMNEKdSXoM1_l7XUwUBRSuTpNVcwZuLrMQMxKpmkxXvbyDWDfJ1vKnOs-dOr1ccjgm6LnO4igNxqMqSQndU6iHhdNcv1CveMnqaEcI0__VK4fUQxpMX8rXoT2ynXRfMl1jWrsW74h0K13Qebp9TEmE1Q)
            }
        )
        response_json = response.json()

        return response_json["108482799333-3mh0recht4dhapuei40jimedc5o28vq8.apps.googleusercontent.com"]

    def get_spotify_uri(self, song_name, artist):

        query = "https://api.spotify.com/v1/users/taylorheil/playlists" .format(
            song_name,
            artist
        )
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(BQDgtesy-c5ZY3GLXcFjX7pcq7iMNEKdSXoM1_l7XUwUBRSuTpNVcwZuLrMQMxKpmkxXvbyDWDfJ1vKnOs-dOr1ccjgm6LnO4igNxqMqSQndU6iHhdNcv1CveMnqaEcI0__VK4fUQxpMX8rXoT2ynXRfMl1jWrsW74h0K13Qebp9TEmE1Q)
            }
        )

        response_json = response.json()

        songs = response_json["tracks"]["items"]


        uri = songs[0]["uri"]

        return uri

    def add_song_to_playlist(self):

        self.get_liked_videos()

        uris = [info["spotify_uri"]
                for song, info in self.all_song_info.items()]

        playlist_id = self.create_playlist()

        request_data = json.dumps(uris)

        query = "https://api.spotify.com/v1/users/{user_id}/playlists".format(
            playlist_id)

        response = requests.post(
            query,
            data=request_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(BQDgtesy-c5ZY3GLXcFjX7pcq7iMNEKdSXoM1_l7XUwUBRSuTpNVcwZuLrMQMxKpmkxXvbyDWDfJ1vKnOs-dOr1ccjgm6LnO4igNxqMqSQndU6iHhdNcv1CveMnqaEcI0__VK4fUQxpMX8rXoT2ynXRfMl1jWrsW74h0K13Qebp9TEmE1Q)
            }
        )

        if response.status_code != 200:
            raise ResponseException(response.status_code)

        response_json = response.json()

        return response_json


if __name__ == '__main__':

    cp = CreatePlaylist()
    cp.add_song_to_playlist()
