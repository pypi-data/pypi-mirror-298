import os

import get_cosmopower_emus


def get_cosmopower_path():
    get_cosmopower_emus.set()
    return os.getenv('PATH_TO_COSMOPOWER_ORGANIZATION')

path_to_cosmopower_organization = get_cosmopower_path()
