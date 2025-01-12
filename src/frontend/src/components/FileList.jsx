import { useState, useEffect, useCallback } from 'react';
import { Box, Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';
import axios from 'axios';

function FileList({ processedFile }) {
  const [files, setFiles] = useState([]);
  const [lastUpdate, setLastUpdate] = useState(0);

  const fetchFiles = useCallback(async () => {
    try {
      const response = await axios.get('/files');
      setFiles(response.data);
      setLastUpdate(Date.now());
    } catch (error) {
      console.error('获取文件列表失败:', error);
    }
  }, []);

  // 初始加载和页面激活时获取文件列表
  useEffect(() => {
    fetchFiles();

    // 页面可见性变化监听
    const handleVisibilityChange = () => {
      if (document.visibilityState === 'visible') {
        const now = Date.now();
        // 如果距离上次更新超过10秒，则刷新列表
        if (now - lastUpdate > 10000) {
          fetchFiles();
        }
      }
    };

    document.addEventListener('visibilitychange', handleVisibilityChange);
    return () => {
      document.removeEventListener('visibilitychange', handleVisibilityChange);
    };
  }, [fetchFiles, lastUpdate]);

  // 当有新文件处理完成时立即刷新列表
  useEffect(() => {
    if (processedFile) {
      fetchFiles();
    }
  }, [processedFile, fetchFiles]);

  // 使用较长的轮询间隔来更新文件列表
  useEffect(() => {
    const intervalId = setInterval(fetchFiles, 30000); // 每30秒更新一次
    return () => clearInterval(intervalId);
  }, [fetchFiles]);

  const handleCleanup = async () => {
    if (window.confirm('确定要清理所有处理文件吗？')) {
      try {
        await axios.post('/cleanup');
        await fetchFiles();
      } catch (error) {
        alert('清理文件失败');
      }
    }
  };

  return (
    <Box>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>文件名</TableCell>
              <TableCell>大小</TableCell>
              <TableCell>处理时间</TableCell>
              <TableCell>操作</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {files.map((file) => (
              <TableRow 
                key={file.name}
                sx={{
                  backgroundColor: file.name === processedFile ? '#e3f2fd' : 'inherit',
                  transition: 'background-color 0.3s'
                }}
              >
                <TableCell sx={{ 
                  maxWidth: 300,
                  overflow: 'hidden',
                  textOverflow: 'ellipsis',
                  whiteSpace: 'nowrap'
                }}>
                  {decodeURIComponent(file.name)}
                </TableCell>
                <TableCell>{file.size}</TableCell>
                <TableCell>{file.time}</TableCell>
                <TableCell>
                  <Button 
                    href={`/download/${encodeURIComponent(file.name)}`}
                    variant="contained"
                    size="small"
                  >
                    下载
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      <Button 
        onClick={handleCleanup}
        variant="contained"
        color="error"
        sx={{ mt: 2 }}
      >
        清理文件
      </Button>
    </Box>
  );
}

export default FileList; 