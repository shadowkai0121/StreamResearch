
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from stream_analysis.chat import Chat
from stream_analysis.env_ import Env_
import seaborn as sns


class ActivityPerMin:
    _chat: Chat
    _env: Env_
    _fig: Figure
    _axes: Axes
    _x_max: int
    _y_min: int = 10
    _fig_amount: int = 4

    def __init__(self, chat: Chat, _env: Env_, *args, **kwargs) -> None:
        self._chat = chat
        self._env = _env

        self.generate(*args, **kwargs)

    def generate(self, *args, **kwargs) -> Figure:
        self._fig, self._axes = plt.subplots(
            self._fig_amount, 1, figsize=kwargs.get('figsize') or (20, 15),
            sharex=True,
            gridspec_kw={'height_ratios': kwargs.get('height_ratios') or (6, 3, 3, 3)})

        self._x_max = self._env.time_labels[1][-1]

        for idx in range(len(self._axes)):
            self._axes[idx].set_xlim(0, self._x_max)
            self._axes[idx].grid(True)

        for attr_name in dir(self):
            if attr_name.startswith('_generate_'):
                generate_chart = getattr(self, attr_name)
                if callable(generate_chart):
                    generate_chart()

        return self._fig

    @property
    def fig(self) -> Figure:
        return self._fig

    def _generate_messages(self) -> None:
        palette = sns.color_palette('magma', n_colors=3)

        self._axes[0].fill_between(
            self._chat.df_per_min['time_in_minutes'],
            0,
            self._chat.df_per_min['messages'],
            label='messages',
            color=palette[2],
            step='mid')

        self._axes[0].fill_between(
            self._chat.df_per_min['time_in_minutes'],
            0,
            self._chat.df_per_min['message_without_emotes'],
            label='message_without_emotes',
            color=palette[1],
            step='mid')

        self._axes[0].fill_between(
            self._chat.df_per_min['time_in_minutes'],
            0,
            self._chat.df_per_min['cleaned_messages'],
            label='cleaned_messages',
            color=palette[0],
            step='mid')

        self._axes[0].vlines(
            self._env.time_labels[1][1:],
            ymin=0,
            ymax=self._chat.df_per_min['messages'].max(),
            colors='red',
            linestyles='--')

        self._axes[0].set_ylim(bottom=0)
        self._axes[0].legend()
        self._axes[0].set_ylabel('Message Count')
        self._axes[0].set_title('Amount of Messages Per Minute')

    def _generate_active_users(self) -> None:
        self._axes[1].step(
            self._chat.df_active_users_per_min['time_in_minutes'],
            self._chat.df_active_users_per_min['active_users'],
            label='Membership Duration avg.',
            color='blue',
            where='mid')

        self._axes[1].vlines(
            self._env.time_labels[1][1:],
            ymin=0,
            ymax=self._chat.df_active_users_per_min['active_users'].max(),
            colors='red',
            linestyles='--')

        self._axes[1].set_ylim(
            self._chat.df_active_users_per_min['active_users'].min() - self._y_min if self._chat.df_active_users_per_min['active_users'].min() > self._y_min else 0)

        self._axes[1].set_ylabel('Active users')
        self._axes[1].set_title('Active users Per Minute')

    def _generate_membership_duration(self) -> None:
        self._axes[2].step(
            self._chat.df_membership_duration_avg_per_min['time_in_minutes'],
            self._chat.df_membership_duration_avg_per_min['membership_duration_avg'],
            label='Membership Duration avg.',
            color='blue',
            where='mid')

        self._axes[2].vlines(
            self._env.time_labels[1][1:],
            ymin=0,
            ymax=self._chat.df_membership_duration_avg_per_min['membership_duration_avg'].max(),
            colors='red',
            linestyles='--')

        self._axes[2].set_ylim(
            self._chat.df_membership_duration_avg_per_min['membership_duration_avg'].min() - self._y_min if self._chat.df_membership_duration_avg_per_min['membership_duration_avg'].min() > self._y_min else 0)

        self._axes[2].set_ylabel('Duration avg.(min)')
        self._axes[2].set_title('Membership Duration avg. Per Minute')

    def _generate_money(self) -> None:
        self._axes[3].step(
            self._chat.df_money_sum_per_min['time_in_minutes'],
            self._chat.df_money_sum_per_min['money_sum'],
            label='Money Per Minute',
            color='blue',
            where='mid')
        
        self._axes[3].vlines(
            self._env.time_labels[1][1:],
            ymin=0,
            ymax=self._chat.df_money_sum_per_min['money_sum'].max(),
            colors='red',
            linestyles='--')

        self._axes[3].set_ylabel('Money (USD)')
        self._axes[3].set_title('Money Per Minute')

        self._axes[3].set_ylim(bottom=0)

        self._axes[3].set_xlabel('Time (HH:MM)')
        self._axes[3].set_xticks(self._env.time_labels[1])
        self._axes[3].set_xticklabels(self._env.time_labels[0], rotation=45)
