import { describe, it } from 'node:test';
import assert from 'node:assert';
import { API_BASE_URL, WASTE_CATEGORIES, VOLUME_TIERS } from '../src/utils/constants.js';

describe('Frontend Integration Suite', () => {
  it('API base URL matches backend API v1 route prefix', () => {
    assert.strictEqual(API_BASE_URL, 'http://localhost:8000/api/v1');
  });

  it('Waste Categories contain mandatory categories', () => {
    const values = WASTE_CATEGORIES.map(c => c.value);
    assert.ok(values.includes('wet'));
    assert.ok(values.includes('dry'));
    assert.ok(values.includes('electronic'));
    assert.ok(values.includes('hazardous'));
    assert.ok(values.includes('mixed'));
  });

  it('Volume Tiers contain approved tiers', () => {
    const values = VOLUME_TIERS.map(v => v.value);
    assert.ok(values.includes('minor'));
    assert.ok(values.includes('moderate'));
    assert.ok(values.includes('bulk'));
  });
});
