import os
import zipfile
import requests
from tqdm import tqdm


def wget_func(url, filename):
    resp = requests.get(url, stream=True)
    total = int(resp.headers.get('content-length', 0))
    file = open(filename, 'wb')
    with tqdm(desc=filename.split("/")[-1], total=total, unit='iB', unit_scale=True, unit_divisor=1024) as bar:
        for data in resp.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)
    file.close()


def extract_archive(archive, target_dir):
    with zipfile.ZipFile(archive, "r") as zf:
        filecount = len(zf.filelist)
        with tqdm(desc=archive.split("/")[-1], total=filecount) as bar:
            for file in zf.filelist:
                bar.update(1)
                bar.set_description_str(file.filename)
                zf.extract(file.filename, target_dir)
