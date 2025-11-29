import { Box, Typography } from '@mui/material';
import ImageCard from './ImageCard';

const ImageGallery = ({ images, onRemove }) => {
  if (images.length === 0) {
    return (
      <Box sx={{ textAlign: 'center', py: 8 }}>
        <Typography variant="h6" color="text.secondary">
          No images uploaded yet. Start by uploading some beautiful images!
        </Typography>
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h5" sx={{ mb: 3, fontWeight: 600 }}>
        Your Gallery ({images.length})
      </Typography>
      <Box
        sx={{
          display: 'grid',
          gridTemplateColumns: {
            xs: 'repeat(1, 1fr)',
            sm: 'repeat(2, 1fr)',
            md: 'repeat(3, 1fr)',
            lg: 'repeat(4, 1fr)',
          },
          gap: 3,
        }}
      >
        {images.map((image) => (
          <ImageCard key={image.id} image={image} onRemove={onRemove} />
        ))}
      </Box>
    </Box>
  );
};

export default ImageGallery;
