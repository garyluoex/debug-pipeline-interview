import os
import shutil
import urllib.request as request

from contextlib import closing


def download_url_data(url, output_path):

    parent_directory = os.path.dirname(output_path)

    with closing(request.urlopen(url)) as r:
        with open(output_path, "wb+") as f:
            shutil.copyfileobj(r, f)

    return output_path


def create_target_directory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
