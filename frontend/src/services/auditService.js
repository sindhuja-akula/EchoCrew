import { request } from './apiClient.js';

export async function listAuditLogs(filters = {}) {
  const params = new URLSearchParams();
  if (filters.action) params.append('action', filters.action);
  if (filters.entity_type) params.append('entity_type', filters.entity_type);
  const queryStr = params.toString();
  return request(`/audit${queryStr ? `?${queryStr}` : ''}`);
}

export async function getAuditLogById(auditId) {
  return request(`/audit/${auditId}`);
}
