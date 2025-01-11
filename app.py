from flask import Flask, request, send_from_directory, jsonify, render_template
from werkzeug.utils import secure_filename
import os
from main import process_single_pdf  # 假设你的主处理函数在main.py中
import shutil
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

# 确保上传和处理后的文件夹存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)
os.makedirs('static/js', exist_ok=True)

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
        # 使用UNIX时间戳作为文件名
        import time
        timestamp = str(int(time.time()))
        filename = f"{timestamp}.pdf"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        print(f"文件已保存到: {file_path}")
        processed_pdf = process_single_pdf(file_path, app.config['PROCESSED_FOLDER'])
        processed_filename = os.path.basename(processed_pdf)
        print(f"处理后的文件已保存到: {processed_filename}")
        return jsonify({'processed_file': processed_filename}), 200

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename)

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