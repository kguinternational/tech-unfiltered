# Tech Unfiltered — Session 02 Dossier (TEC 26-08-13)
## "Replacing a $40,000/Month Call Center With a Local GPU (92ms Full-Duplex Test)"

### Executive Summary & Metadata
- **Date Recorded**: August 13, 2026
- **Location**: Boca Raton Master Production Facility
- **Hosts**: Joann Coffey & George Dubec
- **Runtime**: 24 Minutes 59 Seconds
- **Master Files**: `TEC 26-08-13.mp4` (1.1 GB), `TEC 26-08-13.mp3` (35.9 MB)
- **Key Thematics**: Conversational Voice AI, Zero Per-Minute SaaS Tolls, 92ms Glass-to-Glass Latency, Unified Memory Architecture, 250 Concurrent Calls on Apple Silicon / Local Metal.

---

### Core Discussion Pillars

#### 1. The Real Cost of Legacy Customer Support
- Dissecting the $40,000/month operational burn of traditional outsourced offshore call centers: high turnover, inconsistent QA, training latency, and security exposure.
- Comparison with per-minute voice APIs that charge $0.10 to $0.25 per minute, making high-volume customer interaction prohibitively expensive at scale.

#### 2. The 92ms Latency Breakthrough
- Achieving true full-duplex conversational audio where interruptions (barge-in) feel completely natural and human.
- Localized pipeline architecture: Local Voice Activity Detection (VAD) + Fast Acoustic Tokenizer + Direct GPU Inference + Streaming Synthesis.
- Why zero network round-trip hops to cloud data centers drops latency below the human perception threshold of 100ms.

#### 3. Sovereign Metal Clusters & Zero Marginal Inference Cost
- Leveraging high-bandwidth unified memory (UMA) on local hardware nodes.
- Handling 250 simultaneous inbound customer workflows on a single dedicated appliance without transmitting proprietary client voice data over public networks.
- 100% compliance with HIPAA, SOC2 Type II, and corporate privacy covenants.

---

### Key Quotes & Axioms
- *"The per-minute voice SaaS model is a tax on your customer relationships. When you own the metal, your marginal cost per call drops to zero."* — George Dubec
- *"At 92 milliseconds, the uncanny valley disappears. The conversation becomes an authentic, empathetic encounter."* — Joann Coffey
