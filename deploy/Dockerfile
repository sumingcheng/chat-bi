FROM python:3.10-slim

WORKDIR /chat-bi

# 处理中国镜像源构建参数
ARG USE_CHINA_MIRROR=false
# 安装 uv
RUN pip install --no-cache-dir uv

# 配置 uv 镜像源
RUN if [ "$USE_CHINA_MIRROR" = "true" ]; then \
        uv config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
        uv config set global.trusted-host pypi.tuna.tsinghua.edu.cn; \
    fi

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
