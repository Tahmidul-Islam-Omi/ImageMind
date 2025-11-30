import { useState, useEffect } from 'react';
import { Box, Container, Typography, Paper, Snackbar, Alert } from '@mui/material';
import ImageUploadZone from './ImageUploadZone';
import ImageGallery from './ImageGallery';
import { uploadImage, fetchAllImages, deleteImage } from '../../services/imageService';

const ImageUploadContainer = () => {
  const [images, setImages] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [notification, setNotification] = useState({ open: false, message: '', severity: 'success' });

  // Load existing images on mount
  useEffect(() => {
    loadImages();
  }, []);

  const loadImages = async () => {
    const existingImages = await fetchAllImages();
    setImages(existingImages);
  };

  const handleImageUpload = async (files) => {
    setUploading(true);
    try {
      const uploadedImages = await uploadImage(files);
      setImages((prev) => [...uploadedImages, ...prev]);
      setNotification({
        open: true,
        message: `Successfully uploaded ${uploadedImages.length} image(s)`,
        severity: 'success',
      });
    } catch (error) {
      console.error('Upload failed:', error);
      setNotification({
        open: true,
        message: error.message || 'Upload failed',
        severity: 'error',
      });
    } finally {
      setUploading(false);
    }
  };

  const handleRemoveImage = async (imageId) => {
    try {
      await deleteImage(imageId);
      setImages((prev) => prev.filter((img) => img.id !== imageId));
      setNotification({
        open: true,
        message: 'Image deleted successfully',
        severity: 'success',
      });
    } catch (error) {
      console.error('Delete failed:', error);
      setNotification({
        open: true,
        message: error.message || 'Delete failed',
        severity: 'error',
      });
    }
  };

  return (
    <Container maxWidth="lg" sx={{ py: 6 }}>
      <Box sx={{ textAlign: 'center', mb: 6 }}>
        <Typography
          variant="h3"
          component="h1"
          gutterBottom
          sx={{
            fontWeight: 700,
            background: 'linear-gradient(45deg, #667eea 30%, #764ba2 90%)',
            backgroundClip: 'text',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
          }}
        >
          Image Upload Gallery
        </Typography>
        <Typography variant="h6" color="text.secondary" sx={{ mb: 4 }}>
          Upload and manage your beautiful images
        </Typography>
      </Box>

      <Paper
        elevation={3}
        sx={{
          p: 3,
          mb: 4,
          borderRadius: 3,
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        }}
      >
        <ImageUploadZone onUpload={handleImageUpload} uploading={uploading} />
      </Paper>

      <ImageGallery images={images} onRemove={handleRemoveImage} />

      <Snackbar
        open={notification.open}
        autoHideDuration={4000}
        onClose={() => setNotification({ ...notification, open: false })}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      >
        <Alert
          onClose={() => setNotification({ ...notification, open: false })}
          severity={notification.severity}
          sx={{ width: '100%' }}
        >
          {notification.message}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default ImageUploadContainer;
