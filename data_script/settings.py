import argparse


def get_args():
    parser = argparse.ArgumentParser(description="Scraper")
    parser.add_argument("--mode", choices=["api", "web"], default="web")
    parser.add_argument("--refresh-cache", action="store_true")
    parser.add_argument("--output-file", default="output.csv")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--cache_path", default="cache/data.json")
    return parser.parse_args()


ARGS = get_args()
