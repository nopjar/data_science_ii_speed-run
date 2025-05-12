import json
import os.path

import pandas as pd
import requests
from settings import ARGS

GAME_KEY = "o1y9wo6q"
CATEGORY_KEY = "wkpoo02r"


class MalformedData(Exception):
    pass


class ReferenceNotFound(Exception):
    pass


def get_column_titles():
    col_names = ['#', 'Player', 'Time', 'Date', 'Platform', 'Verified']
    return col_names


def get_player_name(players_in_run, players_def):
    user = None
    for player in players_in_run:
        if player['rel'] == 'user':
            user = player['id']
            break

    if user is None:
        if ARGS.strict:
            raise MalformedData("Player not found in run.")
        # If we do not want to explicitly fail, we try to fix the data.
        return players_in_run[0]['name']

    for player in players_def['data']:
        if 'id' in player and player['id'] == user:
            return player['names']['international']
    raise ReferenceNotFound(f"Player {user} not found.")


def get_platform_name(platform_id, platforms):
    for platform in platforms['data']:
        if platform['id'] == platform_id:
            return platform['name']
    raise ReferenceNotFound(f"Platform {platform_id} not found.")


def get_multi_data(runs, players, platforms, column_titles):
    data = {0: [], 1: [], 2: [], 3: [], 4: [], 5: []}

    for run_data in runs:
        place = run_data['place']
        run = run_data['run']
        data[0].append(place)
        data[1].append(get_player_name(run['players'], players))
        data[2].append(run['times']['primary_t'])
        data[3].append(run['date'])
        data[4].append(get_platform_name(run['system']['platform'], platforms))
        data[5].append(run['status']['status'] == 'verified')

    df = pd.DataFrame.from_dict(data)
    df.columns = column_titles
    return df


def is_cached():
    return os.path.isfile(ARGS.cache_path)


def fetch_data() -> dict:
    if not ARGS.refresh_cache and is_cached():
        print("Using cached data.")
        with open(ARGS.cache_path, 'r') as f:
            return json.load(f)
    else:
        print("Fetching data from API.")
        response = requests.get(
            f'https://www.speedrun.com/api/v1/leaderboards/{GAME_KEY}/category/{CATEGORY_KEY}?embed=players,platforms')
        json_doc = json.loads(response.text)
        print("Writing to cache.")
        os.makedirs(os.path.dirname(ARGS.cache_path), exist_ok=True)
        with open(ARGS.cache_path, 'w') as f:
            json.dump(json_doc, f)
        return json_doc


def main():
    json_doc = fetch_data()
    runs = json_doc['data']['runs']
    players = json_doc['data']['players']
    platforms = json_doc['data']['platforms']
    col_names = get_column_titles()

    return get_multi_data(runs, players, platforms, col_names)
