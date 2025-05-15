import json

import request_limiter
from settings import ARGS


def fetch_game_info():
    response = request_limiter.get(f'https://www.speedrun.com/api/v1/games/{ARGS.game_key}?embed=genres')
    # TODO: fetch from/write to cache
    json_doc = json.loads(response.text)
    return json_doc

def fetch_categories():
    response = request_limiter.get(f'https://www.speedrun.com/api/v1/games/{ARGS.game_key}/categories')
    # TODO: fetch from/write to cache
    json_doc = json.loads(response.text)
    return json_doc


def print_info(json_doc, categories):
    print(f'Name: {json_doc['names']['international']}')
    print('Genres:')
    for genre in json_doc['genres']['data']:
        print(f'  {genre["name"]}: {genre['id']}')
    print('Categories:')
    for category in categories:
        print(f'  {category["name"]}: {category["id"]}')

def main():
    game_info = fetch_game_info()
    categories = fetch_categories()
    print_info(game_info['data'], categories['data'])
