"""
Tests for CleaningEvidence, Verification, Compensation, and CollectionBatch models.
"""

import unittest
from datetime import datetime, timezone
from database.models import (
    CleaningEvidence,
    Verification,
    Compensation,
    CollectionBatch,
    EvidenceType,
    VerificationStatus,
    VerificationMethod,
    CompensationStatus,
    CollectionBatchStatus
)

class TestVerificationAndCompensation(unittest.TestCase):

    def test_verification_enums(self):
        self.assertEqual(EvidenceType.BEFORE.value, "before")
        self.assertEqual(EvidenceType.PROGRESS.value, "progress")
        self.assertEqual(EvidenceType.AFTER.value, "after")
        self.assertEqual(VerificationStatus.APPROVED.value, "approved")
        self.assertEqual(VerificationMethod.AI_ASSISTED.value, "ai_assisted")
        self.assertEqual(CompensationStatus.ELIGIBLE.value, "eligible")
        self.assertEqual(CollectionBatchStatus.COLLECTING.value, "collecting")

    def test_cleaning_evidence_creation(self):
        now = datetime.now(timezone.utc)
        evidence = CleaningEvidence(
            work_unit_id=1,
            work_assignment_id=1,
            submitted_by_id=1,
            evidence_type=EvidenceType.AFTER,
            image_url="storage/evidence/after_001.jpg",
            captured_at=now,
            latitude=12.9716,
            longitude=77.5946
        )
        self.assertEqual(evidence.evidence_type, EvidenceType.AFTER)
        self.assertEqual(evidence.image_url, "storage/evidence/after_001.jpg")

    def test_verification_record_creation(self):
        now = datetime.now(timezone.utc)
        verification = Verification(
            evidence_id=1,
            work_unit_id=1,
            verifier_id=1,
            status=VerificationStatus.APPROVED,
            method=VerificationMethod.MANUAL,
            notes="Visual confirmation completed",
            verified_at=now
        )
        self.assertEqual(verification.status, VerificationStatus.APPROVED)
        self.assertEqual(verification.method, VerificationMethod.MANUAL)

    def test_compensation_record_creation(self):
        compensation = Compensation(
            worker_id=1,
            assignment_id=1,
            verification_id=1,
            amount=250.00,
            currency="INR",
            status=CompensationStatus.ELIGIBLE
        )
        self.assertEqual(compensation.amount, 250.00)
        self.assertEqual(compensation.currency, "INR")
        self.assertEqual(compensation.status, CompensationStatus.ELIGIBLE)

    def test_collection_batch_creation(self):
        now = datetime.now(timezone.utc)
        batch = CollectionBatch(
            batch_code="BATCH-2026-001",
            vehicle_id=1,
            status=CollectionBatchStatus.COLLECTING,
            total_volume_m3=3.5,
            collected_at=now
        )
        self.assertEqual(batch.batch_code, "BATCH-2026-001")
        self.assertEqual(batch.total_volume_m3, 3.5)
        self.assertEqual(batch.status, CollectionBatchStatus.COLLECTING)

if __name__ == "__main__":
    unittest.main()
