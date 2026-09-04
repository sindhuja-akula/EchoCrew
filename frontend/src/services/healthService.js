import { request } from './apiClient.js';

export async function getHealth() {
  return request('/health');
}
