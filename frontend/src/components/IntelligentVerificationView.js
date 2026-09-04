import { IntelligentVerificationService } from '../services/intelligentVerificationService.js';

export class IntelligentVerificationView {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
    }

    async render() {
        this.container.innerHTML = `
            <div class="card fade-in">
                <h2>🤖 Intelligent Verification Sandbox</h2>
                <p>Test the AI verification scoring directly.</p>
                <form id="ai-verification-form">
                    <div class="form-group">
                        <label>Report ID</label>
                        <input type="number" id="ai-report-id" required>
                    </div>
                    <div class="form-group">
                        <label>Assignment ID</label>
                        <input type="number" id="ai-assignment-id" required>
                    </div>
                    <div class="form-group">
                        <label>Evidence ID</label>
                        <input type="number" id="ai-evidence-id" required>
                    </div>
                    <button type="submit" class="btn btn-primary">Analyze</button>
                </form>
                <div id="ai-result-panel" style="margin-top:20px; display:none;">
                    <!-- Results will be injected here -->
                </div>
            </div>
        `;

        document.getElementById('ai-verification-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const reportId = document.getElementById('ai-report-id').value;
            const assignmentId = document.getElementById('ai-assignment-id').value;
            const evidenceId = document.getElementById('ai-evidence-id').value;
            const panel = document.getElementById('ai-result-panel');
            
            try {
                const res = await IntelligentVerificationService.analyze(reportId, assignmentId, evidenceId);
                panel.style.display = 'block';
                panel.innerHTML = `
                    <h3>Analysis Result</h3>
                    <p><strong>Score:</strong> ${res.correspondence_score.toFixed(1)}%</p>
                    <p><strong>Recommendation:</strong> <span class="badge ${res.recommended_status === 'approved' ? 'badge-success' : 'badge-warning'}">${res.recommended_status}</span></p>
                    <p><strong>Location Match:</strong> ${res.location_match ? '✅' : '❌'} (${res.distance_meters.toFixed(1)}m distance)</p>
                    <p><strong>Time Match:</strong> ${res.time_match ? '✅' : '❌'} (${res.time_delta_minutes.toFixed(1)} mins delta)</p>
                `;
            } catch (err) {
                panel.style.display = 'block';
                panel.innerHTML = `<div class="alert alert-danger">${err.message}</div>`;
            }
        });
    }
}
