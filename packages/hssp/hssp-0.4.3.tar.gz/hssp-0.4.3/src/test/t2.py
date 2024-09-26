import asyncio

from hssp.logger.log import Logger
from hssp.network import Net


async def get_rtp():
    url = "http://127.0.0.1:9000/jili/calc-rtp"
    json_data = {
        "game_id": "fgp",
        "game_count": 5000,
        "default_money": 5000,
        "config_id": 1
    }
    resp = await net.post(url, json_data=json_data)
    rtp = resp.json.get("data")['value']
    return rtp


async def main():
    results = await asyncio.gather(*[get_rtp() for _ in range(100)])
    await net.close()
    logger.info(f"Results: {results}")
    logger.info(f"最大RTP: {max(results)}")
    logger.info(f"最小RTP: {min(results)}")


if __name__ == '__main__':
    Logger.init_logger()
    logger = Logger.get_logger("test")
    net = Net()
    asyncio.run(main())
