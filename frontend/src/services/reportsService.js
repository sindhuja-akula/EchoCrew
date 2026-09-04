import { request } from './apiClient.js';

export async function uploadReportPhoto(file) {
  const formData = new FormData();
  formData.append('file', file);

  return request('/reports/upload-photo', {
    method: 'POST',
    body: formData,
  });
}

export async function createReport(reportData) {
  return request('/reports', {
    method: 'POST',
    body: reportData,
  });
}

export async function listReports(filters = {}) {
  const params = new URLSearchParams();
  if (filters.status) params.append('status', filters.status);
  if (filters.category) params.append('category', filters.category);
  if (filters.volume_tier) params.append('volume_tier', filters.volume_tier);
  if (filters.skip !== undefined) params.append('skip', filters.skip);
  if (filters.limit !== undefined) params.append('limit', filters.limit);

  const queryStr = params.toString();
  return request(`/reports${queryStr ? `?${queryStr}` : ''}`);
}

export async function getReportById(reportId) {
  return request(`/reports/${reportId}`);
}
