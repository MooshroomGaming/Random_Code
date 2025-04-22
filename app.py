from typing import List, Tuple, Union
from web_ui import WebUI
import math
import os

from qwen_agent.agents import Assistant
from qwen_agent.gui.gradio import gr

def app_gui():
    # Define the agent
    bot = Assistant(llm={
                    'model': os.environ.get("MODELNAME"),
                    'model_type': 'qwen_dashscope',
                    'generate_cfg': {
                        'max_input_tokens': 32768,
                        'max_retries': 10,
                        'temperature': float(os.environ.get("T", 0.001)),
                        'repetition_penalty': float(os.environ.get("R", 1.0)),
                        "top_k": int(os.environ.get("K", 20)),
                        "top_p": float(os.environ.get("P", 0.8)),
                    }},
                    name='QwQ-32B-preview',
                    description='QwQ-32B-Preview is an experimental research model developed by the Qwen Team, focused on advancing AI reasoning capabilities. As a preview release, it demonstrates promising analytical abilities while having several important limitations such as code switching and recursive reasoning loops. Only single-turn queries are supported in this demo.',
                    system_message= 'You are a helpful and harmless assistant. You are Qwen developed by Alibaba. You should think step-by-step.',
                    rag_cfg={'max_ref_token': 32768, 'rag_searchers': []},
                )
    chatbot_config = {
        'input.placeholder': "Type \"/clear\" to clear the history",
        'verbose': True,
        'prompt.suggestions': [
            {
                'text': 'How many r in strawberry'
            },
            {
                'text': 'Find the least odd prime factor of $2019^8+1$.'
            },
            {
                'text': '''S先生、P先生、Q先生他们知道桌子的抽屉里有16张扑克牌：红桃A、Q、4 黑桃J、8、4、2、7、3 草花K、Q、5、4、6 方块A、5。约翰教授从这16张牌中挑出一张牌来，并把这张牌的点数告诉 P先生，把这张牌的花色告诉Q先生。这时，约翰教授问P先生和Q 先生：你们能从已知的点数或花色中推知这张牌是什么牌吗？于是，S先生听到如下的对话：

P先生：我不知道这张牌。

Q先生：我知道你不知道这张牌。

P先生：现在我知道这张牌了。

Q先生：我也知道了。

请问：这张牌是什么牌？'''
            },
        ]
    }
    WebUI(bot, chatbot_config=chatbot_config).run(concurrency_limit=80)

if __name__ == '__main__':
    app_gui()
