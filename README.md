# Chat-BI

## ✨ 项目简介

你用大白话提要求，它能自动帮你从数据库里找出数据，并做成柱状图、饼图之类的图表给你看。

⭐ 如果这个项目对您有帮助，请给我一个Star！

## 🏗️ 系统架构

```
Frontend (React + TypeScript)
    ↓
Backend API (FastAPI + Python)
    ↓
┌─────────────────┬─────────────────┐
│  Business DB    │   System DB     │
│   (MySQL)       │   (MySQL)       │
└─────────────────┴─────────────────┘
    ↓
Vector Database (Milvus)
    ↓
AI Services (OpenAI)
```

### 调用流程
1. 问题向量化，目的是将用户的自然语言问题转化为向量，方便在数据库中寻找类似的SQL查询模板。

2. 生成SQL查询。如果没有找到匹配的模板，系统会根据数据库结构和用户问题生成一条新的SQL查询语句。

3. 生成自然语言答案，执行SQL查询并获取数据后，系统会将这些结构化的数据转化为通俗易懂的自然语言回答用户。

4. 为新模板生成描述，系统会将新生成的SQL保存为模板，并为其生成简短的描述，方便以后精准匹配。
## 🛠️ 技术栈

**后端**：Python 3.10+ · FastAPI · SQLAlchemy · PyMilvus · OpenAI

**前端**：React 19 · TypeScript · Tailwind CSS · ECharts · Vite

**存储**：MySQL · Milvus


## 运行效果

### 📊 数据可视化展示
**首页**
![首页](images/index.png)

**饼图效果**：按月客户注册数量分布
![饼图效果](images/pie.png)

**折线图效果**：最近30天销售额趋势分析
![折线图效果](images/line.png)


## 📦 快速开始

### 🐳 Docker部署（推荐）

#### 1. 克隆项目
```bash
git clone https://github.com/sumingcheng/chat-bi.git
cd chat-bi
```

#### 2. 配置环境变量
复制并编辑环境配置文件：
```bash
cp .env-temp .env
```

编辑 `.env` 文件，配置必要参数：
```env
# 调试模式
DEBUG=False

DB_HOST=mysql
DB_PORT=3306
DB_USER=root
DB_PASSWORD=admin123456
DB_NAME=chat_bi
DB_SYS_NAME=chat_bi_system


MILVUS_HOST=milvus-standalone
MILVUS_PORT=19530


OPENAI_API_KEY=sk-

EMBEDDING_API_URL=http://172.19.221.125:11434/api/embeddings
EMBEDDING_MODEL=bge-m3
```

#### 3. 启动服务
```bash
# 进入根目录和 web 目录执行 
make build
# 回到根目录
make up 
```

### 💻 本地开发

#### 后端开发
```bash
# 安装依赖
uv sync

# 启动后端服务
python main.py
```

```bash
 # 启动成功显示
 ⚡ root@DESKTOP-AETE0Q9  /data/chat-bi   main  docker logs -f f341b3959a99
INFO:     Will watch for changes in these directories: ['/chat-bi']
INFO:     Uvicorn running on http://0.0.0.0:13000 (Press CTRL+C to quit)
INFO:     Started reloader process [1] using StatReload
INFO:     Started server process [8]
INFO:     Waiting for application startup.
2025-06-03 04:01:07 [INFO] app:57 - 🚀 应用启动中...
2025-06-03 04:01:07 [INFO] app:58 - 📊 开始检查数据库表状态...
2025-06-03 04:01:07 [INFO] app:39 - ✓ 业务数据库表 'category' 已存在
2025-06-03 04:01:07 [INFO] app:39 - ✓ 业务数据库表 'customer' 已存在
2025-06-03 04:01:07 [INFO] app:39 - ✓ 业务数据库表 'product' 已存在
2025-06-03 04:01:07 [INFO] app:39 - ✓ 业务数据库表 'sales_order' 已存在
2025-06-03 04:01:07 [INFO] app:39 - ✓ 业务数据库表 'order_item' 已存在
2025-06-03 04:01:07 [INFO] app:39 - ✓ 业务数据库表 'sales' 已存在
2025-06-03 04:01:07 [INFO] app:49 - ✓ 系统数据库表 'sql_templates' 已存在
2025-06-03 04:01:07 [INFO] app:49 - ✓ 系统数据库表 'sql_template_params' 已存在
2025-06-03 04:01:07 [INFO] app:49 - ✓ 系统数据库表 'query_history' 已存在
2025-06-03 04:01:07 [INFO] app:63 - 📊 开始初始化数据库表...
2025-06-03 04:01:07 [INFO] app:68 - 开始初始化业务数据库表: ['category', 'customer', 'product', 'sales_order', 'order_item', 'sales']
2025-06-03 04:01:07 [INFO] app:71 - 业务数据库表初始化完成
2025-06-03 04:01:07 [INFO] app:68 - 开始初始化系统数据库表: ['sql_templates', 'sql_template_params', 'query_history']
2025-06-03 04:01:07 [INFO] app:71 - 系统数据库表初始化完成
2025-06-03 04:01:07 [INFO] app:71 - ✅ 数据库表初始化完成
2025-06-03 04:01:07 [INFO] app:72 - 🎉 Chat-BI API 启动成功！
INFO:     Application startup complete.
```

#### 前端开发
```bash
cd web

# 安装依赖
pnpm install

# 启动开发服务器
pnpm run dev
```

## 🌐 访问地址

启动成功后，您可以访问：

- **前端**：http://localhost:8888
- **后端API文档**：http://localhost:13000/docs
- **Milvus管理界面**：http://localhost:19000

## 🧪 测试数据

项目提供了测试数据生成工具：

```bash
# 生成测试数据
python test/generate_test_data.py

# 运行测试查询
python test/run_test_data.py
```

## 🤝 贡献指南

我们欢迎所有形式的贡献！


- **作者**：[sumingcheng](https://github.com/sumingcheng)
- **邮箱**：通过GitHub Issues联系
- **项目主页**：https://github.com/sumingcheng/chat-bi
