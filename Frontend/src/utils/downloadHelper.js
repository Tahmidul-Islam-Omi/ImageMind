/**
 * Download a file from a URL
 * @param {string} url - The URL of the file to download
 * @param {string} filename - The name to save the file as
 * @returns {Promise<boolean>} - Success status
 */
export const downloadFile = async (url, filename) => {
  try {
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error('Failed to fetch file');
    }
    
    const blob = await response.blob();
    const blobUrl = window.URL.createObjectURL(blob);
    
    const link = document.createElement('a');
    link.href = blobUrl;
    link.download = filename;
    link.style.display = 'none';
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    // Clean up the blob URL
    window.URL.revokeObjectURL(blobUrl);
    
    return true;
  } catch (error) {
    console.error('Download failed:', error);
    return false;
  }
};


