import { request } from './apiClient.js';

export async function submitVerification(verificationData) {
  return request('/verifications', {
    method: 'POST',
    body: verificationData,
  });
}

export async function listVerifications(workUnitId) {
  const queryStr = workUnitId ? `?work_unit_id=${workUnitId}` : '';
  return request(`/verifications${queryStr}`);
}

export async function getVerificationById(verificationId) {
  return request(`/verifications/${verificationId}`);
}
