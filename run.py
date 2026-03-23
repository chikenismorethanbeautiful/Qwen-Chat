#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
统一Qwen聊天机器人启动器
只需要Qwen3.0的代码，可以加载1.5、2.5、3.0的模型权重
"""

import sys
import os
import argparse
import subprocess

# 配置不同版本的模型路径
MODEL_CONFIGS = {
    '1.5': {
        'name': 'Qwen1.5-0.5B-Instruct',
        'path': './qwen/Qwen1.5-0.5B-Chat',  # 改成你实际的1.5模型路径
        'description': '轻量级模型，适合快速响应'
    },
    '2.5': {
        'name': 'Qwen2.5-0.5B-Instruct',
        'path': './qwen/Qwen2.5-0.5B-Instruct',  # 改成你实际的2.5模型路径
        'description': '改进版本，性能更优'
    },
    '3.0': {
        'name': 'Qwen3-0.5B-Instruct',
        'path': './qwen/Qwen3-0.6B',  # 改成你实际的3.0模型路径
        'description': '最新版本，更强的能力'
    }
}


def run_chatbot(version, host='127.0.0.1', port=8000, custom_path=None):
    """启动指定版本的Qwen聊天机器人"""

    if version not in MODEL_CONFIGS:
        print(f"错误：不支持的版本 '{version}'")
        print(f"支持的版本：{', '.join(MODEL_CONFIGS.keys())}")
        return

    config = MODEL_CONFIGS[version]
    model_path = custom_path if custom_path else config['path']

    # 检查模型路径是否存在
    if not os.path.exists(model_path):
        print(f"错误：模型路径不存在 {model_path}")
        print(f"请检查以下路径是否正确：")
        print(f"  - 1.5: {MODEL_CONFIGS['1.5']['path']}")
        print(f"  - 2.5: {MODEL_CONFIGS['2.5']['path']}")
        print(f"  - 3.0: {MODEL_CONFIGS['3.0']['path']}")
        return

    # 检查web_demo.py是否存在
    web_demo_path = os.path.join(os.path.dirname(__file__), 'examples/demo/web_demo.py')
    if not os.path.exists(web_demo_path):
        print(f"错误：web_demo.py 不存在 {web_demo_path}")
        return

    print(f"=" * 60)
    print(f"🚀 正在启动 Qwen{version} 聊天机器人...")
    print(f"📦 模型版本: {config['name']}")
    print(f"📁 模型路径: {model_path}")
    print(f"💡 模型说明: {config['description']}")
    print(f"🌐 访问地址: http://{host}:{port}")
    print(f"=" * 60)

    # 运行web_demo.py，传递参数
    cmd = [
        sys.executable,
        web_demo_path,
        '--model_version', version,
        '--model_path', model_path,
        '--server_name', host,
        '--server_port', str(port)
    ]

    print(f"执行命令: {' '.join(cmd)}")
    print("\n按 Ctrl+C 停止服务\n")

    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n\n👋 服务已停止")


def main():
    parser = argparse.ArgumentParser(
        description='统一Qwen聊天机器人启动器 - 只需Qwen3.0代码，支持1.5/2.5/3.0',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python run_unified.py 1.5              # 启动 Qwen1.5
  python run_unified.py 2.5 --port 8001 # 启动 Qwen2.5 在 8001 端口
  python run_unified.py 3.0              # 启动 Qwen3.0
  python run_unified.py 2.5 --path ./my_model  # 使用自定义模型路径
        """
    )

    parser.add_argument('version', choices=['1.5', '2.5', '3.0'],
                        help='Qwen模型版本')
    parser.add_argument('--host', default='127.0.0.1',
                        help='绑定的主机地址 (默认: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=8000,
                        help='绑定的端口 (默认: 8000)')
    parser.add_argument('--path', type=str, default=None,
                        help='自定义模型路径 (可选)')

    args = parser.parse_args()
    run_chatbot(args.version, args.host, args.port, args.path)


if __name__ == '__main__':
    main()