import { useState, useCallback } from 'react';
import { Box, Button, Typography, CircularProgress, Stack } from '@mui/material';
import axios from 'axios';

function FileUpload({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [processedFile, setProcessedFile] = useState(null);

  const handleFileChange = useCallback((event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile && selectedFile.type === 'application/pdf') {
      setFile(selectedFile);
      setProcessedFile(null);
    } else {
      alert('请选择PDF文件');
    }
  }, []);

  const handleUpload = useCallback(async () => {
    if (!file) return;
    
    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('/upload', formData);
      const processedFileName = response.data.processed_file;
      setProcessedFile(processedFileName);
      onUploadSuccess(processedFileName);
      
      setFile(null);
      const fileInput = document.getElementById('file-input');
      if (fileInput) {
        fileInput.value = '';
      }
    } catch (error) {
      alert('上传失败：' + (error.response?.data?.error || error.message));
    } finally {
      setUploading(false);
    }
  }, [file, onUploadSuccess]);

  return (
    <Box sx={{ textAlign: 'center', mb: 4 }}>
      <Stack 
        direction="row" 
        spacing={2} 
        justifyContent="center" 
        alignItems="center"
      >
        <input
          type="file"
          accept=".pdf"
          onChange={handleFileChange}
          style={{ display: 'none' }}
          id="file-input"
        />
        <label htmlFor="file-input">
          <Button 
            variant="contained" 
            component="span"
            disabled={uploading}
          >
            选择文件
          </Button>
        </label>

        <Button
          variant="contained"
          onClick={handleUpload}
          disabled={!file || uploading}
        >
          {uploading ? <CircularProgress size={24} /> : '上传'}
        </Button>
      </Stack>

      {file && (
        <Typography sx={{ mt: 2 }}>
          已选择: {file.name}
        </Typography>
      )}

      {processedFile && !uploading && (
        <Typography sx={{ mt: 2, color: 'success.main' }}>
          文件已处理完成：{processedFile}
        </Typography>
      )}
    </Box>
  );
}

export default FileUpload; 