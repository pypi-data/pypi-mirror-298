import asyncio

from hssp.logger.log import Logger
from hssp.network import Net


async def main():
    url = "https://cfws.samr.gov.cn/queryDoc"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "Cookie": "SHAREJSESSIONID=20e6284c-de7f-4c40-9983-65a88318b1ca; __jsluid_s=49b429054b7feb093a7c43138682b4f7",
    }
    resp = await net.post(url, headers=headers, form_data={
        "pageSize": 20,
        "pageNum": 1,
        "queryCondition": '[{"key":"19_s","id":"610900","name":"行政区划：陕西省安康市 "},{"key":"24_i","id":"2024","name":"处罚年份:2024 "},{"key":"8_ss","id":"01","name":"处罚种类:警告 "}]',
        "sortFields": "",
        "ciphertext": "110010 1110010 1010000 1110111 1001100 1110000 1010111 1111010 1110101 1001110 1101101 1010001 1000010 1001101 1000111 111000 1101101 1010010 1001011 110100 1110100 1010000 110110 1111001 110010 110000 110010 110100 110000 111001 110010 110101 1010001 1100100 110101 110001 110100 1000100 1100010 1101111 1010011 1110101 1001000 1000101 1011001 1000101 110000 1000101 1110100 1101000 1011001 1101000 1010100 1000001 111101 111101"
    })
    logger.info(f"Got response: {resp.text}")
    await net.close()


if __name__ == '__main__':
    Logger.init_logger()
    logger = Logger.get_logger("test")
    net = Net()
    asyncio.run(main())
