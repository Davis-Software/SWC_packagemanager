import requests
from tqdm import tqdm


def wget_func(url, filename):
    resp = requests.get(url, stream=True)
    total = int(resp.headers.get('content-length', 0))
    file = open(filename, 'wb')
    with tqdm(desc=filename, total=total, unit='iB', unit_scale=True, unit_divisor=1024) as bar:
        for data in resp.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)
    file.close()
