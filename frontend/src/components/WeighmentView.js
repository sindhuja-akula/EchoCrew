import { TransferService } from '../services/transferService.js';

export class WeighmentView {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
    }

    async render() {
        this.container.innerHTML = `
            <div class="card fade-in">
                <h2>⚖️ Transfer Station Weighment</h2>
                <form id="weighment-form">
                    <div class="form-group">
                        <label>Batch ID</label>
                        <input type="number" id="w-batch-id" required>
                    </div>
                    <div class="form-group">
                        <label>Weighbridge Code</label>
                        <input type="text" id="w-code" required>
                    </div>
                    <div class="form-group">
                        <label>Gross Weight (kg)</label>
                        <input type="number" id="w-gross" step="0.1" required>
                    </div>
                    <div class="form-group">
                        <label>Tare Weight (kg)</label>
                        <input type="number" id="w-tare" step="0.1" required>
                    </div>
                    <button type="submit" class="btn btn-primary">Record Weighment</button>
                </form>
                <div id="w-error" class="alert alert-danger" style="display:none; margin-top:10px;"></div>
                
                <h3 style="margin-top:20px;">Recent Weighments</h3>
                <table class="table" style="margin-top:10px;">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Batch ID</th>
                            <th>Gross (kg)</th>
                            <th>Tare (kg)</th>
                            <th>Net (kg)</th>
                        </tr>
                    </thead>
                    <tbody id="weighment-list"></tbody>
                </table>
            </div>
        `;

        this.loadWeighments();

        document.getElementById('weighment-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const errDiv = document.getElementById('w-error');
            errDiv.style.display = 'none';

            const payload = {
                batch_id: parseInt(document.getElementById('w-batch-id').value),
                weighbridge_code: document.getElementById('w-code').value,
                gross_weight_kg: parseFloat(document.getElementById('w-gross').value),
                tare_weight_kg: parseFloat(document.getElementById('w-tare').value),
                weighment_time: new Date().toISOString()
            };

            try {
                await TransferService.recordWeighment(payload);
                e.target.reset();
                this.loadWeighments();
            } catch (err) {
                errDiv.textContent = err.message;
                errDiv.style.display = 'block';
            }
        });
    }

    async loadWeighments() {
        try {
            const list = await TransferService.getWeighments();
            const tbody = document.getElementById('weighment-list');
            tbody.innerHTML = list.map(w => `
                <tr>
                    <td>${w.id}</td>
                    <td>${w.batch_id}</td>
                    <td>${w.gross_weight_kg}</td>
                    <td>${w.tare_weight_kg}</td>
                    <td><strong>${w.net_weight_kg}</strong></td>
                </tr>
            `).join('');
        } catch(err) {
            console.error(err);
        }
    }
}
