import { listReports } from '../services/reportsService.js';
import { listWorkOrders } from '../services/workOrdersService.js';
import { listAssignments } from '../services/assignmentsService.js';
import { listVerifications } from '../services/verificationService.js';
import { listCompensations } from '../services/compensationService.js';
import { listBatches } from '../services/collectionService.js';
import { listAuditLogs } from '../services/auditService.js';
import { formatDate } from '../utils/formatters.js';

export class SupervisorDashboard {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.state = {
      loading: true,
      error: null,
      stats: {
        totalReports: 0,
        openWorkOrders: 0,
        activeAssignments: 0,
        pendingVerifications: 0,
        eligibleCompensations: 0,
        totalCollectionVolume: 0,
      },
      recentAudits: [],
    };
  }

  async loadData() {
    this.state.loading = true;
    this.state.error = null;
    this.render();

    try {
      const [reportsRes, ordersRes, assignRes, verRes, compRes, batchRes, auditRes] = await Promise.allSettled([
        listReports(),
        listWorkOrders(),
        listAssignments(),
        listVerifications(),
        listCompensations(),
        listBatches(),
        listAuditLogs({ limit: 5 }),
      ]);

      const reports = reportsRes.status === 'fulfilled' ? reportsRes.value.reports || [] : [];
      const orders = ordersRes.status === 'fulfilled' ? ordersRes.value || [] : [];
      const assignments = assignRes.status === 'fulfilled' ? assignRes.value || [] : [];
      const verifications = verRes.status === 'fulfilled' ? verRes.value || [] : [];
      const compensations = compRes.status === 'fulfilled' ? compRes.value || [] : [];
      const batches = batchRes.status === 'fulfilled' ? batchRes.value || [] : [];
      const audits = auditRes.status === 'fulfilled' ? auditRes.value[1] || [] : [];

      const totalVol = batches.reduce((acc, b) => acc + (b.total_volume_m3 || 0), 0);

      this.state.stats = {
        totalReports: reports.length,
        openWorkOrders: orders.filter(o => o.status === 'open').length,
        activeAssignments: assignments.filter(a => a.status === 'assigned' || a.status === 'in_progress').length,
        pendingVerifications: verifications.filter(v => v.status === 'pending').length,
        eligibleCompensations: compensations.filter(c => c.status === 'eligible').length,
        totalCollectionVolume: totalVol.toFixed(1),
      };

      this.state.recentAudits = audits;
      this.state.loading = false;
      this.render();
    } catch (err) {
      this.state.loading = false;
      this.state.error = err.message || 'Failed to load telemetry stats';
      this.render();
    }
  }

  render() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div>
        <div style="margin-bottom: 20px;">
          <h1 style="font-size: 1.6rem; font-weight: 700;">📊 Operational Command Dashboard</h1>
          <p style="color: var(--text-muted); font-size: 0.9rem;">
            Real-time urban waste recovery telemetry and response coordination hub.
          </p>
        </div>

        ${this.state.error ? `
          <div class="alert alert-danger">${this.state.error}</div>
        ` : ''}

        ${this.state.loading ? `
          <div style="text-align: center; padding: 40px; color: var(--text-muted);">
            🔄 Aggregating live PostGIS operational telemetry...
          </div>
        ` : `
          <!-- Telemetry Stat Cards -->
          <div class="grid grid-4" style="margin-bottom: 24px;">
            <div class="card" onclick="location.hash='#reports'" style="cursor: pointer;">
              <div style="font-size: 0.8rem; color: var(--text-muted);">Total Incidents Reported</div>
              <div style="font-size: 2rem; font-weight: 700; color: var(--primary); margin-top: 4px;">
                ${this.state.stats.totalReports}
              </div>
              <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 4px;">Geo-tagged citizen reports</div>
            </div>

            <div class="card" onclick="location.hash='#work-orders'" style="cursor: pointer;">
              <div style="font-size: 0.8rem; color: var(--text-muted);">Open Work Orders</div>
              <div style="font-size: 2rem; font-weight: 700; color: var(--warning); margin-top: 4px;">
                ${this.state.stats.openWorkOrders}
              </div>
              <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 4px;">Pending crew dispatch</div>
            </div>

            <div class="card" onclick="location.hash='#assignments'" style="cursor: pointer;">
              <div style="font-size: 0.8rem; color: var(--text-muted);">Active Field Jobs</div>
              <div style="font-size: 2rem; font-weight: 700; color: #8b5cf6; margin-top: 4px;">
                ${this.state.stats.activeAssignments}
              </div>
              <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 4px;">Assigned / In-progress crews</div>
            </div>

            <div class="card" onclick="location.hash='#verifications'" style="cursor: pointer;">
              <div style="font-size: 0.8rem; color: var(--text-muted);">Pending Verifications</div>
              <div style="font-size: 2rem; font-weight: 700; color: var(--success); margin-top: 4px;">
                ${this.state.stats.pendingVerifications}
              </div>
              <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 4px;">Evidence photos awaiting review</div>
            </div>
          </div>

          <div class="grid grid-2">
            <!-- Recent Audit Logs -->
            <div class="card">
              <div class="card-header">
                <h3 class="card-title">📜 Recent Operational Audit Logs</h3>
                <button class="btn btn-secondary btn-sm" onclick="location.hash='#audit'">View All</button>
              </div>
              ${this.state.recentAudits.length === 0 ? `
                <div style="color: var(--text-muted); font-size: 0.85rem; padding: 12px 0;">No recent audit logs recorded.</div>
              ` : `
                <div class="table-responsive">
                  <table class="table">
                    <thead>
                      <tr>
                        <th>Action</th>
                        <th>Target Entity</th>
                        <th>Timestamp</th>
                      </tr>
                    </thead>
                    <tbody>
                      ${this.state.recentAudits.map(a => `
                        <tr>
                          <td><span class="badge" style="background: rgba(255,255,255,0.08);">${a.action}</span></td>
                          <td>${a.entity_type} #${a.entity_id || 'N/A'}</td>
                          <td style="font-size: 0.8rem;">${formatDate(a.created_at)}</td>
                        </tr>
                      `).join('')}
                    </tbody>
                  </table>
                </div>
              `}
            </div>

            <!-- Operational Shortcuts -->
            <div class="card">
              <h3 class="card-title" style="margin-bottom: 16px;">⚡ Dispatch Quick Actions</h3>
              <div style="display: flex; flex-direction: column; gap: 12px;">
                <button class="btn btn-primary" onclick="location.hash='#reports'">
                  📋 Review Reports & Create Work Orders
                </button>
                <button class="btn btn-secondary" onclick="location.hash='#assignments'">
                  👷 Assign Cleanup Responders
                </button>
                <button class="btn btn-secondary" onclick="location.hash='#verifications'">
                  ✅ Review Evidence & Verify Cleanup
                </button>
                <button class="btn btn-secondary" onclick="location.hash='#collections'">
                  🚛 Track Waste Collection Batches (${this.state.stats.totalCollectionVolume} m³)
                </button>
              </div>
            </div>
          </div>
        `}
      </div>
    `;
  }
}
