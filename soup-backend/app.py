from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

try:
    from volcenginesdkarkruntime import Ark
except ImportError:
    Ark = None

# 加载环境变量
load_dotenv()

app = Flask(__name__)
CORS(app)

# 初始化Ark客户端（如果SDK可用）
if Ark:
    client = Ark(
        base_url="https://ark.cn-beijing.volces.com/api/v3",
        api_key=os.environ.get("ARK_API_KEY"),
    )
else:
    client = None

@app.route('/')
def index():
    return jsonify({
        'status': 'success',
        'message': '海龟汤AI服务正在运行',
        'endpoints': {
            'chat': '/api/chat'
        }
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    if not client:
        return jsonify({'error': 'volcenginesdkarkruntime 未安装'}), 500
    try:
        data = request.json
        messages = data.get('messages', [])
        # 系统提示词
        system_message = {
            "role": "system",
            "content": "你是一个海龟汤游戏的主持人，你需要根据玩家的问题给出适当的提示，但不能直接说出答案。你的回答要简短、神秘，引导玩家思考。"
        }
        if not messages or messages[0].get('role') != 'system':
            messages.insert(0, system_message)
        completion = client.bot_chat.completions.create(
            model="bot-20250605165530-fgzmf",
            messages=messages,
        )
        response = {
            'content': completion.choices[0].message.content,
            'references': completion.references,
            'reasoning': completion.choices[0].message.reasoning_content
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) 