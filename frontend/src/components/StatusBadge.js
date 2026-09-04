export function renderStatusBadge(status, label) {
  const badge = document.createElement('div');
  badge.className = `badge badge-${status}`;
  badge.textContent = label;
  return badge;
}
