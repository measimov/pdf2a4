import { Box, Typography, List, ListItem, ListItemIcon, ListItemText, Paper } from '@mui/material';
import FileUploadIcon from '@mui/icons-material/FileUpload';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import TimerIcon from '@mui/icons-material/Timer';
import DownloadIcon from '@mui/icons-material/Download';
import WarningIcon from '@mui/icons-material/Warning';

function Instructions() {
  return (
    <Box>
      <Typography 
        variant="h5" 
        gutterBottom 
        sx={{ 
          color: '#1976d2',
          fontWeight: 500,
          mb: 3 
        }}
      >
        使用说明
      </Typography>

      <List sx={{ mb: 4 }}>
        <ListItem>
          <ListItemIcon>
            <FileUploadIcon color="primary" />
          </ListItemIcon>
          <ListItemText 
            primary="选择文件"
            primaryTypographyProps={{
              fontWeight: 500,
              color: '#1976d2',
              fontSize: '1.1rem'
            }}
            secondary={'点击"选择文件"按钮，选择需要处理的PDF文件'}
          />
        </ListItem>
        <ListItem>
          <ListItemIcon>
            <CheckCircleIcon color="primary" />
          </ListItemIcon>
          <ListItemText 
            primary="确认上传"
            primaryTypographyProps={{
              fontWeight: 500,
              color: '#1976d2',
              fontSize: '1.1rem'
            }}
            secondary={'选择文件后，点击"上传"按钮开始处理'}
          />
        </ListItem>
        <ListItem>
          <ListItemIcon>
            <TimerIcon color="primary" />
          </ListItemIcon>
          <ListItemText 
            primary="等待处理"
            primaryTypographyProps={{
              fontWeight: 500,
              color: '#1976d2',
              fontSize: '1.1rem'
            }}
            secondary="系统会自动处理您的文件，请耐心等待"
          />
        </ListItem>
        <ListItem>
          <ListItemIcon>
            <DownloadIcon color="primary" />
          </ListItemIcon>
          <ListItemText 
            primary="下载文件"
            primaryTypographyProps={{
              fontWeight: 500,
              color: '#1976d2',
              fontSize: '1.1rem'
            }}
            secondary={'处理完成后，点击"下载"按钮获取处理后的文件'}
          />
        </ListItem>
      </List>

      <Paper 
        elevation={2} 
        sx={{ 
          p: 2, 
          bgcolor: '#fff3cd',
          borderRadius: 2
        }}
      >
        <Typography 
          variant="h6" 
          gutterBottom 
          sx={{ 
            color: '#664d03',
            display: 'flex',
            alignItems: 'center',
            gap: 1
          }}
        >
          <WarningIcon /> 注意事项
        </Typography>
        <List dense>
          <ListItem>
            <ListItemText primary="• 仅支持PDF格式文件" />
          </ListItem>
          <ListItem>
            <ListItemText primary="• 建议文件大小不超过20MB" />
          </ListItem>
          <ListItem>
            <ListItemText primary="• 处理后的文件将在24小时后自动清理" />
          </ListItem>
        </List>
      </Paper>
    </Box>
  );
}

export default Instructions; 