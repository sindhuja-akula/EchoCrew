import { WASTE_CATEGORIES, VOLUME_TIERS } from '../utils/constants.js';
import { validateReportForm } from '../utils/validation.js';
import { uploadReportPhoto, createReport } from '../services/reportsService.js';
import { formatCoordinates, getCategoryMeta, renderStatusBadge } from '../utils/formatters.js';

export class ReportForm {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.state = {
      imageFile: null,
      imagePreviewUrl: null,
      uploadedImageUrl: null,
      latitude: null,
      longitude: null,
      category: 'mixed',
      volume_tier: 'moderate',
      description: '',
      isLocating: false,
      isSubmitting: false,
      locationError: null,
      formErrors: [],
      successReport: null,
    };
  }

  render() {
    if (!this.container) return;

    if (this.state.successReport) {
      this.renderSuccess();
      return;
    }

    const categoryMeta = getCategoryMeta(this.state.category);

    this.container.innerHTML = `
      <div class="card" style="max-width: 680px; margin: 0 auto;">
        <div class="card-header">
          <div>
            <h2 class="card-title" style="font-size: 1.35rem;">🌊 Report Illegal Garbage Accumulation</h2>
            <p style="font-size: 0.88rem; color: var(--text-muted); margin-top: 4px;">
              Submit a geo-tagged report to municipal response crews.
            </p>
          </div>
        </div>

        ${this.state.formErrors.length > 0 ? `
          <div class="alert alert-danger">
            <div>
              <strong>Submission Error:</strong>
              <ul style="margin-left: 20px; margin-top: 4px;">
                ${this.state.formErrors.map(err => `<li>${err}</li>`).join('')}
              </ul>
            </div>
          </div>
        ` : ''}

        <form id="garbage-report-form">
          <!-- 1. Site Photo Upload / Camera Capture -->
          <div class="form-group">
            <label class="form-label">1. Garbage Site Photo <span class="required">*</span></label>
            ${!this.state.imagePreviewUrl ? `
              <div class="dropzone" onclick="document.getElementById('report-photo-input').click()">
                <div style="font-size: 2rem; margin-bottom: 8px;">📷</div>
                <div style="font-weight: 600; color: var(--text-primary);">Click to upload or take a photo</div>
                <div style="font-size: 0.78rem; color: var(--text-muted); margin-top: 4px;">
                  Supports JPG, PNG, WEBP up to 10 MB.
                </div>
                <input type="file" id="report-photo-input" accept="image/*" capture="environment" style="display: none;" />
              </div>
            ` : `
              <div class="preview-container">
                <img src="${this.state.imagePreviewUrl}" alt="Garbage Site Preview" class="preview-image" />
                <button type="button" class="btn-remove-photo" id="btn-remove-photo" title="Remove photo">✕</button>
              </div>
            `}
          </div>

          <!-- 2. Location Capture -->
          <div class="form-group">
            <label class="form-label">2. Accumulation Location <span class="required">*</span></label>
            <div style="display: flex; gap: 12px; align-items: center; flex-wrap: wrap;">
              <button type="button" id="btn-get-location" class="btn btn-secondary ${this.state.isLocating ? 'disabled' : ''}">
                ${this.state.isLocating ? '🔄 Acquiring GPS...' : '📍 Use My Current Location'}
              </button>
              <div style="font-size: 0.9rem; font-weight: 600; color: var(--primary);">
                ${formatCoordinates(this.state.latitude, this.state.longitude)}
              </div>
            </div>
            ${this.state.locationError ? `
              <div style="font-size: 0.82rem; color: var(--danger); margin-top: 6px;">
                ${this.state.locationError}
              </div>
            ` : ''}
          </div>

          <!-- 3. Waste Classification Category -->
          <div class="form-group">
            <label class="form-label">3. Waste Classification Category <span class="required">*</span></label>
            <div class="option-grid">
              ${WASTE_CATEGORIES.map(cat => `
                <div class="option-card ${this.state.category === cat.value ? 'selected' : ''}" data-category="${cat.value}">
                  <div class="option-icon">${cat.icon}</div>
                  <div class="option-title">${cat.label}</div>
                </div>
              `).join('')}
            </div>
            <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 6px;">
              Selected: <strong>${categoryMeta.label}</strong> — ${categoryMeta.description}
            </div>
          </div>

          <!-- 4. Estimated Volume Tier -->
          <div class="form-group">
            <label class="form-label">4. Estimated Volume Tier <span class="required">*</span></label>
            <div class="option-grid" style="grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));">
              ${VOLUME_TIERS.map(vol => `
                <div class="option-card ${this.state.volume_tier === vol.value ? 'selected' : ''}" data-volume="${vol.value}">
                  <div class="option-title" style="color: ${vol.color}; font-size: 1rem;">${vol.title}</div>
                  <div class="option-desc">${vol.desc}</div>
                </div>
              `).join('')}
            </div>
          </div>

          <!-- 5. Optional Description & Landmark Details -->
          <div class="form-group">
            <label class="form-label">5. Site Description & Nearby Landmarks <span style="font-weight: 400; color: var(--text-muted);">(Optional)</span></label>
            <textarea id="report-description" class="form-textarea" placeholder="e.g. Near bus stop on MG Road, spilling onto sidewalk...">${this.state.description}</textarea>
          </div>

          <!-- Submit Button -->
          <div style="margin-top: 24px;">
            <button type="submit" class="btn btn-primary" style="width: 100%; padding: 14px; font-size: 1.05rem;" ${this.state.isSubmitting ? 'disabled' : ''}>
              ${this.state.isSubmitting ? '🔄 Submitting Geo-Report...' : '🚀 Submit Garbage Report'}
            </button>
          </div>
        </form>
      </div>
    `;

    this.attachEvents();
  }

  attachEvents() {
    // Image selection handler
    const fileInput = document.getElementById('report-photo-input');
    if (fileInput) {
      fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
          this.state.imageFile = file;
          this.state.imagePreviewUrl = URL.createObjectURL(file);
          this.render();
        }
      });
    }

    // Remove photo handler
    const btnRemove = document.getElementById('btn-remove-photo');
    if (btnRemove) {
      btnRemove.addEventListener('click', () => {
        this.state.imageFile = null;
        this.state.imagePreviewUrl = null;
        this.render();
      });
    }

    // Geolocation handler
    const btnLocation = document.getElementById('btn-get-location');
    if (btnLocation) {
      btnLocation.addEventListener('click', () => {
        if (!navigator.geolocation) {
          this.state.locationError = 'Geolocation API is not supported by your browser.';
          this.render();
          return;
        }

        this.state.isLocating = true;
        this.state.locationError = null;
        this.render();

        navigator.geolocation.getCurrentPosition(
          (pos) => {
            this.state.latitude = pos.coords.latitude;
            this.state.longitude = pos.coords.longitude;
            this.state.isLocating = false;
            this.render();
          },
          (err) => {
            this.state.isLocating = false;
            this.state.locationError = `Location Error (${err.code}): ${err.message}. Please allow location access.`;
            this.render();
          },
          { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
        );
      });
    }

    // Category click handler
    this.container.querySelectorAll('[data-category]').forEach(card => {
      card.addEventListener('click', () => {
        this.state.category = card.dataset.category;
        this.render();
      });
    });

    // Volume click handler
    this.container.querySelectorAll('[data-volume]').forEach(card => {
      card.addEventListener('click', () => {
        this.state.volume_tier = card.dataset.volume;
        this.render();
      });
    });

    // Description text handler
    const descTextarea = document.getElementById('report-description');
    if (descTextarea) {
      descTextarea.addEventListener('input', (e) => {
        this.state.description = e.target.value;
      });
    }

    // Form submit handler
    const form = document.getElementById('garbage-report-form');
    if (form) {
      form.addEventListener('submit', async (e) => {
        e.preventDefault();
        await this.handleSubmit();
      });
    }
  }

  async handleSubmit() {
    const val = validateReportForm({
      latitude: this.state.latitude,
      longitude: this.state.longitude,
      category: this.state.category,
      volume_tier: this.state.volume_tier,
      imageFile: this.state.imageFile,
    });

    if (!val.valid) {
      this.state.formErrors = val.errors;
      this.render();
      return;
    }

    this.state.isSubmitting = true;
    this.state.formErrors = [];
    this.render();

    try {
      let photoUrl = null;
      if (this.state.imageFile) {
        const uploadRes = await uploadReportPhoto(this.state.imageFile);
        photoUrl = uploadRes.image_url;
      }

      const reportPayload = {
        description: this.state.description || null,
        latitude: parseFloat(this.state.latitude),
        longitude: parseFloat(this.state.longitude),
        category: this.state.category,
        volume_tier: this.state.volume_tier,
        image_url: photoUrl,
      };

      const responseReport = await createReport(reportPayload);
      this.state.isSubmitting = false;
      this.state.successReport = responseReport;
      this.render();
    } catch (err) {
      this.state.isSubmitting = false;
      this.state.formErrors = [err.message || 'Failed to submit report. Please try again.'];
      this.render();
    }
  }

  renderSuccess() {
    const report = this.state.successReport;
    const catMeta = getCategoryMeta(report.category);

    this.container.innerHTML = `
      <div class="card" style="max-width: 600px; margin: 0 auto; text-align: center;">
        <div style="font-size: 3.5rem; margin-bottom: 12px;">✅</div>
        <h2 style="font-size: 1.5rem; color: var(--success);">Garbage Report Submitted Successfully</h2>
        <p style="color: var(--text-secondary); margin-top: 6px; font-size: 0.95rem;">
          Report Reference ID: <strong>#${report.id}</strong>
        </p>

        ${report.is_spatial_duplicate ? `
          <div class="alert alert-warning" style="margin-top: 16px; text-align: left;">
            <div>
              <strong>📍 Spatial Deduplication Notice:</strong><br />
              This location is within 20 meters of an active report (#${report.duplicate_of_report_id}). Your report has been logged and linked to the primary response work order!
            </div>
          </div>
        ` : ''}

        <div style="background: var(--bg-input); border-radius: var(--radius-md); padding: 16px; margin: 20px 0; text-align: left; font-size: 0.9rem;">
          <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span style="color: var(--text-muted);">Status:</span>
            <span>${renderStatusBadge(report.status, 'report')}</span>
          </div>
          <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span style="color: var(--text-muted);">Category:</span>
            <span>${catMeta.icon} ${catMeta.label}</span>
          </div>
          <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span style="color: var(--text-muted);">Volume Tier:</span>
            <span style="font-weight: 600; text-transform: uppercase;">${report.volume_tier}</span>
          </div>
          <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span style="color: var(--text-muted);">Coordinates:</span>
            <span>${formatCoordinates(report.latitude, report.longitude)}</span>
          </div>
          ${report.description ? `
            <div style="margin-top: 8px; border-top: 1px solid var(--border-color); padding-top: 8px;">
              <span style="color: var(--text-muted);">Description:</span>
              <div style="margin-top: 2px;">${report.description}</div>
            </div>
          ` : ''}
        </div>

        ${report.image_url ? `
          <div style="margin-bottom: 20px; border-radius: var(--radius-md); overflow: hidden; max-height: 200px;">
            <img src="http://localhost:8000/${report.image_url}" alt="Submitted site photo" style="width: 100%; height: 200px; object-fit: cover;" />
          </div>
        ` : ''}

        <div style="display: flex; gap: 12px;">
          <button type="button" id="btn-new-report" class="btn btn-primary" style="flex: 1;">
            ➕ Submit Another Report
          </button>
          <button type="button" onclick="location.hash='#my-reports'" class="btn btn-secondary" style="flex: 1;">
            📋 View All Reports
          </button>
        </div>
      </div>
    `;

    const btnNew = document.getElementById('btn-new-report');
    if (btnNew) {
      btnNew.addEventListener('click', () => {
        this.state.successReport = null;
        this.state.imageFile = null;
        this.state.imagePreviewUrl = null;
        this.state.uploadedImageUrl = null;
        this.state.description = '';
        this.render();
      });
    }
  }
}
