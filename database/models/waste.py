"""
Waste category metadata and volumetric descriptors for CleanLoop.
"""

from database.models.enums import WasteCategory, VolumeTier

WASTE_CATEGORY_METADATA = {
    WasteCategory.WET: {"label": "Wet / Organic Waste", "recyclable": False, "priority": "high"},
    WasteCategory.DRY: {"label": "Dry / Recyclable Waste", "recyclable": True, "priority": "medium"},
    WasteCategory.ELECTRONIC: {"label": "E-Waste / Electronics", "recyclable": True, "priority": "high"},
    WasteCategory.CLOTHING: {"label": "Textiles & Clothing", "recyclable": True, "priority": "low"},
    WasteCategory.HAZARDOUS: {"label": "Hazardous Waste", "recyclable": False, "priority": "critical"},
    WasteCategory.MIXED: {"label": "Mixed Unsorted Waste", "recyclable": False, "priority": "medium"},
    WasteCategory.OTHER: {"label": "Other Unclassified", "recyclable": False, "priority": "low"},
}

VOLUME_TIER_DESCRIPTORS = {
    VolumeTier.MINOR: {"estimated_volume_m3": "< 0.2 m³", "description": "Small household bag / litter"},
    VolumeTier.MODERATE: {"estimated_volume_m3": "0.2 - 1.0 m³", "description": "Pile / multiple dumped bags"},
    VolumeTier.BULK: {"estimated_volume_m3": "> 1.0 m³", "description": "Major dumping site / truck load needed"},
}
