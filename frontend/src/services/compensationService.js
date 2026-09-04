import { request } from './apiClient.js';

export async function listCompensations(filters = {}) {
  const params = new URLSearchParams();
  if (filters.worker_id) params.append('worker_id', filters.worker_id);
  if (filters.status) params.append('status', filters.status);
  const queryStr = params.toString();
  return request(`/compensations${queryStr ? `?${queryStr}` : ''}`);
}

export async function getCompensationById(comp_id) {
  return request(`/compensations/${comp_id}`);
}

export async function updateCompensationStatus(comp_id, statusData) {
  return request(`/compensations/${comp_id}/status`, {
    method: 'PATCH',
    body: statusData,
  });
}
