#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : got_ocr
# @Time         : 2024/9/26 18:21
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

from gradio_client import Client as _Client, handle_file

Client = lru_cache(_Client)

client = Client("stepfun-ai/GOT_official_online_demo")
result = client.predict(
    image=handle_file('https://raw.githubusercontent.com/gradio-app/gradio/main/test/test_files/bus.png'),
    got_mode="plain texts OCR",
    fine_grained_mode="box",
    ocr_color="red",
    ocr_box="Hello!!",
    api_name="/run_GOT"
)
print(result)
