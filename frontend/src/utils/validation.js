import { MAX_UPLOAD_SIZE_BYTES } from './constants.js';

export function validateImageFile(file) {
  if (!file) {
    return { valid: false, error: 'Please select or capture a site photo.' };
  }

  const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];
  if (!allowedTypes.includes(file.type.toLowerCase())) {
    return {
      valid: false,
      error: `Unsupported image format (${file.type}). Allowed formats: JPEG, PNG, WEBP.`
    };
  }

  if (file.size > MAX_UPLOAD_SIZE_BYTES) {
    const sizeMb = (file.size / (1024 * 1024)).toFixed(1);
    return {
      valid: false,
      error: `Image size (${sizeMb} MB) exceeds maximum upload limit of 10 MB.`
    };
  }

  return { valid: true, error: null };
}

export function validateCoordinates(lat, lng) {
  if (lat === null || lat === undefined || lng === null || lng === undefined) {
    return { valid: false, error: 'Latitude and Longitude are required. Please click "Use My Location".' };
  }

  const latitude = parseFloat(lat);
  const longitude = parseFloat(lng);

  if (isNaN(latitude) || latitude < -90 || latitude > 90) {
    return { valid: false, error: `Invalid latitude coordinate (${lat}). Must be between -90 and 90.` };
  }

  if (isNaN(longitude) || longitude < -180 || longitude > 180) {
    return { valid: false, error: `Invalid longitude coordinate (${lng}). Must be between -180 and 180.` };
  }

  return { valid: true, error: null };
}

export function validateReportForm({ latitude, longitude, category, volume_tier, imageFile, image_url }) {
  const errors = [];

  const coordVal = validateCoordinates(latitude, longitude);
  if (!coordVal.valid) errors.push(coordVal.error);

  if (!category) errors.push('Waste Category selection is required.');
  if (!volume_tier) errors.push('Volume Tier selection is required.');

  if (imageFile) {
    const imgVal = validateImageFile(imageFile);
    if (!imgVal.valid) errors.push(imgVal.error);
  }

  return {
    valid: errors.length === 0,
    errors
  };
}
