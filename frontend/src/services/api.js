import { API_BASE_URL } from '../utils/constants.js';

export async function fetchDashboardMetrics() {
  const response = await fetch(`${API_BASE_URL}/dashboard/metrics`);
  if (!response.ok) {
    throw new Error('Failed to fetch dashboard metrics');
  }
  return response.json();
}

export async function fetchReports() {
  const response = await fetch(`${API_BASE_URL}/reports`);
  if (!response.ok) {
    throw new Error('Failed to fetch reports');
  }
  return response.json();
}
