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

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

# 确保上传和处理后的文件夹存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)
os.makedirs('static/js', exist_ok=True)

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        try:
            # 获取原始文件名并解码
            original_filename = urllib.parse.unquote(file.filename)
            if isinstance(original_filename, bytes):
                original_filename = original_filename.decode('utf-8')
            
            # 使用安全的文件名处理函数
            safe_filename = secure_chinese_filename(original_filename)
            
            # 移除扩展名
            original_name = os.path.splitext(safe_filename)[0]
            
            # 修改时间戳格式，使文件名更简洁
            timestamp = (datetime.now() + timedelta(hours=8)).strftime('%m%d_%H%M')
            filename = f"{original_name}_{timestamp}.pdf"
            
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            processed_pdf = process_single_pdf(file_path, app.config['PROCESSED_FOLDER'])
            processed_filename = os.path.basename(processed_pdf)
            
            return jsonify({'processed_file': processed_filename}), 200
            
        except Exception as e:
            print(f"处理文件时出错: {str(e)}")
            return jsonify({'error': f'处理文件时出错: {str(e)}'}), 500

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