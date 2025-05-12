import argparse
import os.path

from pandas import DataFrame

import api_scrape
import web_scrape
from settings import ARGS

if __name__ == '__main__':
    df = None
    if ARGS.mode == 'api':
        df = api_scrape.main()
    else:
        df = web_scrape.main()

    if os.path.isdir('output') is False:
        os.mkdir('output')
    DataFrame.to_csv(df, f'output/{ARGS.output_file}')
