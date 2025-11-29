# Image Upload Component

## Architecture

This component follows clean architecture principles with separation of concerns:

### Components
- **ImageUploadContainer**: Main container managing state and orchestrating child components
- **ImageUploadZone**: Drag-and-drop upload zone with file selection
- **ImageGallery**: Grid layout displaying uploaded images
- **ImageCard**: Individual image card with hover effects and actions

### Services
- **imageService**: Handles image upload logic and file system operations

### Features
- ✨ Drag and drop image upload
- 📁 Multiple file selection
- 🎨 Beautiful gradient UI with MUI
- 🖼️ Responsive image gallery
- 🗑️ Delete images
- 💾 Download images
- 🎭 Smooth hover animations
- 📱 Mobile responsive

### Usage
```jsx
import ImageUploadContainer from './components/ImageUpload';

function App() {
  return <ImageUploadContainer />;
}
```
