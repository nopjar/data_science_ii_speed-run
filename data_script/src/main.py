import os.path

from pandas import DataFrame

import genre_scrape
import leaderboard_scrape
from settings import ARGS

if __name__ == '__main__':
    result: list
    if ARGS.command == 'leaderboard':
        result = leaderboard_scrape.main()
    elif ARGS.command == 'genres':
        result = genre_scrape.main()
    else:
        print(f'Unknown command {ARGS.command}')
        exit(1)

    if ARGS.print:
        for r in result:
            print(f'{r["name"]}:')
            print(r["data"])

    for r in result:
        path = f'{ARGS.output_dir}/{r["name"]}.csv'
        os.makedirs(os.path.dirname(ARGS.output_dir), exist_ok=True)
        DataFrame.to_csv(r["data"], path)
