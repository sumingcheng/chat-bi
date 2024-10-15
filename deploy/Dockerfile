FROM continuumio/miniconda3:4.12.0 AS builder

WORKDIR /app

# Optional use of a mirror for China
ARG USE_CHINA_MIRROR=false
COPY environment.yml /app/environment.yml

RUN if [ "$USE_CHINA_MIRROR" = "true" ] ; then \
      conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main && \
      conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free && \
      conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge && \
      conda config --set show_channel_urls yes ; \
    fi && \
    conda env create -f /app/environment.yml && \
    conda clean -a && \
    find /opt/conda/ -follow -type f -name '*.a' -delete && \
    find /opt/conda/ -follow -type f -name '*.pyc' -delete && \
    find /opt/conda/ -follow -type f -name '*.js.map' -delete && \
    rm -rf /opt/conda/pkgs/*

FROM continuumio/miniconda3:4.12.0
#ENV PYTHONDONTWRITEBYTECODE=1
COPY --from=builder /opt/conda /opt/conda

WORKDIR /app
COPY . .

EXPOSE 8000

ENTRYPOINT ["conda", "run", "-n", "minio-upload", "--no-capture-output"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
