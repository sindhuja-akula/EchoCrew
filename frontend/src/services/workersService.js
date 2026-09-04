import { request } from './apiClient.js';

export async function createWorker(workerData) {
  return request('/workers', {
    method: 'POST',
    body: workerData,
  });
}

export async function listWorkers(filters = {}) {
  const params = new URLSearchParams();
  if (filters.status) params.append('status', filters.status);
  if (filters.verification_state) params.append('verification_state', filters.verification_state);
  const queryStr = params.toString();
  return request(`/workers${queryStr ? `?${queryStr}` : ''}`);
}

export async function getWorkerById(workerId) {
  return request(`/workers/${workerId}`);
}

export async function updateWorkerStatus(workerId, statusData) {
  return request(`/workers/${workerId}/status`, {
    method: 'PATCH',
    body: statusData,
  });
}
