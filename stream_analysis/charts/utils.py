from matplotlib.artist import Artist
from stream_analysis.chat import Chat


def wrap_hours_line(chart: Artist, chat: Chat) -> Artist:
    chart.vlines(
        chat._env.hourse_labels[1],
        ymin=0,
        ymax=chat.df_per_min['messages'].max(),
        colors='red',
        linestyles='-')
    return chart
