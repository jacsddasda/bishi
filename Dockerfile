# 使用Python 3.8作为基础镜像
FROM python:3.8-slim

# 设置工作目录
WORKDIR /app

# 复制backend目录到容器中
COPY backend/ /app/

# 复制frontend目录到容器中
COPY frontend/ /app/frontend/

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露端口
EXPOSE 5000

# 启动应用
CMD ["python", "run.py"]