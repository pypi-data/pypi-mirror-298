import asyncio

from hssp.logger.log import Logger
from hssp.network import Net
from hssp.network.downloader import CurlCffiDownloader


async def main():
    url = "https://tools.scrapfly.io/api/fp/ja3"
    net = Net(downloader_cls=CurlCffiDownloader)
    resp = await net.get(url)
    logger.info(resp.text)
    await net.close()


if __name__ == '__main__':
    Logger.init_logger()
    logger = Logger.get_logger("test")
    asyncio.run(main())
