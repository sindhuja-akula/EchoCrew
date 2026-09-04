import { renderStatusBadge } from '../utils/formatters.js';

export function StatusBadge(status, type = 'report') {
  return renderStatusBadge(status, type);
}
