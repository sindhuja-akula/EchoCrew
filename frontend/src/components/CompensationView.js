import { listCompensations, updateCompensationStatus } from '../services/compensationService.js';
import { formatDate, renderStatusBadge } from '../utils/formatters.js';

export class CompensationView {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.state = {
      compensations: [],
      loading: true,
      error: null,
      filterStatus: '',
    };
  }

  async loadData() {
    this.state.loading = true;
    this.state.error = null;
    this.render();

    try {
      const filters = {};
      if (this.state.filterStatus) filters.status = this.state.filterStatus;
      const res = await listCompensations(filters);
      this.state.compensations = res[1] || res || [];
      this.state.loading = false;
      this.render();
    } catch (err) {
      this.state.loading = false;
      this.state.error = err.message || 'Failed to load compensations';
      this.render();
    }
  }

  render() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div class="card">
        <div class="card-header" style="flex-wrap: wrap; gap: 12px;">
          <div>
            <h2 class="card-title">💰 Worker Compensation Eligibility</h2>
            <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 2px;">
              Automated payout eligibility foundation created upon supervisor work verification. (No bank transfer execution in Phase 2).
            </p>
          </div>
          <button class="btn btn-secondary btn-sm" id="btn-refresh-comp">🔄 Refresh</button>
        </div>

        ${this.state.error ? `<div class="alert alert-danger">${this.state.error}</div>` : ''}

        ${this.state.loading ? `
          <div style="text-align: center; padding: 40px; color: var(--text-muted);">🔄 Loading compensations...</div>
        ` : this.state.compensations.length === 0 ? `
          <div style="text-align: center; padding: 40px; color: var(--text-muted);">No compensation eligibility records found.</div>
        ` : `
          <div class="table-responsive">
            <table class="table">
              <thead>
                <tr>
                  <th>Record ID</th>
                  <th>Worker ID</th>
                  <th>Assignment ID</th>
                  <th>Amount</th>
                  <th>Status</th>
                  <th>Logged Date</th>
                  <th>State Action</th>
                </tr>
              </thead>
              <tbody>
                ${this.state.compensations.map(c => `
                  <tr>
                    <td><strong>#${c.id}</strong></td>
                    <td>Worker #${c.worker_id}</td>
                    <td>Assignment #${c.assignment_id}</td>
                    <td style="font-weight: 700; color: var(--success);">${c.amount} ${c.currency}</td>
                    <td>${renderStatusBadge(c.status, 'compensation')}</td>
                    <td>${formatDate(c.created_at)}</td>
                    <td>
                      ${c.status === 'eligible' ? `
                        <button class="btn btn-primary btn-sm" data-comp-action="${c.id}" data-target-status="processing">Process Payout</button>
                      ` : ''}
                      ${c.status === 'processing' ? `
                        <button class="btn btn-success btn-sm" data-comp-action="${c.id}" data-target-status="paid">Mark Paid</button>
                      ` : ''}
                      ${c.status === 'paid' ? `
                        <span style="font-size: 0.8rem; color: var(--success);">Disbursed</span>
                      ` : ''}
                    </td>
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
    const btnRefresh = document.getElementById('btn-refresh-comp');
    if (btnRefresh) btnRefresh.addEventListener('click', () => this.loadData());

    this.container.querySelectorAll('[data-comp-action]').forEach(btn => {
      btn.addEventListener('click', async () => {
        const id = parseInt(btn.dataset.compAction);
        const targetStatus = btn.dataset.targetStatus;
        try {
          await updateCompensationStatus(id, { status: targetStatus });
          this.loadData();
        } catch (err) {
          alert(`Compensation Update Error: ${err.message}`);
        }
      });
    });
  }
}
