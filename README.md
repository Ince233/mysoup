# MySoup - 海龟汤推理游戏

MySoup 是一个基于 AI 的海龟汤推理游戏平台，玩家可以与 AI 主持人进行互动，通过提问来解开谜题。

## 技术栈

### 前端 (soup-frontend)
- 框架：uni-app
- UI 框架：uni-ui
- 开发语言：Vue.js
- 运行环境：HBuilderX

### 后端 (soup-backend)
- 框架：Flask
- 开发语言：Python 3.x
- AI 服务：火山引擎 Ark 服务
- 依赖管理：pip

## 版本需求

### 前端
- HBuilderX 3.0+
- Node.js 14.0+
- Vue.js 2.x

### 后端
- Python 3.8+
- Flask 2.0.1
- Flask-CORS 3.0.10
- volcengine-python-sdk[ark]
- python-dotenv 0.19.0
- werkzeug 2.0.3

## 项目结构
```
mysoup/
├── soup-frontend/          # 前端项目
│   ├── pages/             # 页面文件
│   ├── static/            # 静态资源
│   ├── common/            # 公共组件
│   └── uni_modules/       # uni-app 模块
└── soup-backend/          # 后端项目
    ├── app.py            # 主应用文件
    ├── requirements.txt   # Python 依赖
    └── .env              # 环境变量配置
```

## 运行指南

### 首次设置

#### 前端设置
1. 使用 HBuilderX 打开 `soup-frontend` 目录
2. 在 HBuilderX 中运行项目（运行到浏览器或模拟器）

#### 后端设置
1. 进入 `soup-backend` 目录
2. 创建虚拟环境（仅首次需要）：
   ```bash
   python -m venv venv
   ```
3. 安装依赖（仅首次需要）：
   ```bash
   # Windows
   .\venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```
4. 创建 `.env` 文件并配置 API Key（仅首次需要）：
   ```
   ARK_API_KEY=你的火山引擎API Key
   ```

### 日常运行

#### 前端运行
- 在 HBuilderX 中点击运行按钮即可

#### 后端运行
1. 进入 `soup-backend` 目录
2. 激活虚拟环境：
   ```bash
   # Windows
   .\venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```
3. 启动服务：
   ```bash
   python app.py
   ```

> 注意：每次打开新的终端窗口都需要重新激活虚拟环境，但不需要重新安装依赖。

## API 接口文档

### 1. 聊天接口

#### 请求
- URL: `/api/chat`
- 方法: `POST`
- Content-Type: `application/json`

#### 请求体
```json
{
    "messages": [
        {
            "role": "system",
            "content": "你是海龟汤游戏的主持人..."
        },
        {
            "role": "user",
            "content": "用户消息"
        }
    ]
}
```

#### 响应
```json
{
    "content": "AI回复内容",
    "references": [],
    "reasoning": "推理过程（如果有）"
}
```

### 2. 状态检查接口

#### 请求
- URL: `/`
- 方法: `GET`

#### 响应
```json
{
    "status": "success",
    "message": "海龟汤AI服务正在运行",
    "endpoints": {
        "chat": "/api/chat"
    }
}
```

## 开发注意事项

1. 前端开发
   - 使用 HBuilderX 进行开发和调试
   - 遵循 uni-app 的开发规范
   - 注意跨域请求配置

2. 后端开发
   - 确保 Python 虚拟环境正确配置
   - 保护 API Key 等敏感信息
   - 遵循 RESTful API 设计规范

## 常见问题

1. 跨域问题
   - 确保后端 CORS 配置正确
   - 检查前端请求 URL 是否正确

2. API Key 问题
   - 确保 `.env` 文件存在且配置正确
   - 检查 API Key 是否有效

3. 依赖问题
   - 确保所有依赖版本匹配
   - 使用 `pip freeze` 检查依赖版本

4. 虚拟环境问题
   - 如果遇到依赖相关错误，确保虚拟环境已激活
   - 如果依赖缺失，可以重新运行 `pip install -r requirements.txt`

## 贡献指南

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License 