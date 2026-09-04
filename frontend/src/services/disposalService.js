export class DisposalService {
    static async recordDisposal(disposalData) {
        const response = await fetch('/api/v1/disposal/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(disposalData)
        });
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || 'Failed to record disposal');
        }
        return response.json();
    }

    static async getDisposals() {
        const response = await fetch('/api/v1/disposal/');
        if (!response.ok) throw new Error('Failed to fetch disposals');
        return response.json();
    }

    static async getAnalytics() {
        const response = await fetch('/api/v1/disposal/analytics/summary');
        if (!response.ok) throw new Error('Failed to fetch analytics');
        return response.json();
    }
}
