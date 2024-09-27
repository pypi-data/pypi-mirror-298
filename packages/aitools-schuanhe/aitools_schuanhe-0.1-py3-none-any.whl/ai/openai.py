from aitools_schuanhe.config import Config
from aitools_schuanhe.types.chat_model import ChatOpenAiModel
from aitools_schuanhe.utils.request import request_api


def gpt_35_api(messages: list, config: Config):
    if api_init(config):
        url = config.get_openai_url()
        headers = config.get_openai_headers()
        data = config.get_openai_message(messages)
        return request_api(url, headers, data, config)
    else:
        return None


def api_init(config: Config):
    if config.model in ChatOpenAiModel.__args__:
        if config.get_openai_key() == "":
            print("请先配置openai的api_key")
            if config.get_openai_url() == "":
                print("请先配置openai的url")
                return False
            return False
    else:
        print("不支持的模型")
        return False
    return True

