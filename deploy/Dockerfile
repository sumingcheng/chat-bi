# 使用基础 Python 镜像
FROM python:3.10.13-slim as builder

# 可选：使用中国镜像源
ARG USE_CHINA_MIRROR=false
ENV PIP_ROOT_USER_ACTION=ignore

# 创建工作目录
WORKDIR /chat-bi

# 复制 requirements.txt 到工作目录
COPY requirements.txt .

# 配置 pip 使用中国镜像源（如果需要），并安装依赖项
RUN if [ "$USE_CHINA_MIRROR" = "true" ]; then \
        pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple; \
    fi && \
    pip install --upgrade pip && \
    pip install torch==1.11.0+cpu -f https://download.pytorch.org/whl/torch_stable.html && \
    pip install --no-cache-dir -r requirements.txt

# 使用多阶段构建，减小最终镜像体积
FROM python:3.10.13-slim
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY . /chat-bi
WORKDIR /chat-bi

# 开放端口
EXPOSE 13000

# 设置启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "13000", "--reload"]
