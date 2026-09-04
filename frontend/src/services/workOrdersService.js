import { request } from './apiClient.js';

export async function createWorkOrder(orderData) {
  return request('/work-orders', {
    method: 'POST',
    body: orderData,
  });
}

export async function listWorkOrders(filters = {}) {
  const params = new URLSearchParams();
  if (filters.status) params.append('status', filters.status);
  const queryStr = params.toString();
  return request(`/work-orders${queryStr ? `?${queryStr}` : ''}`);
}

export async function getWorkOrderById(workOrderId) {
  return request(`/work-orders/${workOrderId}`);
}
