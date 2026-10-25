# TECH UNFILTERED SI — EXECUTIVE GO-LIVE RUNBOOK
**Powered by KGU International** | **Founders:** Joann Coffey (CEO & Executive Conductor) & George Dubec (CRO & Deal-Flow Architect)  
**Status:** `100% PRODUCTION READY • NHIL ACTIVE` | **Marginal Compute Cost:** `$0.00 / token`

---

## 1. 1-Command Production Startup (`./launch_production.sh`)

Tech Unfiltered SI is engineered as a self-contained, zero-cloud-dependency sovereign stack. Everything—from the 16:9 Widescreen Broadcast Stage and 24kHz Local Voice Studio to the SQLite + 768D Vector Memory core and 10-Core n8n Workflow Engine—boots via a single command:

```bash
cd "/Users/jccoffey/Documents/KGU International/1. Internal Operations & Tech/Tech Unfiltered"
chmod +x ./launch_production.sh
./launch_production.sh
```

### What `./launch_production.sh` Executes Automatically:
1. **Database & Vector Memory Integrity Check:** Verifies `services/sovereign_backend.db` (SQLite state tables) and `services/rag_index.json` (872 sovereign chunks, 768D vector embeddings).
2. **10-Core Sovereign Module Verification:** Confirms all 10 modules (`KGU-MOD-01` through `KGU-MOD-10`) inside `services/open_source_modules/` are mounted and `VERIFIED_ON_DISK`.
3. **Sovereign Web4 Server Boot (`:8899`):** Launches `services/sovereign_web4_server.py` serving `/landing_page.html` and all 10 production REST/Webhook endpoints.
4. **Live Preflight Attestation:** Queries `/api/launch-preflight` and `/api/cyber-verify` to confirm Phase-0 cryptographic readiness before opening the executive stage.

**Primary Production URL:**
- `http://127.0.0.1:8899/landing_page.html`

---

## 2. Standalone Sovereign n8n Workflow Import (`services/n8n_sovereign_10core_workflow.json`)

We operate with **Zero Zapier** and zero third-party SaaS tax. Our autonomous pipeline runs on the **Standalone Sovereign n8n + SQLite Workflow Core**.

### Importing into Local n8n Instance (Optional UI Inspection):
1. Open your local sovereign n8n dashboard (default `http://127.0.0.1:5678`) or trigger directly via the built-in native executor at `/api/workflow/n8n-10core`.
2. Click **Workflows → Import from File** and select:
   ```text
   services/n8n_sovereign_10core_workflow.json
   ```
3. Activate the workflow (**"KGU Sovereign 10-Core Autonomous Workflow (Zero Zapier • 100% Standalone n8n)"**).

### The 10-Node Autonomous Execution Chain:
| Node | Module ID | Target Endpoint / Action | Function |
| :--- | :--- | :--- | :--- |
| **00** | `TRIGGER` | `POST /webhook/kgu-sovereign-10core` | Inbound Sovereign n8n Webhook Trigger |
| **01** | `KGU-MOD-01` | `POST /api/workflow/csuite-cycle` | 7-Executive Org Chart & Multiplayer ACL (`PC-100..PC-106`) |
| **02** | `KGU-MOD-02` | `GET /api/workflow/state` | Hindsight Persistent Cross-Session Memory (SQLite + 768D Vector) |
| **03** | `KGU-MOD-03` | `POST /api/workflow/avatar-call` | 24kHz Local Voice Cloning Studio & 16:9 Video Avatar Stream |
| **04 & 05** | `KGU-MOD-04/05` | Native JS Code Node | First-Principles SI RAG + Institutional Financial Arbitrage (`$10K`/`$25K`/`$150K`) |
| **06** | `KGU-MOD-06` | `GET /api/cyber-verify` | Phase-0 Cyber-Shield & Plugin Safety Gate (AES-256) |
| **07** | `KGU-MOD-07` | `POST /api/workflow/episode-select` | Impeccable Widescreen 16:9 Stage & Clean Studio Media Sync |
| **08** | `KGU-MOD-08` | `POST /api/workflow/client-tool` | Universal CLI-Anything & DOM Client-Tool Harness |
| **09 & 10** | `KGU-MOD-09/10` | `POST /api/workflow/book-call` | 65+ Executive Playbooks & 5-Step Autonomous Booking Dispatch |

To test the entire 10-Core pipeline from the terminal at any time:
```bash
curl -s -X POST http://127.0.0.1:8899/api/workflow/n8n-10core \
  -H "Content-Type: application/json" \
  -d '{"episodeId":"ep-048","speaker":"duo","trigger":"runbook_verification"}' | python3 -m json.tool
```

---

## 3. Widescreen 16:9 Live Video Call Stage & 24kHz Local Voice Studio

The centerpiece of `/landing_page.html` is the **Widescreen 16:9 Live Video Call Stage** engineered for live interactive dialogue and autonomous DOM control:

- **4 Selectable Live Personas:**
  1. **Joann Coffey** — *CEO & Executive Conductor* (`speaker: "joann"`): Commands sovereign architecture, enterprise AI governance, and full-stack digital twin deployments.
  2. **George Dubec** — *CRO & Deal-Flow Architect* (`speaker: "george"`): Drives institutional capital velocity, Boca Raton syndicate partnerships, and immediate ROI underwriting.
  3. **Dr. Aris Thorne** — *Chief SI Systems Scientist* (`speaker: "aris"`): Deep-dives into 768D vector memory, local hardware nodes, and `$0.00/token` inference telemetry.
  4. **Studio Duo (Joann & George Live)** — *Co-Hosted Widescreen Broadcast* (`speaker: "duo"`): Synchronized dual-host executive briefing.
- **24kHz Local Voice Studio (`KGU-MOD-03`):**
  - Streams local `.mp3`/`.wav` voice synthesis paired with real-time 16:9 studio video lip-sync and waveform telemetry.
  - Zero external API dependency; triggers bidirectional DOM Client Tools (`tour`, `highlight_pricing`, `open_booking`, `switch_episode`) via `/api/workflow/avatar-call` and `/api/workflow/client-tool`.

---

## 4. Broadcast Vault (10 Episodes + 11 Clean Boca Raton Studio Reels)

All broadcast media is served locally with **zero third-party watermarks** and instant episode switching via `/api/workflow/episode-select`:

- **10 Full Broadcast Episodes (`EP-039` through `EP-048`):**
  - Anchored by `EP-048: The Architecture of SI & Sovereign Hardware Nodes`.
  - Complete with synchronized audio tracks (`audio/tec_26_08_05.mp3`, etc.), studio video feeds (`videos/ep_001_studio.mp4`, etc.), and indexed RAG transcripts.
- **11 Clean Boca Raton Studio Reels (`0805_clip1.mp4` .. `0805_clip11.mp4`):**
  - High-impact executive micro-cutdowns audited for 0 third-party watermarks, ready for instant omnichannel syndication by the Autonomous CMO Engine (`PC-102`).

---

## 5. Phase-0 Cybersecurity & 256-Bit Voice Biometric Attestation

Every session, API transaction, and voice synthesis packet is protected by **Phase-0 Cyber-Shield (`KGU-MOD-06`)**:

- **256-Bit Voice Biometric Watermarking:** Authenticates Joann Coffey and George Dubec's vocal signatures against unauthorized cloning.
- **AES-256-GCM Local State Encryption:** All lead captures, enterprise bookings, and C-Suite audit logs remain strictly on-premise inside `services/sovereign_backend.db`.
- **Live Verification Endpoint:**
  ```bash
  curl -s http://127.0.0.1:8899/api/cyber-verify | python3 -m json.tool
  ```

---

## 6. Day-1 $100K/Day Deal-Desk & VIP Onboarding Operations

Tech Unfiltered SI monetizes executive attention directly on the page through a **3-Tier Sovereign Deal-Desk** backed by a **5-Step Autonomous Booking Dispatch (`/api/workflow/book-call`)**:

| Tier | Package Name | Investment | Target Payback | Day-1 Daily Velocity Target |
| :--- | :--- | :--- | :--- | :--- |
| **Tier 1** | **Broadcast Sponsor Package** | **$10,000** | 12 Days | 2x Sponsors / Day ($20,000) |
| **Tier 2** | **24/7 AI Call Center (Most Popular)** | **$25,000** | 19 Days | 2x Deployments / Day ($50,000) |
| **Tier 3** | **Custom Digital Twin & Full-Stack Deployment** | **$150,000** | 28 Days | 1x Enterprise Twin / 3 Days ($50,000 avg/day) |

### 5-Step Autonomous VIP Onboarding Protocol (Triggered on Every Booking):
1. **SQLite Deal-Desk Ledger Commit:** Writes the partner's dossier, tier selection, and timestamp into `services/sovereign_backend.db`.
2. **7-Executive C-Suite Allocation (`PC-100..PC-106`):** Assigns dedicated compute budgets across CEO, CRO, CMO, CTO, CFO, CISO, and COO agents.
3. **Institutional ROI Dossier Generation (`KGU-MOD-05`):** Calculates custom payback telemetry and attaches it to the booking confirmation.
4. **24kHz Voice & Video Concierge Dispatch (`KGU-MOD-03`):** Triggers an immediate personalized executive welcome from Joann Coffey & George Dubec.
5. **Sovereign Calendar & Provisioning Lock:** Issues a cryptographic Deal ID and schedules the Dedicated Sovereign Hardware Node provisioning window.

---

### Quick Endpoint Verification Checklist
```bash
curl -s http://127.0.0.1:8899/api/launch-preflight | python3 -m json.tool
curl -s http://127.0.0.1:8899/api/sovereign-modules | python3 -m json.tool
curl -s http://127.0.0.1:8899/api/workflow/state | python3 -m json.tool
```
