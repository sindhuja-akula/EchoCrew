import { request } from './apiClient.js';

export async function createCollectionBatch(batchData) {
  return request('/collections', {
    method: 'POST',
    body: batchData,
  });
}

export async function listBatches(filters = {}) {
  const params = new URLSearchParams();
  if (filters.status) params.append('status', filters.status);
  if (filters.vehicle_id) params.append('vehicle_id', filters.vehicle_id);
  const queryStr = params.toString();
  return request(`/collections${queryStr ? `?${queryStr}` : ''}`);
}

export async function getBatchById(batchId) {
  return request(`/collections/${batchId}`);
}

export async function updateBatchStatus(batchId, statusData) {
  return request(`/collections/${batchId}/status`, {
    method: 'PATCH',
    body: statusData,
  });
}
