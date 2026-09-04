export class IntelligentVerificationService {
    static async analyze(reportId, assignmentId, evidenceId) {
        const response = await fetch('/api/v1/verifications/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                report_id: reportId,
                assignment_id: assignmentId,
                evidence_id: evidenceId
            })
        });
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || 'Failed to analyze verification');
        }
        return response.json();
    }
}
