import { listReports, getReportById } from '../services/reportsService.js';
import { createWorkOrder } from '../services/workOrdersService.js';
import { formatDate, formatCoordinates, getCategoryMeta, renderStatusBadge } from '../utils/formatters.js';
import { WASTE_CATEGORIES } from '../utils/constants.js';

export class ReportsView {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.state = {
      reports: [],
      total: 0,
      loading: true,
      error: null,
      filterStatus: '',
      filterCategory: '',
      filterVolume: '',
      selectedReport: null,
      isDispatching: false,
      dispatchSuccess: null,
    };
  }

  async loadData() {
    this.state.loading = true;
    this.state.error = null;
    this.render();

    try {
      const filters = {};
      if (this.state.filterStatus) filters.status = this.state.filterStatus;
      if (this.state.filterCategory) filters.category = this.state.filterCategory;
      if (this.state.filterVolume) filters.volume_tier = this.state.filterVolume;

      const res = await listReports(filters);
      this.state.reports = res.reports || [];
      this.state.total = res.total || 0;
      this.state.loading = false;
      this.render();
    } catch (err) {
      this.state.loading = false;
      this.state.error = err.message || 'Failed to load reports';
      this.render();
    }
  }

  render() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div class="card">
        <div class="card-header" style="flex-wrap: wrap; gap: 12px;">
          <div>
            <h2 class="card-title">📋 Garbage Accumulation Reports (${this.state.total})</h2>
            <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 2px;">
              Live citizen and responder incident reports ingested into PostGIS database.
            </p>
          </div>
          <button class="btn btn-secondary btn-sm" id="btn-refresh-reports">🔄 Refresh</button>
        </div>

        <!-- Filters -->
        <div style="display: flex; gap: 12px; margin-bottom: 16px; flex-wrap: wrap; background: var(--bg-input); padding: 12px; border-radius: var(--radius-sm);">
          <select id="filter-status" class="form-select" style="max-width: 180px;">
            <option value="">All Statuses</option>
            <option value="reported" ${this.state.filterStatus === 'reported' ? 'selected' : ''}>Reported</option>
            <option value="under_review" ${this.state.filterStatus === 'under_review' ? 'selected' : ''}>Under Review</option>
            <option value="approved" ${this.state.filterStatus === 'approved' ? 'selected' : ''}>Approved</option>
            <option value="assigned" ${this.state.filterStatus === 'assigned' ? 'selected' : ''}>Assigned</option>
            <option value="in_progress" ${this.state.filterStatus === 'in_progress' ? 'selected' : ''}>In Progress</option>
            <option value="cleaned" ${this.state.filterStatus === 'cleaned' ? 'selected' : ''}>Cleaned</option>
            <option value="verified" ${this.state.filterStatus === 'verified' ? 'selected' : ''}>Verified</option>
          </select>

          <select id="filter-category" class="form-select" style="max-width: 180px;">
            <option value="">All Categories</option>
            ${WASTE_CATEGORIES.map(c => `
              <option value="${c.value}" ${this.state.filterCategory === c.value ? 'selected' : ''}>${c.label}</option>
            `).join('')}
          </select>

          <select id="filter-volume" class="form-select" style="max-width: 180px;">
            <option value="">All Volume Tiers</option>
            <option value="minor" ${this.state.filterVolume === 'minor' ? 'selected' : ''}>Minor</option>
            <option value="moderate" ${this.state.filterVolume === 'moderate' ? 'selected' : ''}>Moderate</option>
            <option value="bulk" ${this.state.filterVolume === 'bulk' ? 'selected' : ''}>Bulk</option>
          </select>
        </div>

        ${this.state.error ? `
          <div class="alert alert-danger">${this.state.error}</div>
        ` : ''}

        ${this.state.loading ? `
          <div style="text-align: center; padding: 40px; color: var(--text-muted);">
            🔄 Loading reports from API...
          </div>
        ` : this.state.reports.length === 0 ? `
          <div style="text-align: center; padding: 40px; color: var(--text-muted);">
            No garbage reports found matching the filter criteria.
          </div>
        ` : `
          <div class="table-responsive">
            <table class="table">
              <thead>
                <tr>
                  <th>Report ID</th>
                  <th>Category</th>
                  <th>Volume</th>
                  <th>Coordinates</th>
                  <th>Status</th>
                  <th>Submitted</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                ${this.state.reports.map(r => {
                  const cat = getCategoryMeta(r.category);
                  return `
                    <tr>
                      <td><strong>#${r.id}</strong></td>
                      <td>${cat.icon} ${cat.label}</td>
                      <td><span style="font-weight:600; text-transform:uppercase; font-size:0.8rem;">${r.volume_tier}</span></td>
                      <td>${formatCoordinates(r.latitude, r.longitude)}</td>
                      <td>${renderStatusBadge(r.status, 'report')}</td>
                      <td>${formatDate(r.created_at)}</td>
                      <td>
                        <button class="btn btn-secondary btn-sm" data-view-report="${r.id}">🔍 View</button>
                      </td>
                    </tr>
                  `;
                }).join('')}
              </tbody>
            </table>
          </div>
        `}
      </div>

      <!-- Detail Modal -->
      ${this.state.selectedReport ? this.renderDetailModal() : ''}
    `;

    this.attachEvents();
  }

  renderDetailModal() {
    const r = this.state.selectedReport;
    const cat = getCategoryMeta(r.category);

    return `
      <div class="modal-overlay" id="modal-overlay">
        <div class="modal-content">
          <div class="card-header">
            <h3 class="card-title">Garbage Report #${r.id}</h3>
            <button class="btn btn-secondary btn-sm" id="btn-close-modal">✕ Close</button>
          </div>

          ${this.state.dispatchSuccess ? `
            <div class="alert alert-success">${this.state.dispatchSuccess}</div>
          ` : ''}

          <div class="grid grid-2" style="margin-bottom: 16px;">
            <div>
              <div style="font-size: 0.8rem; color: var(--text-muted);">Status</div>
              <div style="margin-top: 4px;">${renderStatusBadge(r.status, 'report')}</div>
            </div>
            <div>
              <div style="font-size: 0.8rem; color: var(--text-muted);">Waste Category</div>
              <div style="font-weight: 600; margin-top: 4px;">${cat.icon} ${cat.label}</div>
            </div>
            <div>
              <div style="font-size: 0.8rem; color: var(--text-muted);">Estimated Volume</div>
              <div style="font-weight: 600; text-transform: uppercase; margin-top: 4px;">${r.volume_tier}</div>
            </div>
            <div>
              <div style="font-size: 0.8rem; color: var(--text-muted);">Submitted Date</div>
              <div style="font-size: 0.9rem; margin-top: 4px;">${formatDate(r.created_at)}</div>
            </div>
          </div>

          <div style="margin-bottom: 16px;">
            <div style="font-size: 0.8rem; color: var(--text-muted);">GPS Coordinates</div>
            <div style="font-weight: 600; margin-top: 2px;">${formatCoordinates(r.latitude, r.longitude)}</div>
          </div>

          ${r.description ? `
            <div style="margin-bottom: 16px; background: var(--bg-input); padding: 10px; border-radius: var(--radius-sm);">
              <div style="font-size: 0.8rem; color: var(--text-muted);">Description / Landmark</div>
              <div style="font-size: 0.9rem; margin-top: 4px;">${r.description}</div>
            </div>
          ` : ''}

          ${r.image_url ? `
            <div style="margin-bottom: 16px; border-radius: var(--radius-md); overflow: hidden;">
              <img src="http://localhost:8000/${r.image_url}" alt="Site Photo" style="width: 100%; max-height: 240px; object-fit: cover;" />
            </div>
          ` : ''}

          <!-- Supervisor Dispatch Trigger -->
          <div style="border-top: 1px solid var(--border-color); padding-top: 16px; margin-top: 16px;">
            <h4 style="font-size: 0.95rem; margin-bottom: 8px;">Supervisor Operations</h4>
            ${r.status === 'reported' || r.status === 'under_review' || r.status === 'approved' ? `
              <button class="btn btn-primary" id="btn-dispatch-order" ${this.state.isDispatching ? 'disabled' : ''}>
                ${this.state.isDispatching ? '🔄 Dispatching Work Order...' : '📦 Dispatch Work Order for this Report'}
              </button>
            ` : `
              <div style="font-size: 0.85rem; color: var(--text-muted);">
                Work Order already dispatched for this report (Status: ${r.status}).
              </div>
            `}
          </div>
        </div>
      </div>
    `;
  }

  attachEvents() {
    const btnRefresh = document.getElementById('btn-refresh-reports');
    if (btnRefresh) {
      btnRefresh.addEventListener('click', () => this.loadData());
    }

    const selStatus = document.getElementById('filter-status');
    if (selStatus) {
      selStatus.addEventListener('change', (e) => {
        this.state.filterStatus = e.target.value;
        this.loadData();
      });
    }

    const selCat = document.getElementById('filter-category');
    if (selCat) {
      selCat.addEventListener('change', (e) => {
        this.state.filterCategory = e.target.value;
        this.loadData();
      });
    }

    const selVol = document.getElementById('filter-volume');
    if (selVol) {
      selVol.addEventListener('change', (e) => {
        this.state.filterVolume = e.target.value;
        this.loadData();
      });
    }

    this.container.querySelectorAll('[data-view-report]').forEach(btn => {
      btn.addEventListener('click', () => {
        const id = parseInt(btn.dataset.viewReport);
        const found = this.state.reports.find(r => r.id === id);
        if (found) {
          this.state.selectedReport = found;
          this.state.dispatchSuccess = null;
          this.render();
        }
      });
    });

    const btnClose = document.getElementById('btn-close-modal');
    if (btnClose) {
      btnClose.addEventListener('click', () => {
        this.state.selectedReport = null;
        this.render();
      });
    }

    const btnDispatch = document.getElementById('btn-dispatch-order');
    if (btnDispatch) {
      btnDispatch.addEventListener('click', async () => {
        await this.handleDispatch();
      });
    }
  }

  async handleDispatch() {
    const report = this.state.selectedReport;
    if (!report) return;

    this.state.isDispatching = true;
    this.render();

    try {
      const wo = await createWorkOrder({
        report_id: report.id,
        classification: 'GENERAL_CLEANUP',
        required_worker_count: 1,
      });

      this.state.isDispatching = false;
      this.state.dispatchSuccess = `Work Order ${wo.work_code} created successfully! Sub-unit ${wo.units[0]?.unit_code || 'WU-1'} assigned.`;
      this.loadData();
    } catch (err) {
      this.state.isDispatching = false;
      this.state.error = err.message || 'Failed to dispatch work order.';
      this.render();
    }
  }
}
