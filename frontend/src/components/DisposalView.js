import { DisposalService } from '../services/disposalService.js';

export class DisposalView {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
    }

    async render() {
        this.container.innerHTML = `
            <div class="card fade-in">
                <h2>♻️ Waste Segregation & Disposal</h2>
                <div class="grid" style="margin-bottom: 20px;">
                    <div class="card">
                        <h3>Analytics</h3>
                        <div id="d-analytics">Loading...</div>
                    </div>
                </div>
                
                <form id="disposal-form">
                    <div class="form-group">
                        <label>Weighment ID</label>
                        <input type="number" id="d-weighment-id" required>
                    </div>
                    <div class="form-group">
                        <label>Facility Name</label>
                        <input type="text" id="d-facility-name" required>
                    </div>
                    <div class="form-group">
                        <label>Facility Type</label>
                        <select id="d-facility-type" required>
                            <option value="recycling_plant">Recycling Plant</option>
                            <option value="composting_facility">Composting Facility</option>
                            <option value="waste_to_energy">Waste to Energy</option>
                            <option value="sanitary_landfill">Sanitary Landfill</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Recycled Weight (kg)</label>
                        <input type="number" id="d-recycled" step="0.1" value="0" required>
                    </div>
                    <div class="form-group">
                        <label>Composted Weight (kg)</label>
                        <input type="number" id="d-composted" step="0.1" value="0" required>
                    </div>
                    <div class="form-group">
                        <label>Landfill Weight (kg)</label>
                        <input type="number" id="d-landfill" step="0.1" value="0" required>
                    </div>
                    <button type="submit" class="btn btn-primary">Record Disposal</button>
                </form>
                <div id="d-error" class="alert alert-danger" style="display:none; margin-top:10px;"></div>
                
                <h3 style="margin-top:20px;">Recent Disposals</h3>
                <table class="table" style="margin-top:10px;">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Facility</th>
                            <th>Recycled (kg)</th>
                            <th>Landfill (kg)</th>
                            <th>Diversion %</th>
                        </tr>
                    </thead>
                    <tbody id="disposal-list"></tbody>
                </table>
            </div>
        `;

        this.loadData();

        document.getElementById('disposal-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const errDiv = document.getElementById('d-error');
            errDiv.style.display = 'none';

            const payload = {
                weighment_id: parseInt(document.getElementById('d-weighment-id').value),
                facility_name: document.getElementById('d-facility-name').value,
                facility_type: document.getElementById('d-facility-type').value,
                recycled_weight_kg: parseFloat(document.getElementById('d-recycled').value),
                composted_weight_kg: parseFloat(document.getElementById('d-composted').value),
                landfill_weight_kg: parseFloat(document.getElementById('d-landfill').value),
                processed_at: new Date().toISOString()
            };

            try {
                await DisposalService.recordDisposal(payload);
                e.target.reset();
                this.loadData();
            } catch (err) {
                errDiv.textContent = err.message;
                errDiv.style.display = 'block';
            }
        });
    }

    async loadData() {
        try {
            const list = await DisposalService.getDisposals();
            const tbody = document.getElementById('disposal-list');
            tbody.innerHTML = list.map(d => `
                <tr>
                    <td>${d.id}</td>
                    <td>${d.facility_name}</td>
                    <td>${d.recycled_weight_kg}</td>
                    <td>${d.landfill_weight_kg}</td>
                    <td><strong>${d.diversion_rate_pct.toFixed(1)}%</strong></td>
                </tr>
            `).join('');

            const stats = await DisposalService.getAnalytics();
            const statsDiv = document.getElementById('d-analytics');
            statsDiv.innerHTML = `
                <p><strong>Total Net Weight:</strong> ${stats.total_net_weight_kg.toFixed(1)} kg</p>
                <p><strong>Total Recovered:</strong> ${(stats.total_recycled_kg + stats.total_composted_kg).toFixed(1)} kg</p>
                <p><strong>Total Landfill:</strong> ${stats.total_landfill_kg.toFixed(1)} kg</p>
                <h4 style="color:var(--success-color);">Overall Diversion Rate: ${stats.overall_diversion_rate_pct.toFixed(1)}%</h4>
            `;
        } catch(err) {
            console.error(err);
        }
    }
}
