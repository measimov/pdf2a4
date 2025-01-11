// 定义API基础URL
const API_BASE_URL = window.location.origin;  // 自动获取当前域名和端口

// 文件输入处理
const fileInput = document.getElementById('fileInput');
const fileName = document.getElementById('fileName');
const uploadButton = document.getElementById('uploadButton');

fileInput.addEventListener('change', function() {
    const hasFile = fileInput.files.length > 0;
    fileName.textContent = hasFile ? fileInput.files[0].name : '未选择文件';
    uploadButton.disabled = !hasFile;
});

// 文件上传处理
document.getElementById('uploadForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    if (fileInput.files.length === 0) {
        alert('请选择一个文件。');
        return;
    }
    const formData = new FormData();
    const file = fileInput.files[0];
    
    formData.append('file', file, file.name);
    
    document.getElementById('status').classList.remove('hidden');
    document.getElementById('download').classList.add('hidden');

    try {
        const response = await fetch(`${API_BASE_URL}/upload`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('网络响应失败');
        }

        const data = await response.json();
        document.getElementById('status').classList.add('hidden');

        if (data.processed_file) {
            const downloadLink = document.getElementById('downloadLink');
            const decodedFileName = decodeURIComponent(data.processed_file);
            downloadLink.href = `/download/${encodeURIComponent(data.processed_file)}`;
            downloadLink.textContent = `下载处理后的文件: ${decodedFileName}`;
            document.getElementById('download').classList.remove('hidden');
            
            // 等待一小段时间确保文件已完全写入
            await new Promise(resolve => setTimeout(resolve, 1000));
            
            // 更新文件列表
            await updateFileList();
            
            // 清空文件输入
            fileInput.value = '';
            fileName.textContent = '未选择文件';
        } else {
            alert('文件处理出错。');
        }
    } catch (error) {
        document.getElementById('status').classList.add('hidden');
        alert('文件上传出错：' + error.message);
    }
});

// 清理文件处理
document.getElementById('cleanupBtn').addEventListener('click', function() {
    if (confirm('确定要清理所有处理文件吗？')) {
        fetch('/cleanup', {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            alert('文件清理完成');
            updateFileList();
            document.getElementById('download').classList.add('hidden');
        })
        .catch(error => {
            alert('清理过程出错：' + error.message);
        });
    }
});

// 更新文件列表
async function updateFileList() {
    try {
        const response = await fetch('/files');
        const files = await response.json();
        
        const tbody = document.querySelector('#filesTable tbody');
        tbody.innerHTML = '';
        
        files.forEach(file => {
            const tr = document.createElement('tr');
            const decodedFileName = decodeURIComponent(file.name);
            tr.innerHTML = `
                <td>${decodedFileName}</td>
                <td>${file.size}</td>
                <td>${file.time}</td>
                <td>
                    <a href="/download/${encodeURIComponent(file.name)}" class="file-action">下载</a>
                </td>
            `;
            tbody.appendChild(tr);
        });
        
        document.getElementById('fileList').classList.remove('hidden');
    } catch (error) {
        console.error('获取文件列表失败:', error);
    }
}

// 页面加载时获取文件列表
document.addEventListener('DOMContentLoaded', updateFileList); 