import { listAssignments, createAssignment, updateAssignmentStatus } from '../services/assignmentsService.js';
import { listWorkers, createWorker } from '../services/workersService.js';
import { formatDate, renderStatusBadge } from '../utils/formatters.js';

export class AssignmentsView {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.state = {
      assignments: [],
      workers: [],
      loading: true,
      error: null,
      showAssignModal: false,
      showWorkerModal: false,
      inputWorkerId: '',
      inputWorkUnitId: '',
      newWorkerPhone: '',
      isSubmitting: false,
    };
  }

  async loadData() {
    this.state.loading = true;
    this.state.error = null;
    this.render();

    try {
      const [assignRes, workersRes] = await Promise.all([
        listAssignments(),
        listWorkers(),
      ]);
      this.state.assignments = assignRes || [];
      this.state.workers = workersRes[1] || workersRes || [];
      this.state.loading = false;
      this.render();
    } catch (err) {
      this.state.loading = false;
      this.state.error = err.message || 'Failed to load assignments';
      this.render();
    }
  }

  render() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div class="card">
        <div class="card-header" style="flex-wrap: wrap; gap: 12px;">
          <div>
            <h2 class="card-title">👷 Worker Assignment & Field Dispatch</h2>
            <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 2px;">
              Link registered sanitation workers to specific work units & track job lifecycle state.
            </p>
          </div>
          <div style="display: flex; gap: 8px;">
            <button class="btn btn-secondary btn-sm" id="btn-open-worker-modal">👤 Register Worker</button>
            <button class="btn btn-primary btn-sm" id="btn-open-assign-modal">➕ Assign Worker</button>
            <button class="btn btn-secondary btn-sm" id="btn-refresh-assign">🔄 Refresh</button>
          </div>
        </div>

        ${this.state.error ? `<div class="alert alert-danger">${this.state.error}</div>` : ''}

        ${this.state.loading ? `
          <div style="text-align: center; padding: 40px; color: var(--text-muted);">🔄 Loading worker assignments...</div>
        ` : this.state.assignments.length === 0 ? `
          <div style="text-align: center; padding: 40px; color: var(--text-muted);">No worker assignments found.</div>
        ` : `
          <div class="table-responsive">
            <table class="table">
              <thead>
                <tr>
                  <th>Assign ID</th>
                  <th>Worker ID</th>
                  <th>Work Unit ID</th>
                  <th>Work Order ID</th>
                  <th>Status</th>
                  <th>Assigned At</th>
                  <th>State Controls</th>
                </tr>
              </thead>
              <tbody>
                ${this.state.assignments.map(a => `
                  <tr>
                    <td><strong>#${a.id}</strong></td>
                    <td>Worker #${a.worker_id}</td>
                    <td>Unit #${a.work_unit_id}</td>
                    <td>Order #${a.work_order_id}</td>
                    <td>${renderStatusBadge(a.status, 'assignment')}</td>
                    <td>${formatDate(a.assigned_at)}</td>
                    <td>
                      ${a.status === 'assigned' ? `
                        <button class="btn btn-secondary btn-sm" data-status-action="${a.id}" data-target-status="accepted">Accept</button>
                      ` : ''}
                      ${a.status === 'accepted' ? `
                        <button class="btn btn-primary btn-sm" data-status-action="${a.id}" data-target-status="in_progress">Start Work</button>
                      ` : ''}
                      ${a.status === 'in_progress' ? `
                        <button class="btn btn-success btn-sm" data-status-action="${a.id}" data-target-status="completed">Complete</button>
                      ` : ''}
                      ${a.status !== 'completed' && a.status !== 'cancelled' ? `
                        <button class="btn btn-danger btn-sm" data-status-action="${a.id}" data-target-status="cancelled">Cancel</button>
                      ` : ''}
                      ${a.status === 'completed' ? `<span style="font-size: 0.8rem; color: var(--success);">Done</span>` : ''}
                    </td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        `}
      </div>

      <!-- Assign Worker Modal -->
      ${this.state.showAssignModal ? this.renderAssignModal() : ''}

      <!-- Register Worker Modal -->
      ${this.state.showWorkerModal ? this.renderWorkerModal() : ''}
    `;

    this.attachEvents();
  }

  renderAssignModal() {
    return `
      <div class="modal-overlay">
        <div class="modal-content">
          <div class="card-header">
            <h3 class="card-title">Assign Worker to Work Unit</h3>
            <button class="btn btn-secondary btn-sm" id="btn-close-assign-modal">✕</button>
          </div>
          <form id="assign-form">
            <div class="form-group">
              <label class="form-label">Select Registered Worker <span class="required">*</span></label>
              <select id="select-worker-id" class="form-select" required>
                <option value="">-- Choose Worker --</option>
                ${this.state.workers.map(w => `
                  <option value="${w.id}">Worker #${w.id} (${w.worker_code} - ${w.phone || 'No Phone'}) [Status: ${w.status}]</option>
                `).join('')}
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">Work Unit ID <span class="required">*</span></label>
              <input type="number" id="input-unit-id" class="form-input" placeholder="e.g. 1" required />
            </div>
            <button type="submit" class="btn btn-primary" style="width: 100%;" ${this.state.isSubmitting ? 'disabled' : ''}>
              ${this.state.isSubmitting ? 'Assigning...' : '🚀 Create Assignment'}
            </button>
          </form>
        </div>
      </div>
    `;
  }

  renderWorkerModal() {
    return `
      <div class="modal-overlay">
        <div class="modal-content">
          <div class="card-header">
            <h3 class="card-title">Register New Worker Profile</h3>
            <button class="btn btn-secondary btn-sm" id="btn-close-worker-modal">✕</button>
          </div>
          <form id="register-worker-form">
            <div class="form-group">
              <label class="form-label">Worker Phone Number <span class="required">*</span></label>
              <input type="text" id="input-worker-phone" class="form-input" placeholder="+919876543210" required />
            </div>
            <button type="submit" class="btn btn-primary" style="width: 100%;" ${this.state.isSubmitting ? 'disabled' : ''}>
              ${this.state.isSubmitting ? 'Registering...' : '👤 Register Worker'}
            </button>
          </form>
        </div>
      </div>
    `;
  }

  attachEvents() {
    const btnRefresh = document.getElementById('btn-refresh-assign');
    if (btnRefresh) btnRefresh.addEventListener('click', () => this.loadData());

    const btnOpenAssign = document.getElementById('btn-open-assign-modal');
    if (btnOpenAssign) {
      btnOpenAssign.addEventListener('click', () => {
        this.state.showAssignModal = true;
        this.render();
      });
    }

    const btnCloseAssign = document.getElementById('btn-close-assign-modal');
    if (btnCloseAssign) {
      btnCloseAssign.addEventListener('click', () => {
        this.state.showAssignModal = false;
        this.render();
      });
    }

    const btnOpenWorker = document.getElementById('btn-open-worker-modal');
    if (btnOpenWorker) {
      btnOpenWorker.addEventListener('click', () => {
        this.state.showWorkerModal = true;
        this.render();
      });
    }

    const btnCloseWorker = document.getElementById('btn-close-worker-modal');
    if (btnCloseWorker) {
      btnCloseWorker.addEventListener('click', () => {
        this.state.showWorkerModal = false;
        this.render();
      });
    }

    // Status transition action handlers
    this.container.querySelectorAll('[data-status-action]').forEach(btn => {
      btn.addEventListener('click', async () => {
        const id = parseInt(btn.dataset.statusAction);
        const targetStatus = btn.dataset.targetStatus;
        try {
          await updateAssignmentStatus(id, { status: targetStatus });
          this.loadData();
        } catch (err) {
          alert(`Status Transition Error: ${err.message}`);
        }
      });
    });

    const assignForm = document.getElementById('assign-form');
    if (assignForm) {
      assignForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const wId = parseInt(document.getElementById('select-worker-id').value);
        const uId = parseInt(document.getElementById('input-unit-id').value);

        this.state.isSubmitting = true;
        this.render();

        try {
          await createAssignment({ worker_id: wId, work_unit_id: uId });
          this.state.isSubmitting = false;
          this.state.showAssignModal = false;
          this.loadData();
        } catch (err) {
          this.state.isSubmitting = false;
          alert(`Assignment Error: ${err.message}`);
          this.render();
        }
      });
    }

    const workerForm = document.getElementById('register-worker-form');
    if (workerForm) {
      workerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const phone = document.getElementById('input-worker-phone').value;

        this.state.isSubmitting = true;
        this.render();

        try {
          await createWorker({ phone });
          this.state.isSubmitting = false;
          this.state.showWorkerModal = false;
          this.loadData();
        } catch (err) {
          this.state.isSubmitting = false;
          alert(`Register Worker Error: ${err.message}`);
          this.render();
        }
      });
    }
  }
}
