import { useState } from 'react';
import { Typography, Box, Paper } from '@mui/material';
import FileUpload from './components/FileUpload';
import FileList from './components/FileList';
import Instructions from './components/Instructions';

function App() {
  const [processedFile, setProcessedFile] = useState(null);

  const handleUploadSuccess = (filename) => {
    setProcessedFile(filename);
  };

  return (
    <Box sx={{ 
      display: 'flex',
      minHeight: '100vh',
      minWidth: '100vw',
      margin: 0,
      padding: 0,
    }}>
      {/* 左侧主要内容区域 */}
      <Box sx={{ 
        flex: '0 0 66.67%',
        display: 'flex',
        flexDirection: 'column',
        bgcolor: '#f5f5f5',
      }}>
        <Typography 
          variant="h3" 
          component="h1" 
          gutterBottom 
          align="center"
          sx={{ 
            py: 3,
            fontWeight: 'bold',
            background: 'linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)',
            backgroundClip: 'text',
            textFillColor: 'transparent',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
          }}
        >
          PDF试卷分割工具
        </Typography>

        <Box sx={{ 
          flex: 1, 
          display: 'flex', 
          flexDirection: 'column',
          gap: 2,
          p: 3,
        }}>
          <Paper 
            elevation={3} 
            sx={{ 
              p: 3,
              background: 'linear-gradient(to bottom, #ffffff, #f8f9fa)',
              borderRadius: 2,
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'center'
            }}
          >
            <FileUpload onUploadSuccess={handleUploadSuccess} />
          </Paper>
          
          <Paper 
            elevation={3} 
            sx={{ 
              p: 3,
              flex: 1,
              background: 'linear-gradient(to bottom, #ffffff 0%, #f5f7fa 100%)',
              borderRadius: 2,
              display: 'flex',
              flexDirection: 'column'
            }}
          >
            <Typography 
              variant="h5" 
              gutterBottom 
              sx={{ 
                mb: 3,
                fontWeight: 500,
                color: '#1976d2'
              }}
            >
              处理文件列表
            </Typography>
            <Box sx={{ flex: 1 }}>
              <FileList processedFile={processedFile} />
            </Box>
          </Paper>
        </Box>
      </Box>

      {/* 右侧使用说明 */}
      <Box sx={{ 
        flex: '0 0 30%',
        bgcolor: '#fff',
        borderLeft: '1px solid #e0e0e0',
        height: '100vh',
        overflowY: 'auto',
        p: 3,
      }}>
        <Instructions />
      </Box>
    </Box>
  );
}

export default App;
