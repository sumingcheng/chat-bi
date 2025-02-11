#!/bin/bash
#export HTTP_PROXY="http://172.22.220.64:7890"
#export HTTPS_PROXY="http://172.22.220.64:7890"
pip install torch==1.11.0+cpu -f https://download.pytorch.org/whl/torch_stable.html
pip install -r requirements.txt
pip install -r requirements-win.txt

# 安装 milvus-lite
pip install milvus-lite==2.4.10