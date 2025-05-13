import argparse


def get_args():
    parser = argparse.ArgumentParser(description="Scraper")
    parser.add_argument("--mode", choices=["api", "web"], default="api")
    parser.add_argument("--refresh-cache", action="store_true")
    parser.add_argument("--output-dir", default="output/")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--cache-dir", default="cache/")
    parser.add_argument("--print", action="store_true")
    parser.add_argument("--game-key", default="o1y9wo6q")
    parser.add_argument("--game-category", default="wkpoo02r")
    return parser.parse_args()


ARGS = get_args()
