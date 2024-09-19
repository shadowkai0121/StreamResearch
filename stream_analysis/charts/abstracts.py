
from abc import ABC, abstractmethod
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from stream_analysis.chat import Chat
from stream_analysis.env_ import Env_


class AbstractChart(ABC):
    _chat: Chat
    _env: Env_
    _fig: Figure
    _axes: Axes
    _x_max: int
    _y_min: int = 10
    _fig_amount: int = 4

    @property
    def fig(self) -> Figure:
        return self._fig

    def __init__(self, chat: Chat, _env: Env_, *args, **kwargs) -> None:
        self._chat = chat
        self._env = _env

        self._fig = self.generate(*args, **kwargs)

        for attr_name in dir(self):
            if attr_name.startswith('_generate_'):
                generate_chart = getattr(self, attr_name)
                if callable(generate_chart):
                    generate_chart()

    @abstractmethod
    def generate(self):
        pass
