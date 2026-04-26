# Chat-BI

[中文版本](README.zh-CN.md)

Chat-BI is a natural-language analytics assistant that turns business questions into SQL, executes them against your database, and returns structured answers with charts and tables.

## Highlights

- Natural-language to SQL workflow backed by schema understanding and reusable SQL templates
- FastAPI backend with MySQL + Milvus integration
- Configurable LLM and embedding providers
- Modern React frontend with conversation history, i18n, and light/dark theme switching
- Local-first development flow using `uv` for Python and `pnpm` for the web app

## Architecture

```text
Frontend (React + TypeScript + Vite)
    ->
Backend API (FastAPI)
    ->
Business DB (MySQL) + System DB (MySQL)
    ->
Vector Store (Milvus)
    ->
LLM / Embedding Providers (OpenAI, DeepSeek, Ollama)
```

## How It Works

1. The user asks a question in natural language.
2. The system embeds the question and searches for matching SQL templates.
3. If no good template exists, the backend generates SQL from schema context.
4. The query runs against the business database with basic safety guards.
5. The result is returned as natural-language text plus a chart/table payload.
6. Newly generated templates can be stored for better future matching.

## Tech Stack

- Backend: Python 3.10+, FastAPI, SQLAlchemy, PyMilvus, OpenAI SDK
- Frontend: React 19, TypeScript, Tailwind CSS, Zustand, ECharts, Vite
- Storage: MySQL, Milvus
- Package managers: `uv` (Python), `pnpm` (web)

## Screenshots

<img width="3828" height="2113" alt="image" src="https://github.com/user-attachments/assets/1d4ebe28-03e0-4a38-8934-4a0e582db487" />


## Configuration

The backend now uses a YAML-first configuration model.

1. Copy the example file:

```bash
cp config.example.yaml config.yaml
```

2. Edit `config.yaml` and fill in the values you need:

```yaml
debug: false

database:
  host: localhost
  port: 3306
  user: root
  password: admin123456
  name: chat_bi
  sys_name: chat_bi_system

milvus:
  host: localhost
  port: 19530

llm:
  provider: openai
  model: gpt-4.1
  api_key: your_api_key_here
  base_url: ""

embedding:
  provider: openai
  model: text-embedding-3-small
  dim: 1536
  api_key: ""
  api_url: ""
```

Environment variables can still override YAML values when needed.

## Quick Start

### Option A: Local Development

#### Backend

```bash
uv sync
uv run python main.py
```

The API will be available at `http://localhost:13000`.

#### Frontend

```bash
cd web
pnpm install
pnpm dev
```

The web app will be available at `http://localhost:5173`.

### Option B: Start Only Local Infrastructure

If you want MySQL + Milvus locally and run the app processes on your host machine:

```bash
cd deploy
docker-compose -f docker-compose-base.yaml up -d
```

This brings up:

- MySQL: `localhost:3306`
- Milvus: `localhost:19530`
- Attu: `http://localhost:19000`

### Option C: Full Docker Stack

The repository also includes a full deployment flow:

```bash
make build
make up
```

Notes:

- The compose files live under `deploy/`.
- The current backend runtime is YAML-first, but the provided deployment stack may still rely on environment-based wiring depending on how you deploy it.
- For active development, local development with `config.yaml` is the most straightforward path.

## Useful URLs

- Frontend: `http://localhost:5173`
- Backend API docs: `http://localhost:13000/docs`
- Milvus Attu: `http://localhost:19000`

## Example Questions

- What can I query right now?
- Show the daily sales trend for the last 30 days.
- What are the top 10 products by sales volume?
- Show the sales share by product category.
- Which products have inventory below 10?

## Test Data

```bash
python test/generate_test_data.py
python test/run_test_data.py
```

## Contributing

Issues and pull requests are welcome.

- Author: [sumingcheng](https://github.com/sumingcheng)
- Repository: https://github.com/sumingcheng/chat-bi
