import argparse


def get_args():
    parser = argparse.ArgumentParser(description="Scraper")
    parser.add_argument("--refresh-cache", action="store_true")
    parser.add_argument("--output-dir", default="output/")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--cache-dir", default="cache/")
    parser.add_argument("--print", action="store_true")
    parser.add_argument("--limit", type=int, default=20)

    # Create subparsers
    subparsers = parser.add_subparsers(dest="command")

    leaderboard_parser = subparsers.add_parser("leaderboard")
    leaderboard_parser.add_argument("--game-key", default="o1y9wo6q")
    leaderboard_parser.add_argument("--game-category", default="wkpoo02r")

    genres_parser = subparsers.add_parser("genres")
    genres_parser.add_argument("--genre-key", default="jp23ox26")

    game_info_parser = subparsers.add_parser("game_info")
    game_info_parser.add_argument("--game-key", default="o1y9wo6q")

    subparsers.add_parser("clear")
    return parser.parse_args()


ARGS = get_args()
