// 文件输入处理
const fileInput = document.getElementById('fileInput');
const fileName = document.getElementById('fileName');

fileInput.addEventListener('change', function() {
    fileName.textContent = fileInput.files.length > 0 ? fileInput.files[0].name : '未选择文件';
});

// 文件上传处理
document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();
    if (fileInput.files.length === 0) {
        alert('请选择一个文件。');
        return;
    }
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    document.getElementById('status').classList.remove('hidden');
    document.getElementById('download').classList.add('hidden');

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('网络响应失败');
        }
        return response.json();
    })
    .then(data => {
        document.getElementById('status').classList.add('hidden');
        if (data.processed_file) {
            const downloadLink = document.getElementById('downloadLink');
            downloadLink.href = `/download/${data.processed_file}`;
            document.getElementById('download').classList.remove('hidden');
            updateFileList();
        } else {
            alert('文件处理出错。');
        }
    })
    .catch(error => {
        document.getElementById('status').classList.add('hidden');
        alert('文件上传出错：' + error.message);
    });
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
function updateFileList() {
    fetch('/files')
        .then(response => response.json())
        .then(files => {
            const tbody = document.querySelector('#filesTable tbody');
            tbody.innerHTML = '';
            
            files.forEach(file => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${file.name}</td>
                    <td>${file.size}</td>
                    <td>${file.time}</td>
                    <td>
                        <a href="/download/${file.name}" class="file-action">下载</a>
                    </td>
                `;
                tbody.appendChild(tr);
            });
            
            document.getElementById('fileList').classList.remove('hidden');
        })
        .catch(error => {
            console.error('获取文件列表失败:', error);
        });
}

// 页面加载时获取文件列表
document.addEventListener('DOMContentLoaded', updateFileList); 