import { listVerifications, submitVerification } from '../services/verificationService.js';
import { listEvidence } from '../services/evidenceService.js';
import { formatDate, renderStatusBadge } from '../utils/formatters.js';

export class VerificationView {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.state = {
      verifications: [],
      evidenceItems: [],
      loading: true,
      error: null,
      showReviewModal: false,
      selectedUnitId: 1,
      selectedEvidenceId: null,
      notes: '',
      isSubmitting: false,
    };
  }

  async loadData() {
    this.state.loading = true;
    this.state.error = null;
    this.render();

    try {
      const [verRes, evRes] = await Promise.all([
        listVerifications(),
        listEvidence(),
      ]);
      this.state.verifications = verRes || [];
      this.state.evidenceItems = evRes || [];
      this.state.loading = false;
      this.render();
    } catch (err) {
      this.state.loading = false;
      this.state.error = err.message || 'Failed to load verifications';
      this.render();
    }
  }

  render() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div class="card">
        <div class="card-header" style="flex-wrap: wrap; gap: 12px;">
          <div>
            <h2 class="card-title">✅ Quality Verification & Audit Review</h2>
            <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 2px;">
              Supervisor review of worker cleaning evidence. Approval automatically triggers worker compensation eligibility.
            </p>
          </div>
          <div style="display: flex; gap: 8px;">
            <button class="btn btn-primary btn-sm" id="btn-open-verify-modal">🔍 Perform Audit Decision</button>
            <button class="btn btn-secondary btn-sm" id="btn-refresh-verify">🔄 Refresh</button>
          </div>
        </div>

        ${this.state.error ? `<div class="alert alert-danger">${this.state.error}</div>` : ''}

        ${this.state.loading ? `
          <div style="text-align: center; padding: 40px; color: var(--text-muted);">🔄 Loading verifications...</div>
        ` : `
          <!-- Submitted Evidence Gallery -->
          <div style="margin-bottom: 24px;">
            <h3 style="font-size: 1rem; margin-bottom: 12px; color: var(--text-secondary);">Submitted Photo Evidence Gallery (${this.state.evidenceItems.length})</h3>
            ${this.state.evidenceItems.length === 0 ? `
              <div style="color: var(--text-muted); font-size: 0.85rem;">No evidence photos uploaded yet.</div>
            ` : `
              <div class="grid grid-3">
                ${this.state.evidenceItems.map(ev => `
                  <div class="card" style="padding: 12px; background: var(--bg-input);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                      <span class="badge" style="background: var(--primary-light); color: var(--primary); text-transform: uppercase;">${ev.evidence_type}</span>
                      <span style="font-size: 0.78rem; color: var(--text-muted);">Unit #${ev.work_unit_id}</span>
                    </div>
                    <img src="http://localhost:8000/${ev.image_url}" alt="Evidence" style="width: 100%; height: 160px; object-fit: cover; border-radius: var(--radius-sm);" />
                    <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 6px;">
                      Submitted: ${formatDate(ev.captured_at)}
                    </div>
                  </div>
                `).join('')}
              </div>
            `}
          </div>

          <!-- Verifications Table -->
          <h3 style="font-size: 1rem; margin-bottom: 12px; color: var(--text-secondary);">Audit Trail History (${this.state.verifications.length})</h3>
          ${this.state.verifications.length === 0 ? `
            <div style="color: var(--text-muted); font-size: 0.85rem;">No verification decisions logged yet.</div>
          ` : `
            <div class="table-responsive">
              <table class="table">
                <thead>
                  <tr>
                    <th>Verification ID</th>
                    <th>Work Unit ID</th>
                    <th>Evidence ID</th>
                    <th>Decision</th>
                    <th>Method</th>
                    <th>Notes</th>
                    <th>Verified At</th>
                  </tr>
                </thead>
                <tbody>
                  ${this.state.verifications.map(v => `
                    <tr>
                      <td><strong>#${v.id}</strong></td>
                      <td>Unit #${v.work_unit_id}</td>
                      <td>${v.evidence_id ? `#${v.evidence_id}` : 'None'}</td>
                      <td>${renderStatusBadge(v.status, 'verification')}</td>
                      <td><span style="text-transform: uppercase; font-size: 0.8rem; font-weight: 600;">${v.method}</span></td>
                      <td>${v.notes || '—'}</td>
                      <td>${formatDate(v.verified_at)}</td>
                    </tr>
                  `).join('')}
                </tbody>
              </table>
            </div>
          `}
        `}
      </div>

      <!-- Verification Modal -->
      ${this.state.showReviewModal ? this.renderModal() : ''}
    `;

    this.attachEvents();
  }

  renderModal() {
    return `
      <div class="modal-overlay">
        <div class="modal-content">
          <div class="card-header">
            <h3 class="card-title">Submit Verification Audit Decision</h3>
            <button class="btn btn-secondary btn-sm" id="btn-close-verify-modal">✕</button>
          </div>
          <form id="verify-form">
            <div class="form-group">
              <label class="form-label">Work Unit ID <span class="required">*</span></label>
              <input type="number" id="input-verify-unit" class="form-input" value="${this.state.selectedUnitId}" required />
            </div>
            <div class="form-group">
              <label class="form-label">Evidence ID (Optional)</label>
              <select id="select-verify-evidence" class="form-select">
                <option value="">-- None / General Review --</option>
                ${this.state.evidenceItems.map(ev => `
                  <option value="${ev.id}">Evidence #${ev.id} (Unit #${ev.work_unit_id} - ${ev.evidence_type.toUpperCase()})</option>
                `).join('')}
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">Supervisor Audit Notes</label>
              <textarea id="input-verify-notes" class="form-textarea" placeholder="e.g. Inspected site, waste completely cleared and area sanitized..."></textarea>
            </div>
            <div style="display: flex; gap: 12px;">
              <button type="button" id="btn-approve" class="btn btn-success" style="flex: 1;" ${this.state.isSubmitting ? 'disabled' : ''}>
                ✅ APPROVE & TRIGGER PAYOUT
              </button>
              <button type="button" id="btn-reject" class="btn btn-danger" style="flex: 1;" ${this.state.isSubmitting ? 'disabled' : ''}>
                ❌ REJECT WORK
              </button>
            </div>
          </form>
        </div>
      </div>
    `;
  }

  attachEvents() {
    const btnRefresh = document.getElementById('btn-refresh-verify');
    if (btnRefresh) btnRefresh.addEventListener('click', () => this.loadData());

    const btnOpenModal = document.getElementById('btn-open-verify-modal');
    if (btnOpenModal) {
      btnOpenModal.addEventListener('click', () => {
        this.state.showReviewModal = true;
        this.render();
      });
    }

    const btnCloseModal = document.getElementById('btn-close-verify-modal');
    if (btnCloseModal) {
      btnCloseModal.addEventListener('click', () => {
        this.state.showReviewModal = false;
        this.render();
      });
    }

    const btnApprove = document.getElementById('btn-approve');
    if (btnApprove) {
      btnApprove.addEventListener('click', async () => {
        await this.handleDecision('approved');
      });
    }

    const btnReject = document.getElementById('btn-reject');
    if (btnReject) {
      btnReject.addEventListener('click', async () => {
        await this.handleDecision('rejected');
      });
    }
  }

  async handleDecision(decisionStatus) {
    const unitId = parseInt(document.getElementById('input-verify-unit').value);
    const evSel = document.getElementById('select-verify-evidence').value;
    const notes = document.getElementById('input-verify-notes').value;

    this.state.isSubmitting = true;
    this.render();

    try {
      await submitVerification({
        work_unit_id: unitId,
        evidence_id: evSel ? parseInt(evSel) : null,
        status: decisionStatus,
        method: 'supervisor',
        notes: notes || null,
      });

      this.state.isSubmitting = false;
      this.state.showReviewModal = false;
      this.loadData();
    } catch (err) {
      this.state.isSubmitting = false;
      alert(`Verification Error: ${err.message}`);
      this.render();
    }
  }
}
