import os
import asyncio

import requests

from .api import api


async def download(key, url):
    if url.startswith('alias:'):
        return

    _, ext = url.rsplit('.', 1)
    dirname = 'data'
    os.makedirs(dirname, exist_ok=True)
    path = os.path.join(dirname, f'{key}.{ext}')

    if not os.path.exists(path):
        resp = requests.get(url)
        with open(path, 'wb') as f:
            f.write(resp.content)


async def emoji_download():
    resp = api('emoji.list')
    emoji_data = resp.body
    for k, v in emoji_data['emoji'].items():
        print(f'{k=}', f'{v=}')
        await download(k, v)


async def main():
    await asyncio.create_task(emoji_download())


if __name__ == '__main__':
    asyncio.run(main())
