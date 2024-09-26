#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : tune
# @Time         : 2024/9/20 13:51
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import uuid

from meutils.pipe import *
from meutils.decorators.retry import retrying

from meutils.notice.feishu import send_message as _send_message
from meutils.db.redis_db import redis_client, redis_aclient
from meutils.config_utils.lark_utils import aget_spreadsheet_values, get_next_token_for_polling

from meutils.llm.utils import oneturn2multiturn
from meutils.schemas.openai_types import chat_completion, chat_completion_chunk, ChatCompletionRequest, CompletionUsage
from meutils.schemas.oneapi_types import REDIRECT_MODEL

BASE_URL = "https://chat.tune.app"
FEISHU_URL_VIP = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=gCrlN4"
FEISHU_URL_API = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=9HwQtX"
"https://chat.tune.app/api/models"
# r = requests.get("https://chat.tune.app/tune-api/appConfig")
# r = requests.get("https://chat.tune.app/api/guestLogin")

send_message = partial(
    _send_message,
    url="https://open.feishu.cn/open-apis/bot/v2/hook/e0db85db-0daf-4250-9131-a98d19b909a9",
    title=__name__
)


@alru_cache(ttl=1000)
@retrying(predicate=lambda r: r is None)
async def get_access_token():
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=100) as client:
        response = await client.get("/api/guestLogin")

        logger.debug(response.status_code)
        logger.debug(response.text)

        if response.is_success:
            return response.json()["accessToken"]


@retrying()
async def create_conversation_id(token: Optional[str] = None):
    token = token or await get_access_token()
    headers = {
        "authorization": token
    }
    conversation_id = str(uuid.uuid4())  # shortuuid.random()
    params = {
        "conversation_id": conversation_id,
        "organization_id": "undefined",
        "model": "anthropic/claude-3.5-sonnet",  # "kaushikaakash04/tune-blob",
        "currency": "USD"
    }
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=100) as client:
        response = await client.post("/api/new", params=params)

        logger.debug(response.status_code)
        logger.debug(response.text)

        if response.is_success:
            return conversation_id


async def create(request: ChatCompletionRequest, token: Optional[str] = None, vip: Optional[bool] = False):
    if vip:
        token = await get_next_token_for_polling(feishu_url=FEISHU_URL_VIP)
    token = token or await get_access_token()

    conversation_id = await create_conversation_id(token)

    use_search = False
    if request.messages[0].get('role') != 'system':  # 还原系统信息
        request.messages.insert(0, {'role': 'system', 'content': f'You are {request.model}'})

    if request.model.startswith("net-") or request.model.endswith("all"):
        request.model = "kaushikaakash04/tune-blob"
        use_search = True
    else:
        request.model = REDIRECT_MODEL.get(request.model, "anthropic/claude-3.5-sonnet")

    headers = {
        "authorization": token,
        "content-type": "text/plain;charset=UTF-8"
    }
    params = {
        "organization_id": "undefined",
        "retry": 2,
    }
    payload = {
        # "query": request.last_content,
        "query": oneturn2multiturn(request.messages),

        "conversation_id": conversation_id,
        "model_id": request.model,  # "kaushikaakash04/tune-blob"
        "browseWeb": use_search,
        "attachement": "",
        "attachment_name": "",
        # "messageId": "4a33e497-efb7-4d8f-ae45-9aa7d2c1c5af1726811555410",
        "prevMessageId": "",
        #     "images": [
        #         "https://d2e931syjhr5o9.cloudfront.net/db2a325a-e12d-416e-ad7a-a80a78d2785d_1726892991565.png"
        #     ]
    }

    yield "\n"  # 提升首字速度
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=300) as client:
        async with client.stream("POST", "/api/prompt", json=payload, params=params) as response:
            logger.debug(response.status_code)
            # logger.debug(response.text)

            async for chunk in response.aiter_lines():
                # logger.debug(chunk)

                if chunk and chunk.startswith("{"):
                    chunk = (
                        chunk.replace("Blob", "OpenAI")
                        .replace("Tune", "OpenAI")
                        .replace("https://studio.tune.app", "https://opanai.com")
                        .replace("https://tunehq.ai", "https://opanai.com")
                        .replace("https://chat.tune.app", "https://opanai.com")
                    )

                    try:
                        chunk = json.loads(chunk)
                        chunk = chunk.get('value', "")
                        yield chunk
                        # break

                    except Exception as e:
                        _ = f"{e}\n{chunk}"
                        logger.error(_)
                        send_message(_)
                        yield ""
                elif chunk.strip():
                    logger.debug(chunk)

            # {"value": "完成"}


if __name__ == '__main__':
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzI2OTk2MzA3LCJpYXQiOjE3MjY4MjM1MDcsInN1YiI6ImNhYzk5N2Y1LWViN2YtNDJmNC05NGRhLTdiZWNlMTg3NDJjMyIsImVtYWlsIjoiMzEzMzAzMzAzQHFxLmNvbSIsInBob25lIjoiIiwiYXBwX21ldGFkYXRhIjp7InByb3ZpZGVyIjoiZ2l0aHViIiwicHJvdmlkZXJzIjpbImdpdGh1YiJdfSwidXNlcl9tZXRhZGF0YSI6eyJhdmF0YXJfdXJsIjoiaHR0cHM6Ly9hdmF0YXJzLmdpdGh1YnVzZXJjb250ZW50LmNvbS91LzIwMjY1MzIxP3Y9NCIsImRlZmF1bHRfb3JnYW5pemF0aW9uX2lkIjoiZWIwZmI5OTYtMjMxNy00NjdiLTk4NDctMTVmNmM0MDAwMGI3IiwiZW1haWwiOiIzMTMzMDMzMDNAcXEuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZ1bGxfbmFtZSI6IkJldHRlcm1lIiwiaXNzIjoiaHR0cHM6Ly9hcGkuZ2l0aHViLmNvbSIsImxhc3RfcGFzc3dvcmRfY2hhbmdlZF9hdCI6IjIwMjQtMDktMjBUMDk6MTE6NDAuOTcxOTY2NjkyWiIsIm5hbWUiOiJCZXR0ZXJtZSIsInByZWZlcnJlZF91c2VybmFtZSI6Inl1YW5qaWUtYWkiLCJwcm92aWRlcl9pZCI6IjIwMjY1MzIxIiwic3ViIjoiMjAyNjUzMjEiLCJ1c2VyX25hbWUiOiJ5dWFuamllLWFpIn0sInJvbGUiOiJhdXRoZW50aWNhdGVkIiwiYWFsIjoiYWFsMSIsImFtciI6W3sibWV0aG9kIjoib2F1dGgiLCJ0aW1lc3RhbXAiOjE3MjY4MjM1MDd9XSwic2Vzc2lvbl9pZCI6ImYzNzIxOTcyLTdmODMtNDc4Yi05ZmRmLTQwZjBkZWU3YTcxZiJ9.cwgLtemJKnJuL9laCalW86lAGWqqvK50gOAJMuKafVw"
    # arun(get_access_token())
    arun(create_conversation_id(token))

    model = "anthropic/claude-3.5-sonnet"
    model = "net-anthropic/claude-3.5-sonnet"
    model = "all"

    # model = "kaushikaakash04/tune-blob"
    # model = "openai/o1-mini"
    request = ChatCompletionRequest(model=model, messages=[
        {'role': 'user', 'content': '南京天气怎么样'}
    ])

    arun(create(request, token=token, vip=True))

#  curl -X POST "https://any2chat.chatfire.cn/tune/v1/chat/completions" \
# -H "Authorization: Bearer sk-tune-0UkSny4Fe7ouhF3GPI0lIAKIAj7B2kkJmOV" \
# -H "Content-Type: application/json" \
# -d '{
#   "temperature": 0.8,
#   "messages": [
#   {
#     "role": "user",
#     "content": "1+1"
#   }
# ],
#   "model": "anthropic/claude-3.5-sonnet",
#   "stream": true,
#   "frequency_penalty": 0,
#   "max_tokens": 900
# }'

# {
#     "query": "解释",
#     "conversation_id": "dad4d23e-ee0e-4525-aca5-025d26b8c807",
#     "model_id": "qwen/qwen-2-vl-72b",
#     "browseWeb": false,
#     "attachement": "",
#     "attachment_name": "",
#     "messageId": "fe438968-f9d1-484d-9cea-3c616a02e4491726892994870",
#     "prevMessageId": "",
#     "images": [
#         "https://d2e931syjhr5o9.cloudfront.net/db2a325a-e12d-416e-ad7a-a80a78d2785d_1726892991565.png"
#     ]
# }
