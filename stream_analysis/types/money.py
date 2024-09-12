from datetime import datetime
from time import time

import requests
from stream_analysis.env_ import Env_
from stream_analysis.mixins import ColumnsToPropertyMixin, ConvertMixin
from stream_analysis.utils import get_secure_dict

currency_alias: dict = {
    '₫': 'vnd',
}


class Conversion:
    _instance: 'Conversion' = None
    _exchange: dict = {}
    _env: Env_ = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, _env: Env_):
        self._env = _env
        stream_time = self.get_date_string(
            self._env.video_start_time or time())

        if stream_time not in self._exchange:
            url = f'https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@{stream_time}/v1/currencies/usd.json'

            response = requests.get(url)

            response.raise_for_status()
            self._exchange[stream_time] = response.json().get('usd')

    def exchange_to_usd(self, amount: float, currency: str, _env: Env_ = None) -> float:
        env = self._env
        if isinstance(_env, Env_):
            env = _env

        stream_time = self.get_date_string(env.video_start_time)

        currency = currency.lower()
        if currency in currency_alias:
            currency = currency_alias[currency]

        exchange_rate = self._exchange[stream_time][currency]
        return amount / exchange_rate

    def get_date_string(self, timestamp: int) -> str:
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')


class Money(ColumnsToPropertyMixin, ConvertMixin):
    _columns = (
        'std_amount',  # exchange to USD
        'amount',
        'currency',
        'currency_symbol',
        'text',
    )

    def __init__(self, data: dict, _env: Env_, *args, **kwargs):
        secure_data = get_secure_dict(data)
        std_amount = secure_data['amount'] or 0

        if secure_data['currency'].lower() != 'usd':
            conv = Conversion(_env)
            std_amount = conv.exchange_to_usd(
                secure_data['amount'], secure_data['currency'])

        self.data = {
            'std_amount': std_amount,
            'amount': secure_data['amount'] or 0,
            'currency': secure_data['currency'] or '',
            'currency_symbol': secure_data['currency_symbol'] or '',
            'text': secure_data['text'] or '',
        }

        super().__init__(*args, **kwargs)

    std_amount: float
    amount: float
    currency: str
    currency_symbol: str
    text: str


if __name__ == "__main__":
    from pprint import pprint

    test_data = {
        "amount": 200.0,
        "currency": "JPY",
        "currency_symbol": "¥",
        "text": "¥200",
    }

    env = Env_(
        video_live_url='https://www.youtube.com/live/eP29jR49UDs?si=hzi_2Z4VwT47rmVm')

    conv = Conversion(env)
    # pprint(conv.exchange_to_usd(test_data['amount'], test_data['currency']))

    money_instance = Money(test_data, env)
    pprint(money_instance.to_dict())
