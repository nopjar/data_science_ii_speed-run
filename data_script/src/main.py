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

    if ARGS.print:
        print(df)

    os.makedirs(os.path.dirname(ARGS.output_file), exist_ok=True)
    DataFrame.to_csv(df, ARGS.output_file)
