import { describe, it } from 'node:test';
import assert from 'node:assert';
import { validateCoordinates, validateImageFile, validateReportForm } from '../src/utils/validation.js';

describe('Frontend Validation Utilities Suite', () => {
  it('validateCoordinates accepts valid WGS84 coordinates', () => {
    const res = validateCoordinates(12.9716, 77.5946);
    assert.strictEqual(res.valid, true);
    assert.strictEqual(res.error, null);
  });

  it('validateCoordinates rejects out-of-range coordinates', () => {
    const resLat = validateCoordinates(95.0, 77.5946);
    assert.strictEqual(resLat.valid, false);
    assert.ok(resLat.error.includes('between -90 and 90'));

    const resLng = validateCoordinates(12.9716, 185.0);
    assert.strictEqual(resLng.valid, false);
    assert.ok(resLng.error.includes('between -180 and 180'));
  });

  it('validateImageFile validates image mime types and size', () => {
    const validFile = { type: 'image/jpeg', size: 1024 * 1024 }; // 1MB
    assert.strictEqual(validateImageFile(validFile).valid, true);

    const invalidType = { type: 'application/pdf', size: 1024 };
    assert.strictEqual(validateImageFile(invalidType).valid, false);

    const oversized = { type: 'image/png', size: 15 * 1024 * 1024 }; // 15MB
    assert.strictEqual(validateImageFile(oversized).valid, false);
  });

  it('validateReportForm validates required fields', () => {
    const res = validateReportForm({
      latitude: 12.9716,
      longitude: 77.5946,
      category: 'dry',
      volume_tier: 'minor',
    });
    assert.strictEqual(res.valid, true);
    assert.strictEqual(res.errors.length, 0);
  });
});
