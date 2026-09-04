export class TransferService {
    static async recordWeighment(weighmentData) {
        const response = await fetch('/api/v1/weighments/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(weighmentData)
        });
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || 'Failed to record weighment');
        }
        return response.json();
    }

    static async getWeighments() {
        const response = await fetch('/api/v1/weighments/');
        if (!response.ok) throw new Error('Failed to fetch weighments');
        return response.json();
    }
}
