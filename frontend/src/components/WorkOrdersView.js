import { listWorkOrders, getWorkOrderById, createWorkOrder } from '../services/workOrdersService.js';
import { formatDate, renderStatusBadge } from '../utils/formatters.js';

export class WorkOrdersView {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.state = {
      orders: [],
      loading: true,
      error: null,
      filterStatus: '',
      selectedOrder: null,
      showCreateModal: false,
      createReportId: '',
      createClassification: 'GENERAL_CLEANUP',
      createWorkerCount: 1,
      isSubmitting: false,
    };
  }

  async loadData() {
    this.state.loading = true;
    this.state.error = null;
    this.render();

    try {
      const filters = {};
      if (this.state.filterStatus) filters.status = this.state.filterStatus;
      const res = await listWorkOrders(filters);
      this.state.orders = res || [];
      this.state.loading = false;
      this.render();
    } catch (err) {
      this.state.loading = false;
      this.state.error = err.message || 'Failed to load work orders';
      this.render();
    }
  }

  render() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div class="card">
        <div class="card-header" style="flex-wrap: wrap; gap: 12px;">
          <div>
            <h2 class="card-title">📦 Work Order Dispatch Management</h2>
            <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 2px;">
              Cleanup jobs dispatched per incident report with sub-task work units.
            </p>
          </div>
          <div style="display: flex; gap: 8px;">
            <button class="btn btn-primary btn-sm" id="btn-open-create-wo">➕ New Work Order</button>
            <button class="btn btn-secondary btn-sm" id="btn-refresh-wo">🔄 Refresh</button>
          </div>
        </div>

        <!-- Filter -->
        <div style="margin-bottom: 16px; background: var(--bg-input); padding: 10px; border-radius: var(--radius-sm); display: flex; gap: 12px;">
          <select id="filter-wo-status" class="form-select" style="max-width: 200px;">
            <option value="">All Statuses</option>
            <option value="open" ${this.state.filterStatus === 'open' ? 'selected' : ''}>Open</option>
            <option value="assigned" ${this.state.filterStatus === 'assigned' ? 'selected' : ''}>Assigned</option>
            <option value="in_progress" ${this.state.filterStatus === 'in_progress' ? 'selected' : ''}>In Progress</option>
            <option value="completed" ${this.state.filterStatus === 'completed' ? 'selected' : ''}>Completed</option>
            <option value="cancelled" ${this.state.filterStatus === 'cancelled' ? 'selected' : ''}>Cancelled</option>
          </select>
        </div>

        ${this.state.error ? `<div class="alert alert-danger">${this.state.error}</div>` : ''}

        ${this.state.loading ? `
          <div style="text-align: center; padding: 40px; color: var(--text-muted);">🔄 Loading work orders...</div>
        ` : this.state.orders.length === 0 ? `
          <div style="text-align: center; padding: 40px; color: var(--text-muted);">No work orders found.</div>
        ` : `
          <div class="table-responsive">
            <table class="table">
              <thead>
                <tr>
                  <th>Order Code</th>
                  <th>Report ID</th>
                  <th>Classification</th>
                  <th>Req. Workers</th>
                  <th>Sub-Units</th>
                  <th>Status</th>
                  <th>Dispatched</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                ${this.state.orders.map(o => `
                  <tr>
                    <td><strong>${o.work_code}</strong></td>
                    <td>#${o.report_id}</td>
                    <td>${o.classification}</td>
                    <td>${o.required_worker_count}</td>
                    <td>${o.units ? o.units.length : 0} units</td>
                    <td>${renderStatusBadge(o.status, 'work_order')}</td>
                    <td>${formatDate(o.created_at)}</td>
                    <td>
                      <button class="btn btn-secondary btn-sm" data-view-wo="${o.id}">🔍 Details</button>
                    </td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        `}
      </div>

      <!-- Create Work Order Modal -->
      ${this.state.showCreateModal ? this.renderCreateModal() : ''}

      <!-- Detail Modal -->
      ${this.state.selectedOrder ? this.renderDetailModal() : ''}
    `;

    this.attachEvents();
  }

  renderCreateModal() {
    return `
      <div class="modal-overlay">
        <div class="modal-content">
          <div class="card-header">
            <h3 class="card-title">Create & Dispatch Work Order</h3>
            <button class="btn btn-secondary btn-sm" id="btn-close-create-modal">✕</button>
          </div>
          <form id="create-wo-form">
            <div class="form-group">
              <label class="form-label">Garbage Report ID <span class="required">*</span></label>
              <input type="number" id="input-report-id" class="form-input" placeholder="e.g. 1" value="${this.state.createReportId}" required />
            </div>
            <div class="form-group">
              <label class="form-label">Job Classification</label>
              <select id="input-classification" class="form-select">
                <option value="GENERAL_CLEANUP">General Cleanup</option>
                <option value="BULK_RECOVERY">Bulk Waste Recovery</option>
                <option value="HAZARDOUS_DISPOSAL">Hazardous Containment</option>
                <option value="EWASTE_COLLECTION">E-Waste Retrieval</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">Required Worker Count</label>
              <input type="number" id="input-worker-count" class="form-input" min="1" max="10" value="${this.state.createWorkerCount}" required />
            </div>
            <button type="submit" class="btn btn-primary" style="width: 100%;" ${this.state.isSubmitting ? 'disabled' : ''}>
              ${this.state.isSubmitting ? 'Dispatching...' : '🚀 Dispatch Work Order'}
            </button>
          </form>
        </div>
      </div>
    `;
  }

  renderDetailModal() {
    const o = this.state.selectedOrder;
    return `
      <div class="modal-overlay">
        <div class="modal-content">
          <div class="card-header">
            <h3 class="card-title">Work Order Details (${o.work_code})</h3>
            <button class="btn btn-secondary btn-sm" id="btn-close-detail-modal">✕</button>
          </div>
          <div class="grid grid-2" style="margin-bottom: 16px;">
            <div><strong>Report ID:</strong> #${o.report_id}</div>
            <div><strong>Status:</strong> ${renderStatusBadge(o.status, 'work_order')}</div>
            <div><strong>Classification:</strong> ${o.classification}</div>
            <div><strong>Worker Count Req:</strong> ${o.required_worker_count}</div>
          </div>
          <h4 style="margin: 12px 0 6px;">Associated Work Units (${o.units ? o.units.length : 0})</h4>
          ${o.units && o.units.length > 0 ? `
            <div class="table-responsive">
              <table class="table">
                <thead>
                  <tr>
                    <th>Unit Code</th>
                    <th>Seq</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  ${o.units.map(u => `
                    <tr>
                      <td><strong>${u.unit_code}</strong></td>
                      <td>#${u.sequence_number}</td>
                      <td>${renderStatusBadge(u.status, 'work_order')}</td>
                    </tr>
                  `).join('')}
                </tbody>
              </table>
            </div>
          ` : '<div style="color: var(--text-muted); font-size: 0.85rem;">No work units found.</div>'}
        </div>
      </div>
    `;
  }

  attachEvents() {
    const btnRefresh = document.getElementById('btn-refresh-wo');
    if (btnRefresh) btnRefresh.addEventListener('click', () => this.loadData());

    const selStatus = document.getElementById('filter-wo-status');
    if (selStatus) {
      selStatus.addEventListener('change', (e) => {
        this.state.filterStatus = e.target.value;
        this.loadData();
      });
    }

    const btnOpenCreate = document.getElementById('btn-open-create-wo');
    if (btnOpenCreate) {
      btnOpenCreate.addEventListener('click', () => {
        this.state.showCreateModal = true;
        this.render();
      });
    }

    const btnCloseCreate = document.getElementById('btn-close-create-modal');
    if (btnCloseCreate) {
      btnCloseCreate.addEventListener('click', () => {
        this.state.showCreateModal = false;
        this.render();
      });
    }

    const btnCloseDetail = document.getElementById('btn-close-detail-modal');
    if (btnCloseDetail) {
      btnCloseDetail.addEventListener('click', () => {
        this.state.selectedOrder = null;
        this.render();
      });
    }

    this.container.querySelectorAll('[data-view-wo]').forEach(btn => {
      btn.addEventListener('click', async () => {
        const id = parseInt(btn.dataset.viewWo);
        try {
          const detail = await getWorkOrderById(id);
          this.state.selectedOrder = detail;
          this.render();
        } catch (err) {
          alert(`Failed to load work order: ${err.message}`);
        }
      });
    });

    const createForm = document.getElementById('create-wo-form');
    if (createForm) {
      createForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const repId = parseInt(document.getElementById('input-report-id').value);
        const cls = document.getElementById('input-classification').value;
        const count = parseInt(document.getElementById('input-worker-count').value);

        this.state.isSubmitting = true;
        this.render();

        try {
          await createWorkOrder({
            report_id: repId,
            classification: cls,
            required_worker_count: count,
          });
          this.state.isSubmitting = false;
          this.state.showCreateModal = false;
          this.loadData();
        } catch (err) {
          this.state.isSubmitting = false;
          alert(`Create Work Order Error: ${err.message}`);
          this.render();
        }
      });
    }
  }
}
