import { useState } from 'react';
import {
  Card,
  CardActions,
  IconButton,
  Box,
  Typography,
  Fade,
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import DownloadIcon from '@mui/icons-material/Download';
import ZoomInIcon from '@mui/icons-material/ZoomIn';
import { downloadFile } from '../../utils/downloadHelper';

const ImageCard = ({ image, onRemove }) => {
  const [hover, setHover] = useState(false);

  const handleDownload = async (event) => {
    event.stopPropagation();
    event.preventDefault();
    
    const success = await downloadFile(image.url, image.name);
    if (!success) {
      console.error('Failed to download:', image.name);
    }
  };

  const handleDelete = (event) => {
    event.stopPropagation();
    event.preventDefault();
    onRemove(image.id);
  };

  const handleZoom = (event) => {
    event.stopPropagation();
    event.preventDefault();
    window.open(image.url, '_blank');
  };

  return (
    <Card
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      sx={{
        position: 'relative',
        borderRadius: 3,
        overflow: 'hidden',
        transition: 'all 0.3s ease',
        '&:hover': {
          transform: 'translateY(-8px)',
          boxShadow: '0 12px 24px rgba(0,0,0,0.15)',
        },
      }}
    >
      <Box sx={{ position: 'relative', paddingTop: '100%', backgroundColor: '#f0f0f0' }}>
        <img
          src={image.url}
          alt={image.name}
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            objectFit: 'cover',
          }}
          onError={() => console.error('Failed to load image:', image.name)}
        />

        <Fade in={hover}>
          <Box
            sx={{
              position: 'absolute',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              background: 'linear-gradient(to bottom, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0.3) 100%)',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
              p: 2,
            }}
          >
            <Typography
              variant="body2"
              sx={{
                color: 'white',
                fontWeight: 500,
                overflow: 'hidden',
                textOverflow: 'ellipsis',
                whiteSpace: 'nowrap',
              }}
            >
              {image.name}
            </Typography>

            <CardActions sx={{ justifyContent: 'center', p: 0 }}>
              <IconButton
                size="small"
                onClick={handleDownload}
                title="Download image"
                sx={{
                  color: 'white',
                  backgroundColor: 'rgba(255, 255, 255, 0.2)',
                  '&:hover': { backgroundColor: 'rgba(255, 255, 255, 0.3)' },
                }}
              >
                <DownloadIcon />
              </IconButton>
              <IconButton
                size="small"
                onClick={handleZoom}
                title="Zoom image"
                sx={{
                  color: 'white',
                  backgroundColor: 'rgba(255, 255, 255, 0.2)',
                  '&:hover': { backgroundColor: 'rgba(255, 255, 255, 0.3)' },
                }}
              >
                <ZoomInIcon />
              </IconButton>
              <IconButton
                size="small"
                onClick={handleDelete}
                title="Delete image"
                sx={{
                  color: 'white',
                  backgroundColor: 'rgba(244, 67, 54, 0.8)',
                  '&:hover': { backgroundColor: 'rgba(244, 67, 54, 1)' },
                }}
              >
                <DeleteIcon />
              </IconButton>
            </CardActions>
          </Box>
        </Fade>
      </Box>
    </Card>
  );
};

export default ImageCard;
