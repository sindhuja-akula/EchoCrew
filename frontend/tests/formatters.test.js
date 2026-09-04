import { describe, it } from 'node:test';
import assert from 'node:assert';
import { formatCoordinates, getCategoryMeta, renderStatusBadge } from '../src/utils/formatters.js';

describe('Frontend Formatters Suite', () => {
  it('formatCoordinates formats latitude and longitude nicely', () => {
    const formatted = formatCoordinates(12.9716, 77.5946);
    assert.strictEqual(formatted, '12.9716° N, 77.5946° E');
  });

  it('getCategoryMeta returns metadata for valid category', () => {
    const meta = getCategoryMeta('electronic');
    assert.strictEqual(meta.label, 'E-Waste / Electronic');
    assert.strictEqual(meta.icon, '💻');
  });

  it('renderStatusBadge renders badge element string', () => {
    const badgeHtml = renderStatusBadge('reported', 'report');
    assert.ok(badgeHtml.includes('Reported'));
    assert.ok(badgeHtml.includes('badge'));
  });
});
