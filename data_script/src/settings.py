import argparse


def get_args():
    parser = argparse.ArgumentParser(description="Scraper")
    parser.add_argument("--mode", choices=["api", "web"], default="api")
    parser.add_argument("--refresh-cache", action="store_true")
    parser.add_argument("--output-file", default="output/output.csv")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--cache_path", default="cache/data.json")
    parser.add_argument("--print", action="store_true")
    return parser.parse_args()


ARGS = get_args()
