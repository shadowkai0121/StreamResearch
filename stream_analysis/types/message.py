from chat_downloader.sites.common import Chat

from stream_analysis.env_ import Env_
from stream_analysis.types.money import Money
from stream_analysis.utils import get_secure_dict, strip_symbols, clean_string
from stream_analysis.mixins import ColumnsToPropertyMixin, ConvertMixin
from stream_analysis.types.author import Author

import regex as re


class Message(ColumnsToPropertyMixin, ConvertMixin):
    _columns = (
        'author_id',
        'author_name',
        'author_title',
        'author_membership_duration',
        'author_badge',
        'author_image',
        'message',
        'message_without_emotes',
        'cleaned_message',
        'message_type',
        'money',  # USD
        'time_in_seconds',
        'timestamp',
    )

    def __init__(self, data: Chat, env_: Env_, *args, **kwargs) -> None:
        secure_data = get_secure_dict(data)

        author = Author(secure_data['author'] or {})

        self.data = {
            'author_id': author.id,
            'author_name': author.name,
            'author_title': author.title,
            'author_membership_duration': author.membership_duration,
            'author_badge': author.badge,
            'author_image': author.image,
            'message': secure_data['message'] or '',
            'message_without_emotes': '',
            'cleaned_message': '',
            'message_type': secure_data['message_type'] or '',
            'money': 0,
            'time_in_seconds': secure_data['time_in_seconds'],
            'timestamp': secure_data['timestamp'],
        }
        
        if secure_data['money']:
            money = Money(secure_data['money'], env_)
            self.data['money'] = money.std_amount

        if len(self.message):
            if secure_data['emotes']:
                emote_names = [emote['name'] for emote in data['emotes']]
                self.data['message_without_emotes'] = re.sub(
                    '|'.join(re.escape(emote) for emote in emote_names),
                    '',
                    self.message,
                    flags=re.IGNORECASE)

                self.data['message_without_emotes'] = strip_symbols(
                    self.data['message_without_emotes']) or ''
            else:
                self.data['message_without_emotes'] = self.message

            # clean message
            self.data['cleaned_message'] = clean_string(
                self.message, env_.cleaned_words) or ''

        super().__init__(*args, **kwargs)

    # type hints for IDE
    author_id: str
    author_name: str
    author_title: str
    author_membership_duration: int
    author_badge: str
    author_image: str
    message: str
    message_without_emotes: str
    cleaned_message: str
    message_type: str
    money: float
    time_in_seconds: int
    timestamp: int
