FROM python:3.10-slim

WORKDIR /chat-bi

# 安装 uv
RUN pip install --no-cache-dir uv

# 复制依赖文件
COPY pyproject.toml uv.lock ./

# 使用 uv 同步依赖
RUN uv sync

# 设置环境变量，将 .venv/bin 添加到 PATH
ENV PATH="/chat-bi/.venv/bin:${PATH}"

# 复制项目文件
COPY . .

EXPOSE 13000

CMD ["python", "main.py"]
