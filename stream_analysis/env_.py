from dataclasses import dataclass
from functools import cached_property
from math import ceil
from chat_downloader.sites import YouTubeChatDownloader
from stream_analysis.utils import convert_none, minutes_to_hhmm
import os
import shutil
import regex as re


@dataclass
class Env_:
    video_live_url: str

    debug: bool = bool(convert_none(os.getenv('DEBUG')))
    has_summary: bool = bool(convert_none(os.getenv('HAS_SUMMARY')))
    cleaned_list_path: str = convert_none(os.getenv('CLEANED_LIST_PATH'))
    chat_request_timeout: int | None = convert_none(
        os.getenv('CHAT_REQUEST_TIMEOUT'), int)

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
    def video_start_time(self) -> int:
        timestamp = int(self.video_data.get('start_time', 0))
        if timestamp > 0:
            timestamp = timestamp / 1000000  # YT data is microsecs

        return timestamp

    @cached_property
    def video_end_time(self) -> int:
        timestamp = int(self.video_data.get('end_time', 0))
        if timestamp > 0:
            timestamp = timestamp / 1000000  # YT data is microsecs

        return timestamp

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
    def chat_per_min_csv_path(self) -> str:
        return os.path.join(self.data_path, 'chat_per_min.csv')

    @cached_property
    def chat_timeline_path(self) -> str:
        return os.path.join(self.data_path, 'timeline.png')

    @cached_property
    def chat_wordcloud_path(self) -> str:
        return os.path.join(self.data_path, 'wordcloud.png')

    @cached_property
    def cleaned_words(self) -> tuple:
        with open(self.cleaned_list_path, 'r', encoding='utf8') as f:
            cleaned_words = [word.strip() for word in f.readlines()]
        return cleaned_words

    @cached_property
    def time_labels(self) -> tuple:
        interval = convert_none(os.getenv('PLOT_TIME_INTERVAL'), int) or 10
        interval_by_sec = 60 * interval
        duration = self.video_data.get('duration', 0)
        time_labels = []
        time_values = []

        interval_amount = duration // interval_by_sec + 1

        for i in range(int(interval_amount) + 1):
            time_labels.append(minutes_to_hhmm(i * interval))
            time_values.append(i * interval)

        minutes = ceil(duration / 60)
        time_labels.append(minutes_to_hhmm(minutes))
        time_values.append(minutes)

        return time_labels, time_values

    def __post_init__(self) -> None:
        self.video_live_url = self.video_live_url.split(
            '?')[0] if '?' in self.video_live_url else self.video_live_url

        self.init_env()

    def init_env(self) -> None:
        if not self.debug:
            if os.path.exists(self.data_path):
                shutil.rmtree(self.data_path)

        if not os.path.exists(self.data_path):
            os.mkdir(self.data_path)

    @staticmethod
    def remove_illegal_path_characters(path) -> str:
        illegal_characters = r'[<>:"/\\|?*\x00-\x1F]'
        cleaned_path = re.sub(illegal_characters, '', path).strip()
        return cleaned_path


if __name__ == '__main__':
    env_ = Env_(video_live_url='Http://example.com?si=dafds')
    print(env_.chat_request_timeout)
    print(type(env_.chat_request_timeout))
