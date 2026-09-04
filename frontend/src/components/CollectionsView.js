import { listBatches, createCollectionBatch, updateBatchStatus } from '../services/collectionService.js';
import { formatDate, renderStatusBadge } from '../utils/formatters.js';

export class CollectionsView {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.state = {
      batches: [],
      loading: true,
      error: null,
      showModal: false,
      inputVolume: 5.0,
      inputVehicleId: '',
      isSubmitting: false,
    };
  }

  async loadData() {
    this.state.loading = true;
    this.state.error = null;
    this.render();

    try {
      const res = await listBatches();
      this.state.batches = res[1] || res || [];
      this.state.loading = false;
      this.render();
    } catch (err) {
      this.state.loading = false;
      this.state.error = err.message || 'Failed to load collection batches';
      this.render();
    }
  }

  render() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div class="card">
        <div class="card-header" style="flex-wrap: wrap; gap: 12px;">
          <div>
            <h2 class="card-title">🚛 Waste Collection & Transport Batches</h2>
            <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 2px;">
              Durable batch-level aggregation tracking waste transport from work units to transfer stations.
            </p>
          </div>
          <div style="display: flex; gap: 8px;">
            <button class="btn btn-primary btn-sm" id="btn-open-batch-modal">➕ Create Collection Batch</button>
            <button class="btn btn-secondary btn-sm" id="btn-refresh-batch">🔄 Refresh</button>
          </div>
        </div>

        ${this.state.error ? `<div class="alert alert-danger">${this.state.error}</div>` : ''}

        ${this.state.loading ? `
          <div style="text-align: center; padding: 40px; color: var(--text-muted);">🔄 Loading collection batches...</div>
        ` : this.state.batches.length === 0 ? `
          <div style="text-align: center; padding: 40px; color: var(--text-muted);">No waste collection batches found.</div>
        ` : `
          <div class="table-responsive">
            <table class="table">
              <thead>
                <tr>
                  <th>Batch Code</th>
                  <th>Vehicle ID</th>
                  <th>Total Volume (m³)</th>
                  <th>Status</th>
                  <th>Collected Date</th>
                  <th>Transport Action</th>
                </tr>
              </thead>
              <tbody>
                ${this.state.batches.map(b => `
                  <tr>
                    <td><strong>${b.batch_code}</strong></td>
                    <td>${b.vehicle_id ? `Vehicle #${b.vehicle_id}` : 'Unassigned'}</td>
                    <td><span style="font-weight: 700; color: var(--primary);">${b.total_volume_m3} m³</span></td>
                    <td>${renderStatusBadge(b.status, 'collection')}</td>
                    <td>${formatDate(b.collected_at)}</td>
                    <td>
                      ${b.status === 'collecting' ? `
                        <button class="btn btn-secondary btn-sm" data-batch-action="${b.id}" data-target-status="sealed">Seal Batch</button>
                      ` : ''}
                      ${b.status === 'sealed' ? `
                        <button class="btn btn-primary btn-sm" data-batch-action="${b.id}" data-target-status="in_transit">Start Transit</button>
                      ` : ''}
                      ${b.status === 'in_transit' ? `
                        <button class="btn btn-success btn-sm" data-batch-action="${b.id}" data-target-status="delivered">Mark Delivered</button>
                      ` : ''}
                      ${b.status === 'delivered' ? `
                        <span style="font-size: 0.8rem; color: var(--success);">Delivered</span>
                      ` : ''}
                    </td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        `}
      </div>

      <!-- Create Batch Modal -->
      ${this.state.showModal ? this.renderModal() : ''}
    `;

    this.attachEvents();
  }

  renderModal() {
    return `
      <div class="modal-overlay">
        <div class="modal-content">
          <div class="card-header">
            <h3 class="card-title">Create Waste Collection Batch</h3>
            <button class="btn btn-secondary btn-sm" id="btn-close-batch-modal">✕</button>
          </div>
          <form id="create-batch-form">
            <div class="form-group">
              <label class="form-label">Total Aggregated Waste Volume (m³) <span class="required">*</span></label>
              <input type="number" step="0.1" id="input-batch-vol" class="form-input" value="${this.state.inputVolume}" min="0.1" required />
            </div>
            <div class="form-group">
              <label class="form-label">Vehicle ID (Optional)</label>
              <input type="number" id="input-batch-vehicle" class="form-input" placeholder="e.g. 1" />
            </div>
            <button type="submit" class="btn btn-primary" style="width: 100%;" ${this.state.isSubmitting ? 'disabled' : ''}>
              ${this.state.isSubmitting ? 'Creating...' : '🚛 Create Collection Batch'}
            </button>
          </form>
        </div>
      </div>
    `;
  }

  attachEvents() {
    const btnRefresh = document.getElementById('btn-refresh-batch');
    if (btnRefresh) btnRefresh.addEventListener('click', () => this.loadData());

    const btnOpenModal = document.getElementById('btn-open-batch-modal');
    if (btnOpenModal) {
      btnOpenModal.addEventListener('click', () => {
        this.state.showModal = true;
        this.render();
      });
    }

    const btnCloseModal = document.getElementById('btn-close-batch-modal');
    if (btnCloseModal) {
      btnCloseModal.addEventListener('click', () => {
        this.state.showModal = false;
        this.render();
      });
    }

    this.container.querySelectorAll('[data-batch-action]').forEach(btn => {
      btn.addEventListener('click', async () => {
        const id = parseInt(btn.dataset.batchAction);
        const targetStatus = btn.dataset.targetStatus;
        try {
          await updateBatchStatus(id, { status: targetStatus });
          this.loadData();
        } catch (err) {
          alert(`Batch Status Update Error: ${err.message}`);
        }
      });
    });

    const form = document.getElementById('create-batch-form');
    if (form) {
      form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const vol = parseFloat(document.getElementById('input-batch-vol').value);
        const vehIdStr = document.getElementById('input-batch-vehicle').value;

        this.state.isSubmitting = true;
        this.render();

        try {
          await createCollectionBatch({
            total_volume_m3: vol,
            vehicle_id: vehIdStr ? parseInt(vehIdStr) : null,
          });
          this.state.isSubmitting = false;
          this.state.showModal = false;
          this.loadData();
        } catch (err) {
          this.state.isSubmitting = false;
          alert(`Create Batch Error: ${err.message}`);
          this.render();
        }
      });
    }
  }
}
