import { useState } from 'react';
import { Container, Typography, Box, Grid, Paper } from '@mui/material';
import FileUpload from './components/FileUpload';
import FileList from './components/FileList';
import Instructions from './components/Instructions';

function App() {
  const [processedFile, setProcessedFile] = useState(null);

  const handleUploadSuccess = (filename) => {
    setProcessedFile(filename);
  };

  return (
    <Container maxWidth="xl">
      <Box sx={{ 
        py: 4,
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column'
      }}>
        <Typography 
          variant="h3" 
          component="h1" 
          gutterBottom 
          align="center"
          sx={{ 
            mb: 4,
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
        
        <Grid container spacing={3} sx={{ flex: 1 }}>
          {/* 左侧主要操作区域 */}
          <Grid item xs={12} md={8}>
            <Paper 
              elevation={3} 
              sx={{ 
                p: 3, 
                mb: 3,
                minHeight: '200px',
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
                minHeight: '400px',
                background: 'linear-gradient(to bottom, #ffffff, #f8f9fa)',
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
          </Grid>

          {/* 右侧使用说明 */}
          <Grid item xs={12} md={4}>
            <Paper 
              elevation={3} 
              sx={{ 
                p: 3,
                position: { md: 'sticky' },
                top: { md: 24 },
                background: 'linear-gradient(to bottom, #ffffff, #f8f9fa)',
                borderRadius: 2,
                minHeight: '633px' // 与左侧两个Paper的总高度相匹配
              }}
            >
              <Instructions />
            </Paper>
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
}

export default App;
