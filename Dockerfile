# 使用 Node.js 镜像构建前端
FROM node:18-alpine as frontend-builder

# 设置工作目录
WORKDIR /frontend

# 复制前端项目文件
COPY src/frontend/package*.json ./
COPY src/frontend/vite.config.js ./
COPY src/frontend/index.html ./
COPY src/frontend/src ./src

# 清理 node_modules 和构建目录（确保清理旧的构建文件）
RUN rm -rf node_modules dist

# 安装依赖并构建
RUN npm install
RUN npm run build

# 验证构建产物
RUN ls -la dist && \
    cat dist/index.html

# 使用 Python 镜像作为最终镜像
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

# 创建前端静态文件目录并确保为空
RUN mkdir -p /app/static_frontend && \
    rm -rf /app/static_frontend/*

# 从前端构建阶段复制构建产物到前端静态文件目录
COPY --from=frontend-builder /frontend/dist /app/static_frontend

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露 Flask 应用的端口
EXPOSE 5000

# 验证静态文件是否正确复制
RUN ls -la /app/static_frontend && \
    test -f /app/static_frontend/index.html || exit 1

# 运行 Flask 应用
CMD ["python", "app.py"]