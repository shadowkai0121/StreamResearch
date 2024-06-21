import json
import pandas as pd

def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            out[name[:-1]] = json.dumps(x)  # Convert lists and dicts to JSON string
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

with open('chat.json', 'r') as f:
    json_data = json.load(f)

flattened_data = [flatten_json(item) for item in json_data]

df = pd.DataFrame(flattened_data)

df.to_csv('chart.csv', index=False)

df.head()