import json
import os.path

import pandas as pd
import requests

from exceptions import MalformedData, ReferenceNotFound
from settings import ARGS
from utils import get_cache_file_path
import request_limiter

CACHE_FILE = "leaderboard"


def get_column_titles():
    col_names = ['#', 'Player', 'Player-ID', 'Time', 'Date', 'Platform', 'Verified']
    return col_names


def get_player_info(players_in_run, players_def):
    user = None
    for player in players_in_run:
        if player['rel'] == 'user':
            user = player['id']
            break

    if user is None:
        if ARGS.strict:
            raise MalformedData("Player not found in run.")
        # If we do not want to explicitly fail, we try to fix the data.
        return {'id': None, 'name': players_in_run[0]['name']}

    for player in players_def['data']:
        if 'id' in player and player['id'] == user:
            return {'id': user, 'name': player['names']['international']}
    raise ReferenceNotFound(f"Player {user} not found.")


def get_platform_name(platform_id, platforms):
    for platform in platforms['data']:
        if platform['id'] == platform_id:
            return platform['name']
    if ARGS.strict:
        raise ReferenceNotFound(f"Platform {platform_id} not found.")
    return None


def get_multi_data(runs, players, platforms, column_titles):
    data = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: []}

    for run_data in runs:
        place = run_data['place']
        run = run_data['run']
        player_info = get_player_info(run['players'], players)
        data[0].append(place)
        data[1].append(player_info['name'])
        data[2].append(player_info['id'])
        data[3].append(run['times']['primary_t'])
        data[4].append(run['date'])
        data[5].append(get_platform_name(run['system']['platform'], platforms))
        data[6].append(run['status']['status'] == 'verified')

    df = pd.DataFrame.from_dict(data)
    df.columns = column_titles
    return df


def is_cached():
    return os.path.isfile(get_cache_file_path(CACHE_FILE))


def fetch_data() -> dict:
    path = get_cache_file_path(CACHE_FILE)
    if not ARGS.refresh_cache and is_cached():
        print(f'Using cached data from {path}')
        with open(path, 'r') as f:
            return json.load(f)
    else:
        print("Fetching leaderboard-data from API.")
        response = request_limiter.get(
            f'https://www.speedrun.com/api/v1/leaderboards/{ARGS.game_key}/category/{ARGS.game_category}?embed=players,platforms')
        json_doc = json.loads(response.text)
        print(f'Writing to cache {path}.')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            json.dump(json_doc, f)
        return json_doc


def main():
    json_doc = fetch_data()
    runs = json_doc['data']['runs']
    players = json_doc['data']['players']
    platforms = json_doc['data']['platforms']
    col_names = get_column_titles()

    return {'name': 'leaderboard', 'data': get_multi_data(runs, players, platforms, col_names)}
