import shutil

from settings import ARGS


def main():
    shutil.rmtree(ARGS.cache_dir, ignore_errors=True)
    print(f'Cache directory {ARGS.cache_dir} cleared')