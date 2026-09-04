export function renderNavbar(activeHash, currentRole, healthStatus) {
  const roleName = currentRole ? currentRole.toUpperCase() : 'CITIZEN';
  const healthClass = healthStatus && healthStatus.status === 'healthy' ? 'healthy' : 'offline';
  const healthText = healthStatus && healthStatus.status === 'healthy' ? '● Backend Online' : '● Backend Offline';

  let navItems = [];
  if (currentRole === 'citizen') {
    navItems = [
      { hash: '#report', label: '➕ Report Garbage' },
      { hash: '#my-reports', label: '📋 View Reports' },
    ];
  } else if (currentRole === 'supervisor') {
    navItems = [
      { hash: '#dashboard', label: '📊 Dashboard' },
      { hash: '#reports', label: '📋 Garbage Reports' },
      { hash: '#work-orders', label: '📦 Work Orders' },
      { hash: '#assignments', label: '👷 Worker Assignments' },
      { hash: '#verifications', label: '✅ Verifications' },
      { hash: '#ai-verification', label: '🤖 AI Verification' },
      { hash: '#compensations', label: '💰 Compensations' },
      { hash: '#collections', label: '🚛 Collections' },
      { hash: '#weighments', label: '⚖️ Weighments' },
      { hash: '#disposal', label: '♻️ Disposal' },
      { hash: '#audit', label: '📜 Audit Log' },
    ];
  } else if (currentRole === 'worker') {
    navItems = [
      { hash: '#worker', label: '📱 My Field Jobs' },
    ];
  }

  return `
    <nav class="navbar">
      <div class="nav-brand">
        CleanLoop <span>EchoCrew</span>
      </div>

      <ul class="nav-menu">
        ${navItems.map(item => `
          <li class="nav-item ${activeHash === item.hash ? 'active' : ''}" onclick="location.hash='${item.hash}'">
            ${item.label}
          </li>
        `).join('')}
      </ul>

      <div class="nav-controls">
        <div class="health-pill ${healthClass}">
          ${healthText}
        </div>
        <select id="role-selector" class="role-select" onchange="window.dispatchEvent(new CustomEvent('role-change', { detail: this.value }))">
          <option value="citizen" ${currentRole === 'citizen' ? 'selected' : ''}>Role: Citizen</option>
          <option value="supervisor" ${currentRole === 'supervisor' ? 'selected' : ''}>Role: Supervisor / Dispatcher</option>
          <option value="worker" ${currentRole === 'worker' ? 'selected' : ''}>Role: Responder / Worker</option>
        </select>
      </div>
    </nav>
  `;
}
