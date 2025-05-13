from settings import ARGS


def get_cache_file_path(file_name):
    if ARGS.cache_dir.endswith('/'):
        return f'{ARGS.cache_dir}{file_name}.json'
    else:
        return f'{ARGS.cache_dir}/{file_name}.json'
