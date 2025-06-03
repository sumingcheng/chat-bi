FROM python:3.10-slim

WORKDIR /chat-bi

# 处理中国镜像源构建参数
ARG USE_CHINA_MIRROR=false

# 安装 uv - 使用适合国内的安装方式
RUN if [ "$USE_CHINA_MIRROR" = "true" ]; then \
        # 方式1: 使用国内镜像源安装
        pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn uv; \
    else \
        # 方式2: 使用官方安装脚本（通常更稳定）
        curl -LsSf https://astral.sh/uv/install.sh | sh && \
        mv /root/.cargo/bin/uv /usr/local/bin/uv || \
        # 备选：如果curl失败，使用默认pip安装
        pip install --no-cache-dir uv; \
    fi

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
