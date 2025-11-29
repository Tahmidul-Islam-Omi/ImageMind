/**
 * Image Service - Handles image upload and file system operations
 */

const API_BASE_URL = 'http://localhost:8000/api/v1';

export const uploadImage = async (files) => {
  const formData = new FormData();
  
  // Add all files to FormData
  files.forEach((file) => {
    formData.append('files', file);
  });

  try {
    const response = await fetch(`${API_BASE_URL}/images/upload-multiple`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Upload failed');
    }

    const uploadedImages = await response.json();
    
    // Transform API response to match frontend format
    return uploadedImages.map((img) => ({
      id: img.id,
      name: img.name,
      url: `http://localhost:8000${img.url}`,
      size: img.size,
      type: img.type,
      uploadedAt: img.uploaded_at,
    }));
  } catch (error) {
    console.error('Upload error:', error);
    throw error;
  }
};

export const fetchAllImages = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/images`);
    
    if (!response.ok) {
      throw new Error('Failed to fetch images');
    }

    const data = await response.json();
    
    // Transform API response to match frontend format
    return data.images.map((img) => ({
      id: img.id,
      name: img.name,
      url: `http://localhost:8000${img.url}`,
      size: img.size,
      type: img.type,
      uploadedAt: img.uploaded_at,
    }));
  } catch (error) {
    console.error('Fetch error:', error);
    return [];
  }
};

export const deleteImage = async (imageId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/images/${imageId}`, {
      method: 'DELETE',
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Delete failed');
    }

    return { success: true };
  } catch (error) {
    console.error('Delete error:', error);
    throw error;
  }
};
