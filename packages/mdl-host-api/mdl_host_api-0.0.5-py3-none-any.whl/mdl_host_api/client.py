import requests
from .task import Task
from .exceptions import APIError

class Client:
    def __init__(self, host_url, api_key):
        self.host_url = host_url
        self.api_key = api_key
        self.headers = {"X-API-Key": api_key, "Content-Type": "application/json"}
        self.send_task = self.SendTask(self)
        self.youtube = self.YouTube(self)
        self.spotify = self.Spotify(self)
    
    class YouTube:
        def __init__(self, client):
            self.client = client

        def get_video(self, url, video_format="bestvideo", audio_format="bestaudio"):
            data = {"url": url, "video_format": video_format, "audio_format": audio_format}
            response = requests.post(f"{self.client.host_url}/yt_get_video", json=data, headers=self.client.headers)
            if response.status_code != 200:
                raise APIError(response.json().get('error', 'Unknown error'))
            return Task(self.client, response.json()['task_id'], 'yt_get_video')

        def get_audio(self, url, audio_format="bestaudio"):
            data = {"url": url, "audio_format": audio_format}
            response = requests.post(f"{self.client.host_url}/yt_get_audio", json=data, headers=self.client.headers)
            if response.status_code != 200:
                raise APIError(response.json().get('error', 'Unknown error'))
            return Task(self.client, response.json()['task_id'], 'yt_get_audio')

        def get_live_video(self, url, duration, start=0, video_format="bestvideo", audio_format="bestaudio"):
            data = {"url": url, "start": start, "duration": duration, "video_format": video_format, "audio_format": audio_format}
            response = requests.post(f"{self.client.host_url}/yt_get_live_video", json=data, headers=self.client.headers)
            if response.status_code != 200:
                raise APIError(response.json().get('error', 'Unknown error'))
            return Task(self.client, response.json()['task_id'], 'yt_get_live_video')

        def get_live_audio(self, url, duration, start=0, audio_format="bestaudio"):
            data = {"url": url, "start": start, "duration": duration, "audio_format": audio_format}
            response = requests.post(f"{self.client.host_url}/yt_get_live_audio", json=data, headers=self.client.headers)
            if response.status_code != 200:
                raise APIError(response.json().get('error', 'Unknown error'))
            return Task(self.client, response.json()['task_id'], 'yt_get_live_audio')

        def get_info(self, url):
            data = {"url": url}
            response = requests.post(f"{self.client.host_url}/yt_get_info", json=data, headers=self.client.headers)
            if response.status_code != 200:
                raise APIError(response.json().get('error', 'Unknown error'))
            return Task(self.client, response.json()['task_id'], 'yt_get_info')
        
    class Spotify:
        def __init__(self, client):
            self.client = client

        def get_track(self, url):
            data = {"url": url}
            response = requests.post(f"{self.client.host_url}/sp_get_track", json=data, headers=self.client.headers)
            if response.status_code != 200:
                raise APIError(response.json().get('error', 'Unknown error'))
            return Task(self.client, response.json()['task_id'], 'sp_get_track')

        def get_info(self, url):
            data = {"url": url}
            response = requests.post(f"{self.client.host_url}/sp_get_info", json=data, headers=self.client.headers)
            if response.status_code != 200:
                raise APIError(response.json().get('error', 'Unknown error'))
            return Task(self.client, response.json()['task_id'], 'sp_get_info')
    
    def check_permissions(self, permissions):
        data = {"permissions": permissions}
        response = requests.post(f"{self.host_url}/check_permissions", json=data, headers=self.headers)
        if response.status_code != 200:
            return False
        return True
    
    def create_key(self, name, permissions, response_json=False):
        data = {"name": name, "permissions": permissions}
        response = requests.post(f"{self.host_url}/create_key", json=data, headers=self.headers)
        if response.status_code != 201:
            raise APIError(response.json().get('error', 'Unknown error'))
        if response_json: return response.json()
        return response.json()['key']

    def delete_key(self, name):
        response = requests.delete(f"{self.host_url}/delete_key/{name}", headers=self.headers)
        if response.status_code != 200:
            raise APIError(response.json().get('error', 'Unknown error'))
        return response.json()
    
    def get_key(self, name, response_json=False):
        response = requests.get(f"{self.host_url}/get_key/{name}", headers=self.headers)
        if response.status_code != 200:
            raise APIError(response.json().get('error', 'Unknown error'))
        if response_json: return response.json()
        return response.json()['key']

    def get_keys(self):
        response = requests.get(f"{self.host_url}/get_keys", headers=self.headers)
        if response.status_code != 200:
            raise APIError(response.json().get('error', 'Unknown error'))
        return response.json()
        
    class SendTask:
        def __init__(self, client):
            self.client = client
            self.YouTube = self.YouTube(client)
            self.Spotify = self.Spotify(client)

        class YouTube:
            def __init__(self, client):
                self.client = client
            
            def get_video(self, url, video_format="bestvideo", audio_format="bestaudio"):
                data = {"url": url, "video_format": video_format, "audio_format": audio_format}
                response = requests.post(f"{self.client.host_url}/yt_get_video", json=data, headers=self.client.headers)
                if response.status_code != 200:
                    raise APIError(response.json().get('error', 'Unknown error'))
                return Task(self.client, response.json()['task_id'], 'yt_get_video')
            
            def get_audio(self, url, audio_format="bestaudio"):
                data = {"url": url, "audio_format": audio_format}
                response = requests.post(f"{self.client.host_url}/yt_get_audio", json=data, headers=self.client.headers)
                if response.status_code != 200:
                    raise APIError(response.json().get('error', 'Unknown error'))
                return Task(self.client, response.json()['task_id'], 'yt_get_audio')
            
            def get_live_video(self, url, duration, start=0, video_format="bestvideo", audio_format="bestaudio"):
                data = {"url": url, "start": start, "duration": duration, "video_format": video_format, "audio_format": audio_format}
                response = requests.post(f"{self.client.host_url}/yt_get_live_video", json=data, headers=self.client.headers)
                if response.status_code != 200:
                    raise APIError(response.json().get('error', 'Unknown error'))
                return Task(self.client, response.json()['task_id'], 'yt_get_live_video')
            
            def get_live_audio(self, url, duration, start=0, audio_format="bestaudio"):
                data = {"url": url, "start": start, "duration": duration, "audio_format": audio_format}
                response = requests.post(f"{self.client.host_url}/yt_get_live_audio", json=data, headers=self.client.headers)
                if response.status_code != 200:
                    raise APIError(response.json().get('error', 'Unknown error'))
                return Task(self.client, response.json()['task_id'], 'yt_get_live_audio')

            def get_info(self, url):
                data = {"url": url}
                response = requests.post(f"{self.client.host_url}/yt_get_info", json=data, headers=self.client.headers)
                if response.status_code != 200:
                    raise APIError(response.json().get('error', 'Unknown error'))
                return Task(self.client, response.json()['task_id'], 'yt_get_info')
            
        class Spotify:
            def __init__(self, client):
                self.client = client

            def get_track(self, url):
                data = {"url": url}
                response = requests.post(f"{self.client.host_url}/sp_get_track", json=data, headers=self.client.headers)
                if response.status_code != 200:
                    raise APIError(response.json().get('error', 'Unknown error'))
                return Task(self.client, response.json()['task_id'], 'sp_get_track')
            
            def get_info(self, url):
                data = {"url": url}
                response = requests.post(f"{self.client.host_url}/sp_get_info", json=data, headers=self.client.headers)
                if response.status_code != 200:
                    raise APIError(response.json().get('error', 'Unknown error'))
                return Task(self.client, response.json()['task_id'], 'sp_get_info')
