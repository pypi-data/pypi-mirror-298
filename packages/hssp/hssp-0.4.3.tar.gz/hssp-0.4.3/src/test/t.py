import asyncio
import random
from asyncio import Semaphore

from hssp.network import Net
from hssp.settings.settings import settings


async def request(url: str):
    ua = "Mozilla/5.0 (Linux; Android 14; V2172A Build/UP1A.231005.007; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/126.0.6478.188 Mobile Safari/537.36 XWEB/1260079 MMWEBSDK/20240501 MMWEBID/172 MicroMessenger/8.0.50.2701(0x28003255) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64"
    headers = {
        "User-Agent": ua,
        "Cookie": "PHPSESSID=c2i4l531d6gp34psli6pu44d60"
    }
    resp = await net.get(url, headers=headers)


async def main():
    url = "http://lhs.longhushandaoyi.com/home/index/course_detail/id/{page}.html"
    await asyncio.gather(*[request(url.format(page=page)) for page in range(1, 2)])


if __name__ == '__main__':
    sem = Semaphore(settings.concurrency)
    net = Net(sem=sem)
    asyncio.run(main())
