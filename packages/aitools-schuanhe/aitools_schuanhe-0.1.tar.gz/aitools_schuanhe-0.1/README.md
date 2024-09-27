# ai_tools

这是一个基于Python的AI工具包

示例
```python
from aitools_schuanhe.ai.openai import gpt_35_api
from aitools_schuanhe.config import *
from aitools_schuanhe.utils.request import set_openai_message, set_openai_system
config = Config(
    openai_key="xxxx",
    openai_url="https://xxxx",
)
messages = set_openai_system("你是AI助手，你的名字叫小爱，你的任务是帮助用户回答问题，")
messages = set_openai_message("你好啊，请问你叫什么名字？", messages)
print(gpt_35_api(messages, config))

```