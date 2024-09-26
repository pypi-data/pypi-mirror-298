#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : utils
# @Time         : 2024/9/26 15:54
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

url = "https://api.siliconflow.cn/v1/user/info"


async def check_token(api_key):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json"
    }

    async with httpx.AsyncClient(headers=headers, timeout=60) as client:
        response: httpx.Response = await client.get(url)
        response.raise_for_status()

        logger.debug(response.text)
        logger.debug(response.status_code)

        if response.is_success:
            balance = response.json()['data']['balance']
            return float(balance) > 0


if __name__ == '__main__':
    api_key = os.getenv("SILICONFLOW_API_KEY")
    arun(check_token(api_key))
