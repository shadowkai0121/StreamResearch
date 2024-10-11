from typing import List
from stream_analysis.env_ import Env_
from googleapiclient.discovery import build

import os


youtube = build('youtube', 'v3', developerKey=os.getenv('YT_API_KEY'))


def get_playlist_videos(playlist_id: str) -> List[Env_]:
    videos = []
    next_page_token = None

    while True:
        request = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response['items']:
            video_id = item['snippet']['resourceId']['videoId']
            video_url = Env_(
                video_live_url=f'https://www.youtube.com/live/{video_id}')
            videos.append(video_url)

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return videos


if __name__ == '__main__':
    playlist_id = 'PLECPddeTU9ojxLzMI7U2VybeBO_pvOIpX'

    video_links = get_playlist_videos(playlist_id)

    for link in video_links:
        print(link)
