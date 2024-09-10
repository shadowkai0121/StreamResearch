from dataclasses import dataclass
from functools import cached_property
from chat_downloader.sites import YouTubeChatDownloader
import os
import shutil
import regex as re


@dataclass
class Env_:
    video_live_url: str

    debug: bool = os.getenv('DEBUG')
    has_summary: bool = os.getenv('HAS_SUMMARY')
    cleaned_list_path: str = os.getenv('CLEANED_LIST_PATH')

    @cached_property
    def video_id(self) -> str:
        return self.video_live_url.split('/')[-1].strip() or ''

    @cached_property
    def video_watching_url(self) -> str:
        pattern = r'https?://(?:www\.)?([^/?#]+)'
        match = re.search(pattern, self.video_live_url, re.IGNORECASE)
        if match:
            return f'https://' + match.group(1)
        else:
            return ''

    @cached_property
    def video_data(self) -> dict:
        downloader = YouTubeChatDownloader()
        video_data = downloader.get_video_data(self.video_id)
        return video_data

    @cached_property
    def video_title(self) -> str:
        return self.video_data.get('title', self.video_id) or 'default'

    @cached_property
    def data_path(self) -> str:
        return os.path.join(os.getenv('DATA_PATH'), Env_.remove_illegal_path_characters(self.video_title))

    @cached_property
    def video_liver(self) -> str:
        return self.video_data.get('author', '')

    @cached_property
    def video_data_path(self) -> str:
        return os.path.join(self.data_path, 'info.json')

    @cached_property
    def chat_json_path(self) -> str:
        return os.path.join(self.data_path, 'chat.json')

    @cached_property
    def chat_csv_path(self) -> str:
        return os.path.join(self.data_path, 'chat.csv')

    @cached_property
    def chat_timeline_path(self) -> str:
        return os.path.join(self.data_path, 'timeline.png')

    @cached_property
    def chat_wordcloud_path(self) -> str:
        return os.path.join(self.data_path, 'wordcloud.png')

    def __post_init__(self) -> None:
        self.video_live_url = self.video_live_url.split(
            '?')[0] if '?' in self.video_live_url else self.video_live_url

        self.init_env()

    def init_env(self) -> None:
        if os.path.exists(self.data_path):
            shutil.rmtree(self.data_path)
        os.mkdir(self.data_path)

    @staticmethod
    def remove_illegal_path_characters(path) -> str:
        illegal_characters = r'[<>:"/\\|?*\x00-\x1F]'
        cleaned_path = re.sub(illegal_characters, '', path)
        return cleaned_path.strip()


if __name__ == '__main__':
    env_ = Env_(video_live_url='Http://example.com?si=dafds')
    print(env_.cleaned_list_path)
