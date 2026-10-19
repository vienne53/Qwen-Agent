# Copyright 2023 The Qwen team, Alibaba Group. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied. See the License for the specific language governing
# permissions and limitations under the License.

"""RAG WebUI：右侧 Agents 下拉即选模型（控 token / 是否听语音）。"""

from qwen_agent.agents import Assistant
from qwen_agent.gui import WebUI

# name 会出现在 UI「Agents」下拉；按费用从低到高排
MODEL_PRESETS = [
    {
        'name': '省钱 Turbo',
        'description': '低成本文本。适合简单问答，省 token。',
        'llm': {'model': 'qwen-turbo'},
    },
    {
        'name': '均衡 Plus',
        'description': '默认推荐。文档 RAG，性价比均衡。',
        'llm': {'model': 'qwen-plus-latest'},
    },
    {
        'name': '强力 Max',
        'description': '更强推理，更贵。难题再用。',
        'llm': {'model': 'qwen-max'},
    },
    {
        'name': '语音 Omni',
        'description': '可听麦克风（音/图/视频）。多模态计价，按需开。',
        'llm': {
            'model_type': 'qwenomni_oai',
            'model': 'qwen-omni-turbo-latest',
            'base_url': 'https://dashscope.aliyuncs.com/compatible-mode/v1',
        },
    },
]


def _build_bots():
    return [
        Assistant(
            llm=p['llm'],
            name=p['name'],
            description=p['description'],
        ) for p in MODEL_PRESETS
    ]


def test():
    bot = Assistant(llm={'model': 'qwen-plus-latest'})
    messages = [{'role': 'user', 'content': [{'text': '介绍图一'}, {'file': 'https://arxiv.org/pdf/1706.03762.pdf'}]}]
    for rsp in bot.run(messages):
        print(rsp)


def app_gui():
    bots = _build_bots()
    chatbot_config = {
        'prompt.suggestions': [
            {'text': '介绍图一'},
            {'text': '第二章第一句话是什么？'},
        ],
        'input.placeholder': '先在右侧选模型（省钱/均衡/强力/语音），再提问或上传文件',
    }
    # 传入列表 → WebUI 右侧出现 Agents 下拉，用来切换模型做预算管理
    WebUI(bots, chatbot_config=chatbot_config).run(share=True)


if __name__ == '__main__':
    # test()
    app_gui()
