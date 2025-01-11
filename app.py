from flask import Flask, request, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import os
from main import process_single_pdf  # 假设你的主处理函数在main.py中

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

# 确保上传和处理后的文件夹存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)