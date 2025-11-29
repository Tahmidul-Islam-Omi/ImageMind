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
        border: '3px dashed rgba(255, 255, 255, 0.5)',
        borderRadius: 3,
        p: 6,
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
        <CircularProgress sx={{ color: 'white', mb: 2 }} size={60} />
      ) : (
        <CloudUploadIcon sx={{ fontSize: 80, color: 'white', mb: 2 }} />
      )}

      <Typography variant="h5" sx={{ color: 'white', fontWeight: 600, mb: 1 }}>
        {uploading ? 'Uploading...' : 'Drop your images here'}
      </Typography>

      <Typography variant="body1" sx={{ color: 'rgba(255, 255, 255, 0.8)', mb: 3 }}>
        or click to browse
      </Typography>

      <Button
        variant="contained"
        startIcon={<ImageIcon />}
        disabled={uploading}
        sx={{
          backgroundColor: 'white',
          color: '#667eea',
          px: 4,
          py: 1.5,
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
