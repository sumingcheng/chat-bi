FROM python:3.10.13-slim

# 可选：使用中国镜像源
ARG USE_CHINA_MIRROR=false
ENV PIP_ROOT_USER_ACTION=ignore
WORKDIR /app

# 复制requirements.txt到工作目录
COPY requirements.txt .

# 如果需要，配置pip使用中国镜像源，并安装依赖
RUN if [ "$USE_CHINA_MIRROR" = "true" ] ; then \
        pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple ; \
    fi && \
    pip install --upgrade pip && \
    pip install torch==1.11.0+cpu -f https://download.pytorch.org/whl/torch_stable.html && \
    pip install --no-cache-dir -r requirements.txt

# 复制项目文件到容器
COPY . .

EXPOSE 13000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "13000", "--reload"]
