import { useRef } from 'react';
import { Box, Button, Typography, CircularProgress } from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import ImageIcon from '@mui/icons-material/Image';

const ImageUploadZone = ({ onUpload, uploading }) => {
  const fileInputRef = useRef(null);

  const handleFileSelect = (event) => {
    const files = Array.from(event.target.files);
    if (files.length > 0) {
      onUpload(files);
    }
  };

  const handleDrop = (event) => {
    event.preventDefault();
    const files = Array.from(event.dataTransfer.files);
    const imageFiles = files.filter((file) => file.type.startsWith('image/'));
    if (imageFiles.length > 0) {
      onUpload(imageFiles);
    }
  };

  const handleDragOver = (event) => {
    event.preventDefault();
  };

  const handleBoxClick = () => {
    if (fileInputRef.current !== null && fileInputRef.current !== undefined) {
      fileInputRef.current.click();
    }
  };

  return (
    <Box
      onDrop={handleDrop}
      onDragOver={handleDragOver}
      sx={{
        border: '2px dashed rgba(255, 255, 255, 0.5)',
        borderRadius: 2,
        p: 3,
        textAlign: 'center',
        backgroundColor: 'rgba(255, 255, 255, 0.1)',
        backdropFilter: 'blur(10px)',
        transition: 'all 0.3s ease',
        cursor: 'pointer',
        '&:hover': {
          borderColor: 'rgba(255, 255, 255, 0.8)',
          backgroundColor: 'rgba(255, 255, 255, 0.15)',
          transform: 'translateY(-2px)',
        },
      }}
      onClick={handleBoxClick}
    >
      <input
        ref={fileInputRef}
        type="file"
        multiple
        accept="image/*"
        onChange={handleFileSelect}
        style={{ display: 'none' }}
      />

      {uploading ? (
        <CircularProgress sx={{ color: 'white', mb: 1.5 }} size={40} />
      ) : (
        <CloudUploadIcon sx={{ fontSize: 50, color: 'white', mb: 1.5 }} />
      )}

      <Typography variant="h6" sx={{ color: 'white', fontWeight: 600, mb: 0.5 }}>
        {uploading ? 'Uploading...' : 'Drop your images here'}
      </Typography>

      <Typography variant="body2" sx={{ color: 'rgba(255, 255, 255, 0.8)', mb: 2 }}>
        or click to browse
      </Typography>

      <Button
        variant="contained"
        startIcon={<ImageIcon />}
        disabled={uploading}
        size="small"
        sx={{
          backgroundColor: 'white',
          color: '#667eea',
          px: 3,
          py: 1,
          fontWeight: 600,
          '&:hover': {
            backgroundColor: 'rgba(255, 255, 255, 0.9)',
          },
        }}
      >
        Select Images
      </Button>
    </Box>
  );
};

export default ImageUploadZone;
