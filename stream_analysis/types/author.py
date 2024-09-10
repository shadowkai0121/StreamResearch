from stream_analysis.utils import get_secure_dict
from stream_analysis.mixins import ColumnsToPropertyMixin, ConvertMixin

import regex as re

def seperate_author_title(author_title: str) -> tuple:
    if author_title.lower() == 'new member':
        return ('member', 0)

    match = re.match(r'(.*) \((\d+) (years*|months*)\)', author_title)

    if match:
        name = match.group(1).lower()
        number = int(match.group(2))
        period = match.group(3).lower()

        if period in ('year', 'years'):
            days = number * 365
        elif period in ('month', 'months'):
            days = number * 30

        return (name, days)
    else:
        return ('', 0)

class Author(ColumnsToPropertyMixin, ConvertMixin):
    _columns = (
        'id',
        'name',
        'title',
        'membership_duration',
        'badge',
        'image',
    )

    def __init__(self, data: dict, *args, **kwargs) -> None:
        secure_data = get_secure_dict(data)

        badges = secure_data['badges']
        title = None
        member_duration = None
        badge_url = None
        image_url = None

        if badges:
            badges = badges[0]
            title, member_duration = seperate_author_title(
                badges['title'] or '')
            try:
                badge_url = badges['icons'][0]['url']
            except KeyError:
                badge_url = ''
        else:
            # normal viewer doesnt have badges
            title = ''
            member_duration = 0

        image_url = secure_data['images'][0]['url']


        self.data = {
            'id': secure_data['id'] or '',
            'name': secure_data['name'] or '',
            'title': title,
            'membership_duration': member_duration,
            'badge': badge_url or '',
            'image': image_url or '',
        }

        super().__init__(*args, **kwargs)

    # type hints for IDE
    id: str
    name: str
    title: str
    membership_duration: int
    badge: str
    image: str
