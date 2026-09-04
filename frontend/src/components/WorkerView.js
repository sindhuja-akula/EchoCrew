import { listAssignments, updateAssignmentStatus } from '../services/assignmentsService.js';
import { uploadReportPhoto } from '../services/reportsService.js';
import { submitEvidence } from '../services/evidenceService.js';
import { formatDate, renderStatusBadge } from '../utils/formatters.js';

export class WorkerView {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.state = {
      workerId: 1,
      assignments: [],
      loading: true,
      error: null,
      showEvidenceModal: false,
      selectedAssignment: null,
      evidenceType: 'after',
      evidenceFile: null,
      evidencePreviewUrl: null,
      isSubmitting: false,
    };
  }

  async loadData() {
    this.state.loading = true;
    this.state.error = null;
    this.render();

    try {
      const res = await listAssignments({ worker_id: this.state.workerId });
      this.state.assignments = res || [];
      this.state.loading = false;
      this.render();
    } catch (err) {
      this.state.loading = false;
      this.state.error = err.message || 'Failed to load assigned jobs';
      this.render();
    }
  }

  render() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div class="card" style="max-width: 680px; margin: 0 auto;">
        <div class="card-header" style="flex-wrap: wrap; gap: 12px;">
          <div>
            <h2 class="card-title">📱 Responder Mobile Field Portal</h2>
            <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 2px;">
              View assigned cleanup work units, transition job state, and upload photo proof.
            </p>
          </div>
          <div style="display: flex; gap: 8px; align-items: center;">
            <span style="font-size: 0.85rem; font-weight: 600;">Worker ID:</span>
            <input type="number" id="input-active-worker-id" class="form-input" value="${this.state.workerId}" style="width: 80px; padding: 4px 8px;" />
            <button class="btn btn-secondary btn-sm" id="btn-refresh-worker-jobs">🔄 Sync</button>
          </div>
        </div>

        ${this.state.error ? `<div class="alert alert-danger">${this.state.error}</div>` : ''}

        ${this.state.loading ? `
          <div style="text-align: center; padding: 40px; color: var(--text-muted);">🔄 Syncing field jobs from backend...</div>
        ` : this.state.assignments.length === 0 ? `
          <div style="text-align: center; padding: 40px; color: var(--text-muted);">
            No assigned cleanup jobs for Worker #${this.state.workerId}.
          </div>
        ` : `
          <div class="grid grid-1" style="gap: 16px;">
            ${this.state.assignments.map(a => `
              <div class="card" style="background: var(--bg-input); border-left: 4px solid var(--primary);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                  <span style="font-weight: 700; font-size: 1.05rem;">Work Unit #${a.work_unit_id}</span>
                  ${renderStatusBadge(a.status, 'assignment')}
                </div>
                <div style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 12px;">
                  Parent Work Order: #${a.work_order_id} | Assigned: ${formatDate(a.assigned_at)}
                </div>

                <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                  ${a.status === 'assigned' ? `
                    <button class="btn btn-primary btn-sm" data-worker-action="${a.id}" data-target-status="accepted">
                      👍 Accept Job
                    </button>
                  ` : ''}

                  ${a.status === 'accepted' ? `
                    <button class="btn btn-primary btn-sm" data-worker-action="${a.id}" data-target-status="in_progress">
                      ▶️ Start Cleanup Work
                    </button>
                  ` : ''}

                  ${a.status === 'in_progress' ? `
                    <button class="btn btn-secondary btn-sm" data-upload-evidence-modal="${a.id}">
                      📷 Upload Photo Proof
                    </button>
                    <button class="btn btn-success btn-sm" data-worker-action="${a.id}" data-target-status="completed">
                      ✅ Mark Work Completed
                    </button>
                  ` : ''}

                  ${a.status === 'completed' ? `
                    <span style="font-size: 0.85rem; color: var(--success); font-weight: 600;">Work Completed & Submitted for Audit</span>
                  ` : ''}
                </div>
              </div>
            `).join('')}
          </div>
        `}
      </div>

      <!-- Upload Evidence Modal -->
      ${this.state.showEvidenceModal ? this.renderEvidenceModal() : ''}
    `;

    this.attachEvents();
  }

  renderEvidenceModal() {
    const a = this.state.selectedAssignment;
    return `
      <div class="modal-overlay">
        <div class="modal-content">
          <div class="card-header">
            <h3 class="card-title">Upload Cleaning Proof Photo</h3>
            <button class="btn btn-secondary btn-sm" id="btn-close-ev-modal">✕</button>
          </div>
          <form id="upload-ev-form">
            <div class="form-group">
              <label class="form-label">Evidence Phase</label>
              <select id="select-ev-type" class="form-select">
                <option value="before">BEFORE Cleanup</option>
                <option value="progress">PROGRESS (In-between)</option>
                <option value="after" selected>AFTER Cleanup</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">Photo Capture <span class="required">*</span></label>
              ${!this.state.evidencePreviewUrl ? `
                <div class="dropzone" onclick="document.getElementById('worker-ev-photo-input').click()">
                  <div style="font-size: 2rem;">📷</div>
                  <div style="font-weight: 600;">Click or capture photo</div>
                  <input type="file" id="worker-ev-photo-input" accept="image/*" capture="environment" style="display: none;" />
                </div>
              ` : `
                <div class="preview-container">
                  <img src="${this.state.evidencePreviewUrl}" class="preview-image" alt="Evidence preview" />
                  <button type="button" class="btn-remove-photo" id="btn-remove-ev-photo">✕</button>
                </div>
              `}
            </div>
            <button type="submit" class="btn btn-primary" style="width: 100%;" ${this.state.isSubmitting ? 'disabled' : ''}>
              ${this.state.isSubmitting ? 'Uploading Proof...' : '🚀 Submit Photo Evidence'}
            </button>
          </form>
        </div>
      </div>
    `;
  }

  attachEvents() {
    const btnRefresh = document.getElementById('btn-refresh-worker-jobs');
    if (btnRefresh) {
      btnRefresh.addEventListener('click', () => {
        const idInput = document.getElementById('input-active-worker-id');
        if (idInput) this.state.workerId = parseInt(idInput.value) || 1;
        this.loadData();
      });
    }

    this.container.querySelectorAll('[data-worker-action]').forEach(btn => {
      btn.addEventListener('click', async () => {
        const id = parseInt(btn.dataset.workerAction);
        const targetStatus = btn.dataset.targetStatus;
        try {
          await updateAssignmentStatus(id, { status: targetStatus });
          this.loadData();
        } catch (err) {
          alert(`Status Update Error: ${err.message}`);
        }
      });
    });

    this.container.querySelectorAll('[data-upload-evidence-modal]').forEach(btn => {
      btn.addEventListener('click', () => {
        const id = parseInt(btn.dataset.uploadEvidenceModal);
        const found = this.state.assignments.find(a => a.id === id);
        if (found) {
          this.state.selectedAssignment = found;
          this.state.showEvidenceModal = true;
          this.state.evidenceFile = null;
          this.state.evidencePreviewUrl = null;
          this.render();
        }
      });
    });

    const btnCloseModal = document.getElementById('btn-close-ev-modal');
    if (btnCloseModal) {
      btnCloseModal.addEventListener('click', () => {
        this.state.showEvidenceModal = false;
        this.render();
      });
    }

    const evFileInput = document.getElementById('worker-ev-photo-input');
    if (evFileInput) {
      evFileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
          this.state.evidenceFile = file;
          this.state.evidencePreviewUrl = URL.createObjectURL(file);
          this.render();
        }
      });
    }

    const btnRemoveEv = document.getElementById('btn-remove-ev-photo');
    if (btnRemoveEv) {
      btnRemoveEv.addEventListener('click', () => {
        this.state.evidenceFile = null;
        this.state.evidencePreviewUrl = null;
        this.render();
      });
    }

    const evForm = document.getElementById('upload-ev-form');
    if (evForm) {
      evForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        if (!this.state.evidenceFile) {
          alert('Please select or capture a photo first.');
          return;
        }

        const evType = document.getElementById('select-ev-type').value;
        const assignment = this.state.selectedAssignment;

        this.state.isSubmitting = true;
        this.render();

        try {
          const uploadRes = await uploadReportPhoto(this.state.evidenceFile);
          await submitEvidence({
            work_unit_id: assignment.work_unit_id,
            work_assignment_id: assignment.id,
            evidence_type: evType,
            image_url: uploadRes.image_url,
          });

          this.state.isSubmitting = false;
          this.state.showEvidenceModal = false;
          alert('Evidence photo submitted successfully!');
          this.loadData();
        } catch (err) {
          this.state.isSubmitting = false;
          alert(`Submit Evidence Error: ${err.message}`);
          this.render();
        }
      });
    }
  }
}
