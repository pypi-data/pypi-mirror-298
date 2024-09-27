import json
import requests

from aitools_schuanhe.config import Config
from aitools_schuanhe.log.db_log import save_to_db


def request_api(url, headers, data, config: Config):
    try:
        print("请求地址:", url)
        print("请求头:", headers)
        print("请求参数:", data)
        inserted_id = save_to_db(data, "request_log", config)

        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # 如果请求失败，抛出异常
        result = response.json()
        result["request_id"] = inserted_id
        save_to_db(result, "response_log", config)
        print("返回结果:", result)
        return result
    except requests.exceptions.RequestException as e:
        print(f'HTTP请求错误: {e}')
        return None


def set_openai_message(add_message: str, messages=None):
    """
    设置openai的message
    """
    if messages is None:
        messages = []
    messages.append({"role": "user", "content": add_message})
    return messages


def set_openai_system(system_message: str, messages=None):
    """
    设置openai的system message
    """
    if messages is None:
        messages = []
    messages.append({"role": "system", "content": system_message})
    return messages


def set_openai_assistant(assistant_message: str, messages=None):
    """
    设置openai的assistant message
    """
    if messages is None:
        messages = []
    messages.append({"role": "assistant", "content": assistant_message})
    return messages
