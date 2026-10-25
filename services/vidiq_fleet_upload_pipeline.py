#!/usr/bin/env python3
"""
========================================================================================
TECH UNFILTERED SI & KGU INTERNATIONAL — VIDIQ FLEET UPLOAD PIPELINE
========================================================================================
Automated VidIQ-optimized multi-episode publishing engine for Tech Unfiltered SI.
Handles all 6 studio master episodes + official show trailer in exact chronological order:

  1. Episode 01: TEC 26-08-05 (Aug 5, 2026 · 45:41 · 1.9 GB)
  2. Episode 02: TEC 26-08-13 (Aug 13, 2026 · 24:59 · 1.0 GB)
  3. Episode 03: TEC 26-08-20 (Aug 20, 2026 · 25:49 · 1.07 GB)
  4. Episode 04: TEC 26-08-27 (Aug 27, 2026 · 34:28 · 1.43 GB)
  5. Episode 05: TEC 26-09-03 (Sep 3, 2026 · 22:47 · 947 MB)
  6. Episode 06: TEC 26-09-10 (Sep 10, 2026 · 29:51 · 1.24 GB)
  Trailer:       TEC TRAILER  (Aug 21, 2026 · 1:14 · 50.4 MB)

VidIQ Standards Enforced:
- High-CTR Curiosity Title (Under 70 characters with power keywords)
- Above-the-fold First 3 Lines with High-Ticket Money Links ($10K, $25K, $150K)
- Clickable 00:00 Chapter Timestamps
- Key Executive Bullet Takeaways
- Verified Host Profiles (Joann Coffey & George Dubec)
- 501(c)(3) Foundation Governance Acknowledgment (The JC Coffey Foundation, EIN 33-3450194)
- 20+ High-Volume Search Tags & Category 28 (Science & Technology)
- High-Contrast 1280x720 Studio Thumbnail Attached
- Pinned Comment Copy Staged for Day-1 Conversion
========================================================================================
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path
from typing import Dict, Any, List, Optional

ROOT_DIR = Path("/Users/jccoffey/Documents/KGU International/1. Internal Operations & Tech/Tech Unfiltered")
SERVICES_DIR = ROOT_DIR / "services"
VIDEOS_DIR = ROOT_DIR / "videos"
THUMBS_DIR = ROOT_DIR / "thumbs"
AUDIO_DIR = ROOT_DIR / "audio"
CLIENT_SECRETS_FILE = SERVICES_DIR / "client_secrets.json"
TOKEN_FILE = SERVICES_DIR / "token.json"
MANIFEST_DIR = SERVICES_DIR / "syndication_10channels"

SCOPES = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtubepartner",
]

# MASTER CHRONOLOGICAL EPISODE CATALOG WITH VIDIQ OPTIMIZED METADATA
EPISODES_CATALOG = [
    {
        "order": 1,
        "code": "EP-001",
        "date": "2026-08-05",
        "video_file": "tec_26_08_05.mp4",
        "audio_file": "tec_26_08_05.mp3",
        "thumb_file": "thumb_ep01.jpg",
        "duration_str": "45:41",
        "title": "Why Rented Cloud Wrappers Collapse (Own The Dedicated Hardware Node)",
        "vidiq_title": "Why Rented Cloud Wrappers Collapse Under Margin Pressure | Tech Unfiltered Ep 01",
        "vidiq_score": 98,
        "primary_keyword": "Dedicated Sovereign Hardware Nodes",
        "hook": "Software wrappers face an existential margin collapse under OpenAI token tax. In Episode 01, Joann Coffey & George Dubec break down why true enterprise sovereignty requires owning dedicated local hardware wafers at $0.00 marginal cost.",
        "chapters": [
            ("00:00", "Cold Open: Stop Calling API Wrappers Synthetic Intelligence"),
            ("03:15", "Why Rented Cloud Wrappers Collapse Under Margin Pressure"),
            ("09:20", "Dedicated Sovereign Hardware Nodes ($0.00 Token Tax)"),
            ("17:40", "After Swiping & Autonomous Digital Twin Interactions"),
            ("28:40", "Zero-Human-Bottleneck (NHIL) Operations at Scale"),
            ("38:15", "Physical SI: The Mechanical Energy Bottleneck"),
            ("44:20", "Sovereign Retainers & Deal Desk Lock-In")
        ],
        "takeaways": [
            "Dedicated Sovereign Hardware Nodes outperform rented cloud wrappers with zero marginal token tax.",
            "100% No-Human-In-The-Loop (NHIL) execution eliminates manual SaaS seat license overhead.",
            "Physical SI embodiment grounds intelligence in hardware, local clusters, and private micro-grids."
        ],
        "tags": [
            "Tech Unfiltered SI", "Tech Unfiltered", "Physical Superintelligence", "KGU International",
            "Joann Coffey", "George Dubec", "Boca Raton Studio", "Dedicated Sovereign Hardware Nodes",
            "AI Call Center", "Autonomous Enterprise", "Digital Twins", "NHIL", "Superintelligence",
            "Voice AI", "Local LLM", "Apple Silicon AI", "Private Compute Node", "Zero Token Tax"
        ]
    },
    {
        "order": 2,
        "code": "EP-002",
        "date": "2026-08-13",
        "video_file": "tec_26_08_13.mp4",
        "audio_file": "tec_26_08_13.mp3",
        "thumb_file": "thumb_ep02.jpg",
        "duration_str": "24:59",
        "title": "We Replaced a $40,000/Mo Call Center With a Local GPU (92ms Live Test)",
        "vidiq_title": "We Replaced a $40,000/Mo Call Center With a Local GPU (92ms Test) | Ep 02",
        "vidiq_score": 97,
        "primary_keyword": "Open Source AI Call Center Local GPU",
        "hook": "Why spend $0.18/minute on hosted voice wrappers when a dedicated local node delivers sub-100ms full-duplex conversational audio with zero per-minute tolls? Live studio stress-test with Joann Coffey & George Dubec.",
        "chapters": [
            ("00:00", "Live Stress Test: 92ms Full-Duplex Voice Demonstration"),
            ("04:30", "The SaaS Burn: Why $15,000/Mo Call Center Bills Are Obsolete"),
            ("09:45", "Sovereign Voice 3 vs Hosted Cloud Wrappers (Deep Benchmark)"),
            ("16:20", "Local Silero VAD + Flow-Matching Zero-Shot Voice Synthesis"),
            ("21:30", "Deploying a Turnkey 24/7 AI Call Center in 24 Hours")
        ],
        "takeaways": [
            "Sub-100ms conversational voice response achieved on local Apple Silicon Metal clusters.",
            "250 simultaneous inbound SIP calls handled at $0.00 marginal inference tax.",
            "Instant qualification and CRM booking directly through self-hosted SQLite vaults."
        ],
        "tags": [
            "Open Source Voice AI", "AI Call Center", "Local Voice Cloning", "Tech Unfiltered",
            "Joann Coffey", "George Dubec", "Sovereign Voice", "Whisper Local", "Silero VAD",
            "Enterprise Call Automation", "Zero Token Tax", "KGU International", "Physical SI"
        ]
    },
    {
        "order": 3,
        "code": "EP-003",
        "date": "2026-08-20",
        "video_file": "tec_26_08_20.mp4",
        "audio_file": "tec_26_08_20.mp3",
        "thumb_file": "thumb_ep03.jpg",
        "duration_str": "25:49",
        "title": "Living Worlds in Code Runtime: Why Static 3D Models Are Dead",
        "vidiq_title": "Living Worlds in Code Runtime: Why Static 3D Models Are Dead | Ep 03",
        "vidiq_score": 96,
        "primary_keyword": "Procedural 3D Runtime Living Worlds",
        "hook": "We are way beyond static polygon files. Joann Coffey and George Dubec demonstrate living worlds generated at runtime in code—pure geometry, trigonometric kinematics, and procedural physical simulations running on sovereign nodes.",
        "chapters": [
            ("00:00", "Beyond Static Models: The Runtime Code-as-Geometry Paradigm"),
            ("05:15", "Trigonometric Kinematics: Eliminating Keyframes in Physical Twins"),
            ("11:30", "Geothermal Microgrids & The Hard Physics of Data Centers"),
            ("18:10", "Organoid Biocomputing Wetware & 2026 Physical Superintelligence"),
            ("22:50", "The JC Coffey Foundation & Sacred Legacy Memory Preservation")
        ],
        "takeaways": [
            "Code-as-Geometry instantiates living 3D environments procedurally with zero external asset files.",
            "Physical SI grounds synthetic intelligence in robotic actuation, clean energy, and hardware wafers.",
            "Legacy memory preservation empowers families and institutions via sovereign digital vaults."
        ],
        "tags": [
            "Code as Geometry", "ThreeJS Procedural", "Living Worlds Runtime", "Physical SI",
            "Joann Coffey", "George Dubec", "Geothermal Microgrids", "Biocomputing",
            "Tech Unfiltered SI", "Digital Twins", "Superintelligence", "KGU International"
        ]
    },
    {
        "order": 4,
        "code": "EP-004",
        "date": "2026-08-27",
        "video_file": "tec_26_08_27.mp4",
        "audio_file": "tec_26_08_27.mp3",
        "thumb_file": "thumb_ep04.jpg",
        "duration_str": "34:28",
        "title": "Autonomous AI Agents Broke Our Contract: The Boardroom Shield",
        "vidiq_title": "Autonomous AI Agents Broke Our Contract: The Boardroom Shield | Ep 04",
        "vidiq_score": 95,
        "primary_keyword": "AI Agent Liability Audit Boardroom Shield",
        "hook": "When autonomous AI agent swarms make unauthorized financial commitments or breach privacy guardrails, who is legally liable? Joann Coffey and George Dubec unveil the 6-point forensic audit shielding corporate directors from personal liability.",
        "chapters": [
            ("00:00", "The Rogue Agent Liability Crisis Facing Enterprise Boards"),
            ("06:20", "NYC's Gen-AI Ban & The Danger of Cognitive Surrender"),
            ("14:10", "The Mechanical Compute Bottleneck: Welders, Grids & Cooling"),
            ("21:45", "The 6-Point Forensic Legal Defense Shield & BDI State Attestation"),
            ("28:30", "The Love Effect OS: Preserving Human Honor in an Automated Era")
        ],
        "takeaways": [
            "Enterprise boards face personal fiduciary exposure for unauthorized autonomous agent transactions.",
            "Cryptographic BDI mental state attestation creates an unbreachable courtroom evidentiary shield.",
            "The Love Effect OS anchors exponential technology in human reverence and ethical governance."
        ],
        "tags": [
            "AI Agent Liability", "Boardroom Defense Shield", "Autonomous Agent Governance",
            "Tech Unfiltered", "Joann Coffey", "George Dubec", "BDI Attestation", "Lex Sovereign",
            "The Love Effect OS", "JC Coffey Foundation", "Enterprise AI Audit"
        ]
    },
    {
        "order": 5,
        "code": "EP-005",
        "date": "2026-09-03",
        "video_file": "tec_26_09_03.mp4",
        "audio_file": "tec_26_09_03.mp3",
        "thumb_file": "thumb_ep05.jpg",
        "duration_str": "22:47",
        "title": "Autonomous C-Suite Swarms: 7 Exec Agents Running a Company NHIL",
        "vidiq_title": "Autonomous C-Suite Swarms: 7 Exec Agents Running a Company NHIL | Ep 05",
        "vidiq_score": 96,
        "primary_keyword": "Autonomous C-Suite AI Agents Paperclip",
        "hook": "From CEO to CMO, CRO, and General Counsel—how 7 self-healing autonomous agents govern capital allocation, legal contracts, and media syndication with 100% No Human In The Loop. Joann Coffey & George Dubec broadcast live from Boca Raton.",
        "chapters": [
            ("00:00", "Mobile Studio & Dedicated Mesh Network Architecture"),
            ("04:40", "The 7-Executive Autonomous C-Suite Org Chart (PC-100 to PC-106)"),
            ("09:50", "Paperclip Protocol: Atomic Ticket Checkouts & SHA-256 Receipts"),
            ("15:30", "How Our CMO Agent Cuts 5 Viral Reels In Under 130 Milliseconds"),
            ("19:45", "Locking Enterprise Onboarding with Zero Human Operators")
        ],
        "takeaways": [
            "Paperclip governance enforces atomic task checkout and deterministic BDI mental state cycles.",
            "Autonomous C-Suite agents operate continuously at $0.00 marginal software token overhead.",
            "100% NHIL execution replaces multi-million-dollar administrative back-office bloat."
        ],
        "tags": [
            "Autonomous Agents", "AI C-Suite", "Paperclip Protocol", "NHIL", "Joann Coffey",
            "George Dubec", "Tech Unfiltered SI", "KGU International", "Self-Healing Agents",
            "Superintelligence", "Autonomous Enterprise"
        ]
    },
    {
        "order": 6,
        "code": "EP-006",
        "date": "2026-09-10",
        "video_file": "tec_26_09_10.mp4",
        "audio_file": "tec_26_09_10.mp3",
        "thumb_file": "thumb_ep06.jpg",
        "duration_str": "29:51",
        "title": "$100K/Day Sovereign Deal Flow: The Trillion-Dollar Blueprint",
        "vidiq_title": "$100K/Day Sovereign Deal Flow: The Trillion-Dollar Blueprint | Ep 06",
        "vidiq_score": 99,
        "primary_keyword": "Sovereign Deal Flow Physical Superintelligence",
        "hook": "How KGU International generates high-ticket enterprise capital velocity ($10K sponsorships, $25K call centers, $150K hardware nodes) using 100% autonomous state machines, JPMorgan Chase wire routing, and zero ad spend.",
        "chapters": [
            ("00:00", "The Trillion-Dollar Blueprint: Capital Velocity in Physical SI"),
            ("05:40", "Three-Tier High-Ticket Monetization Matrix ($10K / $25K / $150K)"),
            ("12:15", "Sovereign Escrow Gateway & Cryptographically Sealed Legal Dockets"),
            ("19:30", "Physical SI Invariant: Wafers, Microgrids, and Embodied Robotics"),
            ("26:10", "Season 1 Master Review & Exclusive VIP Deal Desk Access")
        ],
        "takeaways": [
            "High-ticket conversion velocity achieves $100K/day without external advertising dependencies.",
            "Direct escrow locking guarantees 20% immediate cash deposit upon contract ratification.",
            "Physical Superintelligence merges sovereign compute infrastructure with long-term human legacy."
        ],
        "tags": [
            "Capital Velocity", "Sovereign Deal Desk", "High Ticket Sales", "Physical Superintelligence",
            "Joann Coffey", "George Dubec", "KGU International", "Tech Unfiltered SI",
            "JPMorgan Escrow", "Hardware Nodes", "Autonomous Revenue"
        ]
    },
    {
        "order": 0,
        "code": "TRAILER",
        "date": "2026-08-21",
        "video_file": "tec_trailer.mp4",
        "audio_file": "tec_trailer.mp3",
        "thumb_file": "thumb_trailer.jpg",
        "duration_str": "1:14",
        "title": "Tech Unfiltered SI: 100% No Human In The Loop (Official Trailer)",
        "vidiq_title": "Tech Unfiltered SI: The Sovereign Media Network (Official Trailer)",
        "vidiq_score": 97,
        "primary_keyword": "Tech Unfiltered SI Official Trailer",
        "hook": "No teleprompters. No corporate PR spin. 100% No Human In The Loop. Joann Coffey & George Dubec bring you inside the private Boca Raton studio to witness the birth of Physical Superintelligence.",
        "chapters": [
            ("00:00", "We Are Way Beyond Static Models"),
            ("00:25", "Dedicated Sovereign Hardware Nodes"),
            ("00:50", "The Love Effect OS & Physical SI")
        ],
        "takeaways": [
            "The official broadcast network hosted by Joann Coffey & George Dubec.",
            "Dissecting dedicated sovereign hardware nodes, zero token margins, and boardroom defense.",
            "Powered by KGU International LLC and the JC Coffey Foundation."
        ],
        "tags": [
            "Tech Unfiltered Trailer", "Tech Unfiltered SI", "Joann Coffey", "George Dubec",
            "Physical Superintelligence", "KGU International", "Autonomous Podcast"
        ]
    }
]


def build_vidiq_description(ep: Dict[str, Any]) -> str:
    """Builds a high-converting, VidIQ-optimized YouTube description."""
    title = ep["vidiq_title"]
    hook = ep["hook"]
    
    chapters_txt = "\n".join([f"{ts} — {c_title}" for ts, c_title in ep["chapters"]])
    takeaways_txt = "\n".join([f"{i+1}. {t}" for i, t in enumerate(ep["takeaways"])])
    
    desc = f"""{title}

⚡ THE BROADCAST THESIS:
"{hook}"

🔥 DEPLOY 24/7 SOVEREIGN VOICE AI OR SPONSOR TECH UNFILTERED SI:
• Podcast Episode Sponsorship ($10,000): https://thepromise.si/#sponsor
• Turnkey 24/7 AI Call Center Deployment ($25,000): https://thepromise.si/#callcenter
• Dedicated Sovereign Hardware Node ($150,000): https://thepromise.si/#hardware
• Direct Studio Hotline: 1-888-323-TECH (1-888-323-8324)

⏱ CHAPTERS & TIMESTAMPS:
{chapters_txt}

🧠 KEY EXECUTIVE TAKEAWAYS:
{takeaways_txt}

🎙️ MEET THE HOSTS:
• Joann Coffey — Founder & Executive Conductor, KGU International; Creator, Tech Unfiltered SI; Author of The Love Effect OS. 50 years of entrepreneurial mastery engineering 100% No Human In The Loop (NHIL) infrastructure.
• George Dubec — Chief Revenue Officer, Co-Host & Venture Deal-Flow Architect. Turning conversations into verified institutional escrow and boardroom liability shields.

🛡️ 501(c)(3) PHILANTHROPIC FIREWALL & COMPLIANCE:
This broadcast acknowledges the philanthropic mission of The JC Coffey Foundation, Inc. (EIN: 33-3450194), a 501(c)(3) tax-exempt public benefit foundation dedicated to sacred legacy memory preservation, youth technology access, and compassionate disaster resilience. Produced under IRC Section 513(i) Qualified Sponsorship standards.
• JC Coffey Foundation Inquiries: 1-844-SAFE-107 | foundation@jccoffeyfoundation.org

🌐 OFFICIAL SOVEREIGN NETWORK PLATFORMS:
• 4K Interactive Sovereign Stream: http://127.0.0.1:8899
• Next.js Broadcast Hub: http://localhost:3002
• High-Ticket Deal Desk & Escrow: http://127.0.0.1:8899/#dealdesk
• Full Master Audio RSS Feed: http://127.0.0.1:8899/podcast_feed_si.xml
• Spotify Verified Enclosure: http://127.0.0.1:8899/podcast_feed_spotify.xml

#TechUnfilteredSI #PhysicalSuperintelligence #SovereignHardware #NHIL #KGUInternational #JoannCoffey #GeorgeDubec #VoiceAI #AICallCenter #DealDesk"""
    return desc


def build_pinned_comment(ep: Dict[str, Any]) -> str:
    """Builds the high-converting VidIQ pinned comment."""
    return f"""⚡ Welcome to Tech Unfiltered SI ({ep['code']})!

Direct Deal Desk Access for Founders, CTOs & Enterprise Boards:
1. Test our live 92ms Sovereign Voice line right now: 1-888-323-TECH (1-888-323-8324)
2. Deploy your Turnkey 24/7 AI Call Center ($25,000): https://thepromise.si/#callcenter
3. Lock your Episode Media Sponsorship ($10,000): https://thepromise.si/#sponsor
4. Commission your Dedicated Sovereign Hardware Node ($150,000): https://thepromise.si/#hardware

What is your take on owning dedicated hardware wafers vs renting OpenAI cloud tokens? Drop your thoughts below — Joann & George read every response."""


def generate_fleet_manifest() -> Dict[str, Any]:
    """Compiles the complete VidIQ fleet manifest for all episodes in order."""
    now_iso = time.strftime("%Y-%m-%dT%H:%M:%SZ")
    manifest = {
        "engine": "Tech Unfiltered SI • VidIQ Fleet Upload Engine",
        "organization": "KGU International LLC & The JC Coffey Foundation (EIN: 33-3450194)",
        "createdAt": now_iso,
        "standard": "VidIQ High-CTR & Day-1 High-Ticket Monetization",
        "category": "28 (Science & Technology)",
        "totalEpisodes": len(EPISODES_CATALOG),
        "episodesInOrder": []
    }
    
    for ep in EPISODES_CATALOG:
        vid_path = VIDEOS_DIR / ep["video_file"]
        aud_path = AUDIO_DIR / ep["audio_file"]
        thumb_path = THUMBS_DIR / ep["thumb_file"]
        
        ep_entry = {
            "order": ep["order"],
            "code": ep["code"],
            "date": ep["date"],
            "duration": ep["duration_str"],
            "vidiqScore": ep["vidiq_score"],
            "title": ep["vidiq_title"],
            "primaryKeyword": ep["primary_keyword"],
            "videoFile": str(vid_path),
            "videoExists": vid_path.exists(),
            "videoSizeMB": round(vid_path.stat().st_size / (1024*1024), 1) if vid_path.exists() else 0,
            "audioFile": str(aud_path),
            "audioExists": aud_path.exists(),
            "thumbnailFile": str(thumb_path),
            "thumbnailExists": thumb_path.exists(),
            "description": build_vidiq_description(ep),
            "pinnedComment": build_pinned_comment(ep),
            "tags": ep["tags"],
            "status": "STAGED_READY_FOR_UPLOAD" if (vid_path.exists() and thumb_path.exists()) else "ASSETS_PENDING"
        }
        manifest["episodesInOrder"].append(ep_entry)
        
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
    out_file = MANIFEST_DIR / "VIDIQ_ALL_EPISODES_FLEET_MANIFEST.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
        
    return manifest


def print_manifest_summary(manifest: Dict[str, Any]):
    print("======================================================================================")
    print("TECH UNFILTERED SI — VIDIQ MASTER FLEET UPLOAD MANIFEST")
    print("======================================================================================")
    print(f"Generated At:   {manifest['createdAt']}")
    print(f"Total Episodes: {manifest['totalEpisodes']} (Ordered Chronologically Starting with EP-001)")
    print("--------------------------------------------------------------------------------------")
    print(f"{'Ord':<4} {'Code':<8} {'Date':<12} {'Dur':<8} {'Size MB':<10} {'Thumb':<7} {'Title'}")
    print("--------------------------------------------------------------------------------------")
    for ep in sorted(manifest["episodesInOrder"], key=lambda x: (x["order"] if x["order"] > 0 else 99)):
        ord_lbl = f"#{ep['order']}" if ep['order'] > 0 else "TR"
        t_ok = "OK" if ep["thumbnailExists"] else "MISSING"
        print(f"{ord_lbl:<4} {ep['code']:<8} {ep['date']:<12} {ep['duration']:<8} {ep['videoSizeMB']:<10} {t_ok:<7} {ep['title'][:45]}...")
    print("======================================================================================")


def upload_single_episode(ep_entry: Dict[str, Any], dry_run: bool = False):
    """Executes upload of a single episode with VidIQ metadata & thumbnail."""
    print(f"\n[*] Processing {ep_entry['code']} (Order #{ep_entry['order']}): {ep_entry['title']}")
    vid_path = Path(ep_entry["videoFile"])
    thumb_path = Path(ep_entry["thumbnailFile"])
    
    if not vid_path.exists():
        print(f"[!] ERROR: Video file {vid_path} not found on disk.")
        return False
        
    if dry_run:
        print("    [DRY RUN] Would upload:")
        print(f"    - Video:     {vid_path} ({ep_entry['videoSizeMB']} MB)")
        print(f"    - Thumbnail: {thumb_path} (exists={thumb_path.exists()})")
        print(f"    - Title:     {ep_entry['title']}")
        print(f"    - Tags ({len(ep_entry['tags'])}): {', '.join(ep_entry['tags'][:5])}...")
        print("    - Category:  28 (Science & Technology)")
        print("    - Privacy:   Public")
        print("    [DRY RUN] Completed without network calls.")
        return True

    # Real Upload Path
    try:
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
    except ImportError:
        print("[!] Missing Google API dependencies.")
        return False
        
    creds = None
    if TOKEN_FILE.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                with open(TOKEN_FILE, "w") as f:
                    f.write(creds.to_json())
        except Exception as e:
            print(f"[!] Token refresh warning: {e}")
            creds = None

    if not creds or not creds.valid:
        if not CLIENT_SECRETS_FILE.exists():
            print(f"[!] Cannot upload: {CLIENT_SECRETS_FILE} missing.")
            return False
        print("[*] Launching browser OAuth consent flow via client_secrets.json...")
        flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRETS_FILE), SCOPES)
        creds = flow.run_local_server(port=8081, open_browser=True)
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())
        print(f"[+] Credentials cached at {TOKEN_FILE}")

    yt = build("youtube", "v3", credentials=creds)
    body = {
        "snippet": {
            "title": ep_entry["title"],
            "description": ep_entry["description"],
            "tags": ep_entry["tags"],
            "categoryId": "28",
            "defaultLanguage": "en",
            "defaultAudioLanguage": "en"
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False,
            "embeddable": True,
            "publicStatsViewable": True
        }
    }
    
    media = MediaFileUpload(
        str(vid_path),
        mimetype="video/mp4",
        chunksize=1024 * 1024 * 8,
        resumable=True
    )
    
    print(f"[*] Starting resumable upload for {ep_entry['code']} ({ep_entry['videoSizeMB']} MB)...")
    request = yt.videos().insert(part="snippet,status", body=body, media_body=media)
    
    response = None
    last_reported = -1
    while response is None:
        status, response = request.next_chunk()
        if status:
            pct = int(status.progress() * 100)
            if pct != last_reported and pct % 10 == 0:
                print(f"    [Upload Progress] {pct}% transmitted...")
                last_reported = pct
                
    video_id = response.get("id")
    video_url = f"https://youtu.be/{video_id}"
    print(f"[+] Video Published! Video ID: {video_id} -> {video_url}")
    
    # Attach thumbnail
    if thumb_path.exists():
        try:
            print(f"[*] Attaching custom thumbnail: {thumb_path.name}...")
            thumb_media = MediaFileUpload(str(thumb_path), mimetype="image/jpeg")
            yt.thumbnails().set(videoId=video_id, media_body=thumb_media).execute()
            print("[+] Thumbnail uploaded successfully!")
        except Exception as e:
            print(f"[!] Warning setting thumbnail: {e}")
            
    # Record to published log
    record = {
        "code": ep_entry["code"],
        "order": ep_entry["order"],
        "videoId": video_id,
        "videoUrl": video_url,
        "title": ep_entry["title"],
        "uploadedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "status": "PUBLISHED"
    }
    with open(SERVICES_DIR / "youtube_published_records.json", "a") as rf:
        rf.write(json.dumps(record) + "\n")
        
    return True


def main():
    parser = argparse.ArgumentParser(description="VidIQ Fleet Upload Pipeline for Tech Unfiltered SI")
    parser.add_argument("--dry-run", action="store_true", help="Simulate uploads with complete VidIQ metadata without network calls")
    parser.add_argument("--manifest-only", action="store_true", help="Generate and inspect the VidIQ manifest without executing uploads")
    parser.add_argument("--upload-all", action="store_true", help="Upload all 6 episodes + trailer in exact chronological order")
    parser.add_argument("--episode", type=int, default=None, help="Upload a specific episode number (1 to 6)")
    args = parser.parse_args()
    
    manifest = generate_fleet_manifest()
    print_manifest_summary(manifest)
    
    if args.manifest_only:
        print("\n[+] Manifest generated successfully at services/syndication_10channels/VIDIQ_ALL_EPISODES_FLEET_MANIFEST.json")
        return
        
    if args.episode is not None:
        target = next((ep for ep in manifest["episodesInOrder"] if ep["order"] == args.episode), None)
        if not target:
            print(f"[!] Episode #{args.episode} not found.")
            return
        upload_single_episode(target, dry_run=args.dry_run)
        return
        
    if args.upload_all or args.dry_run:
        # Sort in order: Episode 1 to 6, then Trailer
        sorted_eps = sorted(manifest["episodesInOrder"], key=lambda x: (x["order"] if x["order"] > 0 else 99))
        print(f"\n[*] Initiating sequential processing for {len(sorted_eps)} videos in chronological order starting with EP-001...")
        for ep in sorted_eps:
            success = upload_single_episode(ep, dry_run=args.dry_run)
            if not success:
                print(f"[!] Aborting remaining queue due to failure on {ep['code']}.")
                break
            time.sleep(1)


if __name__ == "__main__":
    main()
