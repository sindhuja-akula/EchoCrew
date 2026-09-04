import { request } from './apiClient.js';

export async function submitEvidence(evidenceData) {
  return request('/evidence', {
    method: 'POST',
    body: evidenceData,
  });
}

export async function listEvidence(workUnitId) {
  const queryStr = workUnitId ? `?work_unit_id=${workUnitId}` : '';
  return request(`/evidence${queryStr}`);
}

export async function getEvidenceById(evidenceId) {
  return request(`/evidence/${evidenceId}`);
}
