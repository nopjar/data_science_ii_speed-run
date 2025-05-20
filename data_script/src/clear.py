import shutil

from settings import ARGS


def main():
    shutil.rmtree(ARGS.cache_dir, ignore_errors=True)
    shutil.rmtree(ARGS.output_dir, ignore_errors=True)
    print(f'Cache directory {ARGS.cache_dir} and output directory {ARGS.output_dir} cleared.')