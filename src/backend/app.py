from flask import Flask, request, send_from_directory, jsonify, render_template
from werkzeug.utils import secure_filename
import os
from main import process_single_pdf  # 假设你的主处理函数在main.py中
import shutil
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import urllib.parse
from flask_cors import CORS
import re
import logging
from logging.handlers import RotatingFileHandler

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('pdf_processor')
logger.setLevel(logging.INFO)

# 创建日志目录
os.makedirs('logs', exist_ok=True)

# 创建文件处理器
file_handler = RotatingFileHandler(
    'logs/app.log',
    maxBytes=1024 * 1024,  # 1MB
    backupCount=10,
    encoding='utf-8'
)

# 设置日志格式
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

app = Flask(__name__, 
    static_folder='static_frontend',
    static_url_path='/'
)
CORS(app)
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

# 确保上传和处理后的文件夹存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def secure_chinese_filename(filename):
    """安全的文件名处理，保留中文字符"""
    # 分离文件名和扩展名
    name, ext = os.path.splitext(filename)
    
    # 只保留中文、英文、数字和一些基本符号
    allowed_chars = re.compile(r'[^\u4e00-\u9fa5a-zA-Z0-9-_.]')
    clean_name = allowed_chars.sub('', name)
    
    # 处理文件名为空的情况
    if not clean_name:
        clean_name = 'unnamed'
        
    # 限制文件名长度
    if len(clean_name) > 200:
        clean_name = clean_name[:200]
        
    return clean_name + ext

# 在每个请求之前记录请求信息
@app.before_request
def log_request_info():
    logger.info('Headers: %s', dict(request.headers))
    logger.info('Path: %s', request.path)
    logger.info('Method: %s', request.method)

# 修改错误处理
@app.errorhandler(Exception)
def handle_exception(e):
    logger.error('未处理的异常: %s', str(e), exc_info=True)
    return jsonify({'error': str(e)}), 500

# 静态文件路由
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        logger.error('没有文件部分')
        return jsonify({'error': '没有文件部分'}), 400
    
    file = request.files['file']
    if file.filename == '':
        logger.error('没有选择文件')
        return jsonify({'error': '没有选择文件'}), 400
    
    if file:
        try:
            original_filename = urllib.parse.unquote(file.filename)
            logger.info('处理文件: %s', original_filename)
            
            safe_filename = secure_chinese_filename(original_filename)
            original_name = os.path.splitext(safe_filename)[0]
            timestamp = datetime.now().strftime('%m%d_%H%M')
            filename = f"{original_name}_{timestamp}.pdf"
            
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            logger.info('文件已保存: %s', file_path)
            
            processed_pdf = process_single_pdf(file_path, app.config['PROCESSED_FOLDER'])
            logger.info('文件处理完成: %s', processed_pdf)
            
            return jsonify({'processed_file': processed_pdf}), 200
            
        except Exception as e:
            logger.error('处理文件时出错', exc_info=True)
            return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    # 解码文件名
    decoded_filename = urllib.parse.unquote(filename)
    return send_from_directory(
        app.config['PROCESSED_FOLDER'], 
        decoded_filename,
        as_attachment=True,
        download_name=decoded_filename
    )

@app.route('/cleanup', methods=['POST'])
def cleanup():
    try:
        # 清理 uploads 目录
        for file in os.listdir(app.config['UPLOAD_FOLDER']):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file)
            if os.path.isfile(file_path):
                os.remove(file_path)
                
        # 清理 processed 目录
        for file in os.listdir(app.config['PROCESSED_FOLDER']):
            file_path = os.path.join(app.config['PROCESSED_FOLDER'], file)
            if os.path.isfile(file_path):
                os.remove(file_path)
                
        # 清理临时工作目录
        for dir_name in os.listdir():
            if dir_name.startswith('work_'):
                shutil.rmtree(dir_name)
                
        return jsonify({'message': '清理完成'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def cleanup_old_files():
    # 清理超过24小时的文件
    cutoff_time = datetime.now() - timedelta(hours=24)
    
    for folder in [app.config['UPLOAD_FOLDER'], app.config['PROCESSED_FOLDER']]:
        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            if os.path.isfile(file_path):
                file_time = datetime.fromtimestamp(os.path.getctime(file_path))
                if file_time < cutoff_time:
                    os.remove(file_path)
    
    # 清理临时工作目录
    for dir_name in os.listdir():
        if dir_name.startswith('work_'):
            dir_path = os.path.join(os.getcwd(), dir_name)
            dir_time = datetime.fromtimestamp(os.path.getctime(dir_path))
            if dir_time < cutoff_time:
                shutil.rmtree(dir_path)

# 创建定时任务
scheduler = BackgroundScheduler()
scheduler.add_job(func=cleanup_old_files, trigger="interval", hours=24)
scheduler.start()

@app.route('/files', methods=['GET'])
def list_files():
    processed_files = []
    for file in os.listdir(app.config['PROCESSED_FOLDER']):
        if file.endswith('.pdf'):
            file_path = os.path.join(app.config['PROCESSED_FOLDER'], file)
            file_size = os.path.getsize(file_path) / 1024  # 转换为 KB
            file_time = os.path.getctime(file_path)
            processed_files.append({
                'name': file,
                'size': f"{file_size:.1f} KB",
                'time': datetime.fromtimestamp(file_time).strftime('%Y-%m-%d %H:%M:%S')
            })
    return jsonify(processed_files)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)