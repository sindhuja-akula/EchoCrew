# 08 - AI & ML Architecture 🤖

## Overview
EchoCrew incorporates AI/ML models under `backend/app/ai/` for predictive hotspot detection and automated report classification.

### Components
1. **Report Text Classifier**: Extracts incident severity and required equipment from freeform text descriptions.
2. **Spatial Clustering Engine**: Groups near-simultaneous reports within a 500-meter radius buffer to calculate hotspot intensity scores.
3. **Provider Abstraction Layer**: Decouples model implementations behind unified interfaces.
