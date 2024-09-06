import json
import pandas as pd
import re


def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            # Convert lists and dicts to JSON string
            out[name[:-1]] = json.dumps(x)
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

def title_convert_to_array(title_string):
    match = re.match(r'(.*) \((\d+) (year|years|month|months)\)', title_string)
    
    if match:
        name = match.group(1)
        number = int(match.group(2))
        period = match.group(3)

        if period in ('year', 'years'):
            days = number * 365
        elif period in ('month', 'months'):
            days = number * 30

        return (name, days)
    else:
        return ('', 0)


with open('chat.json', 'r') as f:
    json_data = json.load(f)

formatted_data = {
    'action_type': [],
    'author_name': [],
    'author_title': [],
    'author_member_duration': [],
    'message': [],
    'message_type': [],
    'time_in_seconds': [],
    'timestamp': []
}
for data in json_data:
    formatted_data['action_type'].append(data['action_type'])
    formatted_data['author_name'].append(data['author']['name'])
    try:
        title, member_duration = title_convert_to_array(data['author']['badges'][0]['title'])
    except Exception as e:
        title = ''
        member_duration = 0
    formatted_data['author_title'].append(title)
    formatted_data['author_member_duration'].append(member_duration)
    formatted_data['message'].append(data['message'])
    formatted_data['message_type'].append(data['message_type'])
    formatted_data['time_in_seconds'].append(data['time_in_seconds'])
    formatted_data['timestamp'].append(data['timestamp'])
# flattened_data = [flatten_json(item) for item in json_data]

df = pd.DataFrame(formatted_data)
df = df.loc[df['time_in_seconds'] >= 0] # remove message before live

df.to_csv('chat.csv', index=False)
print(df.head(), flush=True)
print(df[['author_member_duration']].describe(), flush=True)

df['time_in_minutes'] = (df['time_in_seconds'] // 60).astype(int)

total_messages_per_minute = df.groupby('time_in_minutes').size().reset_index(name='message_count')

member_messages_per_minute = df[df['author_title'] == 'Member'].groupby('time_in_minutes').size().reset_index(name='message_count')

moving_average = total_messages_per_minute.copy(True)
moving_average['message_count'] = total_messages_per_minute['message_count'].rolling(window=10).mean()
moving_average['message_count'] = moving_average['message_count'].fillna(total_messages_per_minute['message_count'].mean())

mean_member_duration = df.groupby('time_in_minutes').mean('author_member_duration')[['author_member_duration']]

df_per_minute = pd.DataFrame({
    'minute': total_messages_per_minute['time_in_minutes'],
    'total': total_messages_per_minute['message_count'],
    'member': member_messages_per_minute['message_count'],
    'mean_member_duration': mean_member_duration['author_member_duration'],
    'mv10': moving_average['message_count']
})
df_per_minute.to_csv('chat_per_minute.csv')

print(df_per_minute.head(), flush=True)
print(df_per_minute[['total', 'member', 'mean_member_duration']].describe(), flush=True)