import jwt
import bcrypt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
from database import (
    get_user_by_username,
    get_user_by_email,
    get_user_by_id,
    create_user
)

SECRET_KEY = 'your-super-secret-key-change-in-production'
ALGORITHM = 'HS256'
TOKEN_EXPIRY_HOURS = 24

def hash_password(password):
    """加密密码"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password, password_hash):
    """验证密码"""
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

def generate_token(user):
    """生成JWT Token"""
    payload = {
        'user_id': user.get('user_id'),
        'username': user.get('username', '微信用户'),
        'email': user.get('email', ''),
        'openid': user.get('openid', ''),
        'exp': datetime.utcnow() + timedelta(hours=TOKEN_EXPIRY_HOURS),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token):
    """解析JWT Token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    """需要Token验证的装饰器"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header[7:]
        
        if not token:
            return jsonify({'error': '缺少认证Token', 'status': 'error'}), 401
        
        payload = decode_token(token)
        if not payload:
            return jsonify({'error': '无效或已过期的Token', 'status': 'error'}), 401
        
        request.current_user = payload
        return f(*args, **kwargs)
    
    return decorated

def validate_email(email):
    """验证邮箱格式"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """验证密码强度"""
    if len(password) < 6:
        return False
    return True

def validate_username(username):
    """验证用户名格式"""
    if len(username) < 3 or len(username) > 20:
        return False
    return username.isalnum()

def register(username, email, password):
    """用户注册"""
    errors = []
    
    if not validate_username(username):
        errors.append('用户名必须是3-20个字母或数字')
    
    if not validate_email(email):
        errors.append('邮箱格式不正确')
    
    if not validate_password(password):
        errors.append('密码长度至少6位')
    
    if errors:
        return {'success': False, 'errors': errors}, 400
    
    if get_user_by_username(username):
        errors.append('用户名已存在')
        return {'success': False, 'errors': errors}, 400
    
    if get_user_by_email(email):
        errors.append('邮箱已被注册')
        return {'success': False, 'errors': errors}, 400
    
    password_hash = hash_password(password)
    user_id = create_user(username, email, password_hash)
    
    if user_id:
        token = generate_token(user_id, username, email)
        return {
            'success': True,
            'message': '注册成功',
            'user': {
                'id': user_id,
                'username': username,
                'email': email
            },
            'token': token
        }, 201
    else:
        return {'success': False, 'errors': ['注册失败，请稍后重试']}, 500

def login(username_or_email, password):
    """用户登录"""
    errors = []
    
    if not username_or_email or not password:
        errors.append('用户名/邮箱和密码不能为空')
        return {'success': False, 'errors': errors}, 400
    
    user = None
    if '@' in username_or_email:
        user = get_user_by_email(username_or_email)
    else:
        user = get_user_by_username(username_or_email)
    
    if not user:
        errors.append('用户不存在')
        return {'success': False, 'errors': errors}, 401
    
    if not verify_password(password, user['password_hash']):
        errors.append('密码错误')
        return {'success': False, 'errors': errors}, 401
    
    token = generate_token(user['id'], user['username'], user['email'])
    return {
        'success': True,
        'message': '登录成功',
        'user': {
            'id': user['id'],
            'username': user['username'],
            'email': user['email']
        },
        'token': token
    }, 200

def get_profile(user_id):
    """获取用户信息"""
    user = get_user_by_id(user_id)
    if not user:
        return {'success': False, 'error': '用户不存在'}, 404
    
    return {
        'success': True,
        'user': {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'created_at': user['created_at']
        }
    }, 200

def logout():
    """退出登录（前端清除Token即可）"""
    return {
        'success': True,
        'message': '退出成功'
    }, 200
