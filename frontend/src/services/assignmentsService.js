import { request } from './apiClient.js';

export async function createAssignment(assignmentData) {
  return request('/assignments', {
    method: 'POST',
    body: assignmentData,
  });
}

export async function listAssignments(filters = {}) {
  const params = new URLSearchParams();
  if (filters.worker_id) params.append('worker_id', filters.worker_id);
  if (filters.status) params.append('status', filters.status);
  const queryStr = params.toString();
  return request(`/assignments${queryStr ? `?${queryStr}` : ''}`);
}

export async function updateAssignmentStatus(assignmentId, statusData) {
  return request(`/assignments/${assignmentId}/status`, {
    method: 'PATCH',
    body: statusData,
  });
}
