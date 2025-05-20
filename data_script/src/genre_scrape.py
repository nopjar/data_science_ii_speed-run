import json
import os.path

import pandas as pd

import request_limiter
import utils
from exceptions import MalformedData
from settings import ARGS


def get_column_titles():
    return ['id', 'name', 'released', 'first_speedrun_date', 'first_speedrun_time', 'top_run_date', 'top_run_time']


def fetch_genre():
    path = utils.get_cache_file_path(f"genres/{ARGS.genre_key}-{ARGS.limit}")
    if utils.is_cached(path):
        print(f'Using cached data from {path}')
        with open(path, 'r') as f:
            return json.load(f)
    else:
        print(f'limit: {ARGS.limit}')
        response = request_limiter.get(
            f'https://www.speedrun.com/api/v1/games?genre={ARGS.genre_key}&max={min(200, ARGS.limit)}')
        json_doc = json.loads(response.text)
        print(f'Writing to cachefile {path}')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            json.dump(json_doc, f)
        return json_doc


def fetch_top_runs(ids):
    dic = {}
    for game_id, category in ids.items():
        path = utils.get_cache_file_path(f"genres/games/{game_id}-top-run")
        if utils.is_cached(path):
            print(f'Using cached data from {path}')
            with open(path, 'r') as f:
                dic[game_id] = json.load(f)
        else:
            print('Fetching top-run data from API.')
            response = request_limiter.get(
                f'https://www.speedrun.com/api/v1/leaderboards/{game_id}/category/{category}?limit=1')
            json_doc = json.loads(response.text)
            print(f'Writing to cachefile {path}')
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w') as f:
                json.dump(json_doc, f)
            dic[game_id] = json_doc
    return dic


def filter_first_run_date(json_doc):
    for data in json_doc['data']:
        if data['date'] is not None:
            return data
    if ARGS.strict:
        raise MalformedData("No first run found.")
    return {'date': None, 'times': {'primary_t': None}}


def fetch_first_runs(ids):
    dic = {}
    for game_id, category in ids.items():
        path = utils.get_cache_file_path(f"genres/games/{game_id}-first-run")
        if utils.is_cached(path):
            print(f'Using cached data from {path}')
            with open(path, 'r') as f:
                dic[game_id] = json.load(f)
        else:
            print('Fetching first-run data from API.')
            response = request_limiter.get(
                f'https://www.speedrun.com/api/v1/runs?game={game_id}&category={category}&orderby=date&direction=asc&max=200')
            json_doc = json.loads(response.text)
            json_doc['data'] = [filter_first_run_date(json_doc)]
            print(f'Writing to cachefile {path}')
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w') as f:
                json.dump(json_doc, f)
            dic[game_id] = json_doc
    return dic


def get_multi_data(json_docs, top_runs, first_runs, column_titles):
    data = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: []}

    for game in json_docs['data']:
        print(f'Processing {game["id"]}')
        if (game['id'] in top_runs and 'status' in top_runs[game['id']]) or (
                game['id'] in first_runs and 'status' in first_runs[game['id']]):
            if ARGS.strict:
                raise MalformedData(f"Missing data for {game['id']}")
            print(f'Skipping {game["id"]} due to missing data.')
            continue

        data[0].append(game['id'])
        data[1].append(game['names']['international'])
        data[2].append(game['release-date'])
        if game['id'] not in first_runs:
            if ARGS.strict:
                raise MalformedData(f"Missing data for {game['id']}")
            data[3].append(None)
            data[4].append(None)
        else:
            data[3].append(first_runs[game['id']]['data'][0]['date'])
            data[4].append(first_runs[game['id']]['data'][0]['times']['primary_t'])
        if game['id'] not in top_runs or len(top_runs[game['id']]['data']['runs']) == 0:
            if ARGS.strict:
                raise MalformedData(f"Missing data for {game['id']}")
            data[5].append(None)
            data[6].append(None)
        else:
            data[5].append(top_runs[game['id']]['data']['runs'][0]['run']['date'])
            data[6].append(top_runs[game['id']]['data']['runs'][0]['run']['times']['primary_t'])

    df = pd.DataFrame.from_dict(data)
    df.columns = column_titles
    return [{'name': f'genre-{ARGS.genre_key}', 'data': df}]


def extract_game_and_category_id(json_docs):
    data = {}
    for game in json_docs['data']:
        category = None
        for link in game['links']:
            if link['rel'] == 'leaderboard':
                category = link['uri'].split('/')[-1]
                break

        if category is None:
            if ARGS.strict:
                raise MalformedData(f"No category found for {game['id']}")
            continue
        data[game['id']] = category
    return data


def main():
    json_docs = fetch_genre()
    column_titles = get_column_titles()
    ids = extract_game_and_category_id(json_docs)
    top_runs = fetch_top_runs(ids)
    first_runs = fetch_first_runs(ids)

    return get_multi_data(json_docs, top_runs, first_runs, column_titles)
