import json
import os.path

import pandas as pd

from exceptions import MalformedData
from settings import ARGS
from utils import get_cache_file_path
import request_limiter


def get_column_titles():
    col_names = ['Time', 'Date', 'Platform', 'Verified']
    return col_names


def get_platform(data):
    if 'name' in data:
        return data['name']
    elif ARGS.strict:
        raise MalformedData("Platform not found in run.")
    return None

def get_data(user_id, user, column_titles):
    data = {0: [], 1: [], 2: [], 3: []}

    for run in user['data']:
        data[0].append(run['times']['primary_t'])
        data[1].append(run['date'])
        data[2].append(get_platform(run['platform']['data']))
        data[3].append(run['status']['status'] == 'verified')

    df = pd.DataFrame.from_dict(data)
    df.columns = column_titles
    return {'name': user_id, 'data': df}


def get_multi_data(users, column_titles):
    dfs = []
    for name, user in users.items():
        dfs.append(get_data(name, user, column_titles))
    return dfs


def is_cached(user_id):
    return os.path.isfile(get_cache_file_path(user_id))


def fetch_data(user_id) -> dict:
    path = get_cache_file_path(user_id)
    if not ARGS.refresh_cache and is_cached(user_id):
        print(f'Using cached data from {path}')
        with open(path, 'r') as f:
            return json.load(f)
    else:
        print(f'Fetching player data for {user_id} from API.')
        response = request_limiter.get(
            f'https://www.speedrun.com/api/v1/runs?game={ARGS.game_key}&user={user_id}&category={ARGS.game_category}&embed=players,platform&max=200')
        json_doc = json.loads(response.text)
        print(f'Writing to cachefile {path}')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            json.dump(json_doc, f)
        return json_doc


def fetch_all(user_ids):
    dfs = {}
    for user_id in user_ids:
        dfs[user_id] = fetch_data(user_id)
    return dfs


def main(user_ids):
    json_docs = fetch_all(user_ids)
    column_title = get_column_titles()

    return get_multi_data(json_docs, column_title)
