import os.path

from pandas import DataFrame

import api_scrape as api_scrape
import web_scrape
from settings import ARGS

if __name__ == '__main__':
    result: list
    if ARGS.mode == 'api':
        result = api_scrape.main()
    else:
        result = web_scrape.main()

    if ARGS.print:
        for r in result:
            print(f'{r["name"]}:')
            print(r["data"])

    os.makedirs(os.path.dirname(ARGS.output_dir), exist_ok=True)
    for r in result:
        DataFrame.to_csv(r["data"], f'{ARGS.output_dir}/{r["name"]}.csv')
