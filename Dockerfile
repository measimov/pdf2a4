# 使用Python官方镜像
FROM python:3.9-slim

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-chi-sim \
    tesseract-ocr-eng \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制后端代码到容器中
COPY src/backend /app

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露Flask应用的端口
EXPOSE 5000

# 运行Flask应用
CMD ["python", "app.py"]