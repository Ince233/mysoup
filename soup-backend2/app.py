# 导入必要的Flask模块
from flask import Flask, request, jsonify, session
# 导入CORS支持跨域请求
from flask_cors import CORS
# 导入LangChain相关模块用于AI功能
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
# 导入dotenv用于加载环境变量
from dotenv import load_dotenv
# 导入其他必要模块
import os
import json
import random
import uuid

# 导入认证相关函数
from auth import (
    register, login, get_profile, logout,
    token_required, generate_token, decode_token
)
# 导入数据库初始化函数
from database import init_db

# ----------------------------
# 初始化
# ----------------------------
# 加载环境变量
load_dotenv()

# 初始化数据库
init_db()

# 创建Flask应用实例
app = Flask(__name__)
# 设置Flask的secret_key用于会话管理
app.secret_key = os.getenv("FLASK_SECRET_KEY", "fallback-secret-key-for-dev")
# 配置CORS允许所有来源访问API接口
CORS(app, resources={r"/api/*": {"origins": "*"}})

# 存储活跃游戏会话的字典
active_games = {}

def load_tang_database():
    """
    加载海龟汤谜题数据库
    从tang.json文件中读取谜题数据
    
    Returns:
        list: 谜题数据列表，每个元素包含汤面和汤底
    """
    try:
        with open("tang.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ 警告: 无法加载 tang.json: {e}")
        return []

# 加载海龟汤谜题数据库
TANG_DB = load_tang_database()

# 初始化LLM模型
llm = ChatOpenAI(
    # 使用的模型名称
    model="deepseek-chat",
    # 从环境变量获取API密钥
    openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
    # DeepSeek API的基础URL
    openai_api_base="https://api.deepseek.com/v1",
    # 生成内容的随机性（0.0-1.0）
    temperature=0.3,
    # 最大重试次数
    max_retries=2,
)

# ----------------------------
# 工具函数
# ----------------------------
def get_or_create_game(session_id):
    if session_id not in active_games:
        if TANG_DB:
            puzzle = random.choice(TANG_DB)
            active_games[session_id] = puzzle
        else:
            prompt = ChatPromptTemplate.from_messages([
                ("system", "请生成一个经典的中文海龟汤谜题（只输出汤面，不要解释）"),
                ("user", "开始")
            ])
            response = (prompt | llm).invoke({})
            active_games[session_id] = {
                "surface": response.content.strip(),
                "bottom": "[动态生成谜题，无固定汤底]"
            }
    return active_games[session_id]

# ----------------------------
# 微信登录路由
# ----------------------------
@app.route('/api/wechat-login', methods=['POST'])
def wechat_login():
    try:
        data = request.json
        if not data:
            return jsonify({'error': '请求体必须是 JSON'}), 400
        
        # 获取微信登录参数
        code = data.get('code')
        user_info = data.get('userInfo', {})
        
        if not code:
            return jsonify({'error': '缺少code参数'}), 400
        
        # TODO: 调用微信API验证code，获取openid和session_key
        # 这里需要实际的微信API调用，暂时模拟
        openid = f'wechat_{uuid.uuid4()}'
        
        # 模拟用户信息
        user = {
            'user_id': openid,
            'username': user_info.get('nickName', '微信用户'),
            'avatar': user_info.get('avatarUrl', ''),
            'openid': openid,
            'session_key': 'mock_session_key'  # 实际应该是微信返回的session_key
        }
        
        # 生成JWT令牌
        token = generate_token(user)
        
        return jsonify({
            'success': True,
            'token': token,
            'user': user
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/decrypt-phone', methods=['POST'])
def decrypt_phone():
    try:
        data = request.json
        if not data:
            return jsonify({'error': '请求体必须是 JSON'}), 400
        
        # 获取解密参数
        encrypted_data = data.get('encryptedData')
        iv = data.get('iv')
        code = data.get('code')
        
        if not all([encrypted_data, iv, code]):
            return jsonify({'error': '缺少必要参数'}), 400
        
        # TODO: 调用微信API解密手机号
        # 这里需要实际的微信API调用，暂时模拟
        phone_number = '13800138000'
        
        return jsonify({
            'success': True,
            'phoneNumber': phone_number
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/logout', methods=['POST'])
def api_logout():
    result, status_code = logout()
    return jsonify(result), status_code

@app.route('/api/profile', methods=['GET'])
@token_required
def api_profile():
    user_id = request.current_user['user_id']
    result, status_code = get_profile(user_id)
    return jsonify(result), status_code

@app.route('/api/verify-token', methods=['GET'])
def api_verify_token():
    token = None
    
    if 'Authorization' in request.headers:
        auth_header = request.headers['Authorization']
        if auth_header.startswith('Bearer '):
            token = auth_header[7:]
    
    if not token:
        return jsonify({'valid': False, 'error': '缺少Token'}), 401
    
    payload = decode_token(token)
    if not payload:
        return jsonify({'valid': False, 'error': '无效或已过期的Token'}), 401
    
    return jsonify({
        'valid': True,
        'user': {
            'user_id': payload['user_id'],
            'username': payload['username'],
            'email': payload['email']
        }
    }), 200

# ----------------------------
# 游戏路由
# ----------------------------
@app.route('/')
def index():
    return jsonify({
        'status': 'success',
        'message': '🐢 海龟汤 RAG 增强 AI 服务正在运行',
        'endpoints': {
            'chat': '/api/chat',
            'register': '/api/register',
            'login': '/api/login',
            'logout': '/api/logout',
            'profile': '/api/profile',
            'verify_token': '/api/verify-token'
        },
        'instructions': '发送 POST /api/chat with { "messages": [...] }，建议携带 session_id'
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        if not data:
            return jsonify({'error': '请求体必须是 JSON'}), 400

        session_id = data.get("session_id")
        if not session_id:
            session_id = str(uuid.uuid4())

        puzzle = get_or_create_game(session_id)
        
        enhanced_system = f"""
你是一位专业的"海龟汤"游戏主持人。本局谜题如下：

【汤面】
{puzzle['surface']}

【汤底（仅供内部判断，严禁提前泄露！）】
{puzzle['bottom']}

规则：
1. 如果这是第一条消息，请只回复【汤面】内容，不要加任何解释。
2. 玩家提问时，仅回答："是"、"不是"、"无关"或"无法回答"。
3. 若玩家说"我放弃"或准确描述汤底，请完整揭示汤底并简要解释。
4. 保持简洁、中立，不诱导，不编造。
"""

        messages = [("system", enhanced_system)]
        
        user_messages = data.get("messages", [])
        for msg in user_messages:
            role = msg.get("role")
            content = msg.get("content", "")
            if role == "user":
                messages.append(("human", content))
            elif role == "assistant":
                messages.append(("ai", content))

        prompt = ChatPromptTemplate.from_messages(messages)
        chain = prompt | llm
        response = chain.invoke({})

        return jsonify({
            "session_id": session_id,
            "content": response.content.strip(),
            "status": "success"
        })

    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

@app.route('/api/reset', methods=['POST'])
def reset_game():
    session_id = request.json.get("session_id")
    if session_id and session_id in active_games:
        del active_games[session_id]
    return jsonify({"message": "游戏已重置", "session_id": session_id})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
