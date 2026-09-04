import {
  REPORT_STATUSES,
  WORKER_STATUSES,
  WORK_ORDER_STATUSES,
  ASSIGNMENT_STATUSES,
  VERIFICATION_STATUSES,
  COMPENSATION_STATUSES,
  COLLECTION_BATCH_STATUSES,
  WASTE_CATEGORIES,
} from './constants.js';

export function formatDate(dateString) {
  if (!dateString) return 'N/A';
  try {
    return new Date(dateString).toLocaleString('en-IN', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      hour12: true,
    });
  } catch (e) {
    return dateString;
  }
}

export function formatCoordinates(lat, lng) {
  if (lat === null || lat === undefined || lng === null || lng === undefined) return 'Location Not Set';
  const latNum = parseFloat(lat);
  const lngNum = parseFloat(lng);
  return `${latNum.toFixed(4)}° N, ${lngNum.toFixed(4)}° E`;
}

export function getCategoryMeta(categoryValue) {
  const found = WASTE_CATEGORIES.find(c => c.value === categoryValue);
  return found || { label: categoryValue || 'General', icon: '🗑️', description: '' };
}

export function renderStatusBadge(status, type = 'report') {
  let map = REPORT_STATUSES;
  if (type === 'worker') map = WORKER_STATUSES;
  else if (type === 'work_order') map = WORK_ORDER_STATUSES;
  else if (type === 'assignment') map = ASSIGNMENT_STATUSES;
  else if (type === 'verification') map = VERIFICATION_STATUSES;
  else if (type === 'compensation') map = COMPENSATION_STATUSES;
  else if (type === 'collection') map = COLLECTION_BATCH_STATUSES;

  const meta = map[status] || { label: status || 'Unknown', color: '#64748b' };
  return `<span class="badge" style="background-color: ${meta.color}20; color: ${meta.color}; border: 1px solid ${meta.color}40;">● ${meta.label}</span>`;
}

export function capitalize(str) {
  if (!str) return '';
  return str.charAt(0).toUpperCase() + str.slice(1).replace(/_/g, ' ');
}
