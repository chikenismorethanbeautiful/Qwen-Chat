#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Qwen 聊天机器人 - 统一版本
支持加载 Qwen1.5、Qwen2.5、Qwen3.0 的模型权重
"""

import argparse
import gradio as gr
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# 添加命令行参数解析
parser = argparse.ArgumentParser(description='Qwen ChatBot - 统一版本')
parser.add_argument('--model_version', type=str, default='3.0',
                    choices=['1.5', '2.5', '3.0'],
                    help='Qwen模型版本: 1.5, 2.5, 3.0')
parser.add_argument('--model_path', type=str, default=None,
                    help='模型路径，如果不指定则根据版本自动选择')
parser.add_argument('--server_name', type=str, default='127.0.0.1',
                    help='服务器地址')
parser.add_argument('--server_port', type=int, default=8000,
                    help='服务器端口')
args = parser.parse_args()

# 根据版本自动选择模型路径（如果你把模型都放在统一目录下）
MODEL_PATHS = {
    '1.5': './qwen/Qwen1.5-0.5B-Chat',  # 1.5的模型路径
    '2.5': './qwen/Qwen2.5-0.5B-Instruct',  # 2.5的模型路径
    '3.0': './qwen/Qwen3-0.6B'  # 3.0的模型路径
}

# 确定使用的模型路径
if args.model_path:
    DEFAULT_CKPT_PATH = args.model_path
else:
    DEFAULT_CKPT_PATH = MODEL_PATHS.get(args.model_version, MODEL_PATHS['3.0'])

print(f"正在加载模型: {args.model_version}")
print(f"模型路径: {DEFAULT_CKPT_PATH}")

# 加载模型和tokenizer（原有代码保持不变）
tokenizer = AutoTokenizer.from_pretrained(DEFAULT_CKPT_PATH, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    DEFAULT_CKPT_PATH,
    torch_dtype="auto",
    device_map="auto",
    trust_remote_code=True
)


def predict(message, history):
    """对话预测函数"""
    # 这里的代码保持不变，就是你原有的predict函数
    messages = []
    for user_msg, bot_msg in history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": bot_msg})
    messages.append({"role": "user", "content": message})

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    generated_ids = model.generate(
        model_inputs.input_ids,
        max_new_tokens=512,
        temperature=0.7,
        do_sample=True
    )

    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return response


# 创建界面
demo = gr.ChatInterface(
    fn=predict,
    title=f"Qwen {args.model_version} ChatBot",
    description=f"基于 Qwen {args.model_version} 的对话机器人，模型路径：{DEFAULT_CKPT_PATH}"
)

# 启动服务
demo.launch(server_name=args.server_name, server_port=args.server_port)