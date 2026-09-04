export const API_BASE_URL = 'http://localhost:8000/api/v1';

export const WASTE_CATEGORIES = [
  { value: 'wet', label: 'Organic / Wet Waste', icon: '🥬', description: 'Food scraps, kitchen waste, compostables' },
  { value: 'dry', label: 'Dry Recyclable Waste', icon: '📦', description: 'Paper, cardboard, plastics, glass' },
  { value: 'electronic', label: 'E-Waste / Electronic', icon: '💻', description: 'Computers, phones, batteries, wiring' },
  { value: 'clothing', label: 'Textile / Clothing', icon: '👕', description: 'Old garments, fabrics, shoes' },
  { value: 'hazardous', label: 'Hazardous Waste', icon: '⚠️', description: 'Chemicals, medical items, paint, batteries' },
  { value: 'mixed', label: 'Mixed / Unsegregated', icon: '🗑️', description: 'General unsegregated trash pile' },
  { value: 'other', label: 'Other Waste', icon: '🧱', description: 'Debris, tires, bulky inert materials' },
];

export const VOLUME_TIERS = [
  { value: 'minor', label: 'Minor', title: 'Small Pile / Single Bag', desc: 'Households or small bag dump (< 0.2 m³)', color: '#10b981' },
  { value: 'moderate', label: 'Moderate', title: 'Medium Pile / Multiple Bags', desc: 'Accumulated street pile or several bags (0.2 – 1.0 m³)', color: '#f59e0b' },
  { value: 'bulk', label: 'Bulk', title: 'Large Dumping Site', desc: 'Major illegal dumping or truckload site (> 1.0 m³)', color: '#ef4444' },
];

export const REPORT_STATUSES = {
  reported: { label: 'Reported', color: '#64748b' },
  under_review: { label: 'Under Review', color: '#f59e0b' },
  approved: { label: 'Approved', color: '#3b82f6' },
  assigned: { label: 'Assigned', color: '#8b5cf6' },
  in_progress: { label: 'In Progress', color: '#06b6d4' },
  cleaned: { label: 'Cleaned', color: '#10b981' },
  verified: { label: 'Verified', color: '#059669' },
};

export const WORKER_STATUSES = {
  available: { label: 'Available', color: '#10b981' },
  assigned: { label: 'Assigned', color: '#3b82f6' },
  off_duty: { label: 'Off Duty', color: '#64748b' },
  suspended: { label: 'Suspended', color: '#ef4444' },
};

export const WORK_ORDER_STATUSES = {
  open: { label: 'Open', color: '#3b82f6' },
  assigned: { label: 'Assigned', color: '#8b5cf6' },
  in_progress: { label: 'In Progress', color: '#06b6d4' },
  completed: { label: 'Completed', color: '#10b981' },
  cancelled: { label: 'Cancelled', color: '#ef4444' },
};

export const ASSIGNMENT_STATUSES = {
  pending: { label: 'Pending', color: '#f59e0b' },
  assigned: { label: 'Assigned', color: '#3b82f6' },
  accepted: { label: 'Accepted', color: '#8b5cf6' },
  in_progress: { label: 'In Progress', color: '#06b6d4' },
  completed: { label: 'Completed', color: '#10b981' },
  cancelled: { label: 'Cancelled', color: '#ef4444' },
};

export const VERIFICATION_STATUSES = {
  pending: { label: 'Pending', color: '#f59e0b' },
  approved: { label: 'Approved', color: '#10b981' },
  rejected: { label: 'Rejected', color: '#ef4444' },
  requires_review: { label: 'Requires Review', color: '#6366f1' },
};

export const COMPENSATION_STATUSES = {
  pending: { label: 'Pending', color: '#f59e0b' },
  eligible: { label: 'Eligible', color: '#10b981' },
  processing: { label: 'Processing', color: '#3b82f6' },
  paid: { label: 'Paid', color: '#059669' },
  rejected: { label: 'Rejected', color: '#ef4444' },
};

export const COLLECTION_BATCH_STATUSES = {
  collecting: { label: 'Collecting', color: '#3b82f6' },
  sealed: { label: 'Sealed', color: '#8b5cf6' },
  in_transit: { label: 'In Transit', color: '#f59e0b' },
  delivered: { label: 'Delivered', color: '#10b981' },
};

export const MAX_UPLOAD_SIZE_BYTES = 10 * 1024 * 1024; // 10MB limit matching backend MAX_UPLOAD_SIZE_MB
