import { listAuditLogs } from '../services/auditService.js';
import { formatDate } from '../utils/formatters.js';

export class AuditView {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.state = {
      logs: [],
      total: 0,
      loading: true,
      error: null,
      filterAction: '',
      filterEntity: '',
    };
  }

  async loadData() {
    this.state.loading = true;
    this.state.error = null;
    this.render();

    try {
      const filters = {};
      if (this.state.filterAction) filters.action = this.state.filterAction;
      if (this.state.filterEntity) filters.entity_type = this.state.filterEntity;

      const res = await listAuditLogs(filters);
      this.state.total = res[0] || 0;
      this.state.logs = res[1] || res || [];
      this.state.loading = false;
      this.render();
    } catch (err) {
      this.state.loading = false;
      this.state.error = err.message || 'Failed to load audit logs';
      this.render();
    }
  }

  render() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div class="card">
        <div class="card-header" style="flex-wrap: wrap; gap: 12px;">
          <div>
            <h2 class="card-title">📜 Immutable System Audit Log Trail</h2>
            <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 2px;">
              System-generated chronological audit records for all operational lifecycle events. Cannot be forged by clients.
            </p>
          </div>
          <button class="btn btn-secondary btn-sm" id="btn-refresh-audit">🔄 Refresh</button>
        </div>

        <!-- Filter -->
        <div style="display: flex; gap: 12px; margin-bottom: 16px; background: var(--bg-input); padding: 10px; border-radius: var(--radius-sm); flex-wrap: wrap;">
          <input type="text" id="filter-audit-action" class="form-input" placeholder="Filter by action (e.g. report_created)" value="${this.state.filterAction}" style="max-width: 220px;" />
          <input type="text" id="filter-audit-entity" class="form-input" placeholder="Filter by entity (e.g. GarbageReport)" value="${this.state.filterEntity}" style="max-width: 220px;" />
          <button class="btn btn-secondary btn-sm" id="btn-apply-audit-filter">Apply Filter</button>
        </div>

        ${this.state.error ? `<div class="alert alert-danger">${this.state.error}</div>` : ''}

        ${this.state.loading ? `
          <div style="text-align: center; padding: 40px; color: var(--text-muted);">🔄 Loading audit trail...</div>
        ` : this.state.logs.length === 0 ? `
          <div style="text-align: center; padding: 40px; color: var(--text-muted);">No audit log entries recorded.</div>
        ` : `
          <div class="table-responsive">
            <table class="table">
              <thead>
                <tr>
                  <th>Audit ID</th>
                  <th>Action</th>
                  <th>Entity Reference</th>
                  <th>Actor ID</th>
                  <th>Description</th>
                  <th>Recorded At</th>
                </tr>
              </thead>
              <tbody>
                ${this.state.logs.map(a => `
                  <tr>
                    <td><strong>#${a.id}</strong></td>
                    <td><span class="badge" style="background: rgba(255,255,255,0.08); font-family: monospace;">${a.action}</span></td>
                    <td><span style="font-weight: 600;">${a.entity_type}</span> #${a.entity_id || 'N/A'}</td>
                    <td>${a.actor_id ? `User #${a.actor_id}` : 'System'}</td>
                    <td style="font-size: 0.85rem;">${a.description || '—'}</td>
                    <td style="font-size: 0.8rem; color: var(--text-muted);">${formatDate(a.created_at)}</td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        `}
      </div>
    `;

    this.attachEvents();
  }

  attachEvents() {
    const btnRefresh = document.getElementById('btn-refresh-audit');
    if (btnRefresh) btnRefresh.addEventListener('click', () => this.loadData());

    const btnFilter = document.getElementById('btn-apply-audit-filter');
    if (btnFilter) {
      btnFilter.addEventListener('click', () => {
        this.state.filterAction = document.getElementById('filter-audit-action').value.trim();
        this.state.filterEntity = document.getElementById('filter-audit-entity').value.trim();
        this.loadData();
      });
    }
  }
}
