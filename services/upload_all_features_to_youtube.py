#!/usr/bin/env python3
"""
Tech Unfiltered SI — Master YouTube Upload Pipeline (All Features)
Uploads Episode 01 Studio Master with:
- Clickable Chapter Timestamps
- Day-1 High-Ticket Monetization Funnel ($10K, $25K, $150K)
- SEO Tags & Category 28 Science & Tech
- Custom Verified Cover Artwork Thumbnail
- Resumable Chunked Upload Engine
"""

import os
import sys
import json
import time
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent
TOKEN_FILE = BASE_DIR / "token.json"
CLIENT_SECRETS_FILE = BASE_DIR / "client_secrets.json"

SCOPES = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtubepartner"
]

VIDEO_PATH = ROOT_DIR / "videos" / "tec_26_08_05.mp4"
THUMBNAIL_PATH = ROOT_DIR / "cover_art.png"

TITLE = "Episode 01: The Architecture of SI & Sovereign Hardware Nodes | Tech Unfiltered SI"

DESCRIPTION = """Episode 01 of Tech Unfiltered SI — The #1 Superintelligence (SI) Broadcast.
Recorded live in our Boca Raton Studio with Joann Coffey (CEO, KGU International) and George Dubec (CRO).

⚡ DEPLOY 24/7 SOVEREIGN VOICE AI OR SPONSOR THE SHOW:
• 24/7 AI Call Center Deployment ($25,000): https://techunfiltered.fm/#sponsor
• Podcast Episode Sponsorship ($10,000): https://techunfiltered.fm/#sponsor
• Dedicated Sovereign Hardware Node ($150,000): https://techunfiltered.fm/#sponsor
• Direct Studio Hotline: 1-888-KGU-SOVEREIGN

CHAPTERS & TIMESTAMPS:
00:00 — Welcome to Tech Unfiltered SI (Boca Raton Studio)
03:00 — Why Rented Cloud Wrappers Collapse Under Margin Pressure
09:00 — Dedicated Sovereign Hardware Nodes ($0.00 Token Tax)
17:00 — After Swiping & Autonomous Digital Twin Interactions
28:40 — Zero-Human-Bottleneck (NHIL) Operations
38:15 — Physical SI & The Energy Bottleneck
44:20 — Next Broadcast Preview & Sovereign Retainers

KEY EXECUTIVE TAKEAWAYS:
1. Dedicated Sovereign Hardware Nodes outperform rented cloud wrappers by 10x with zero marginal token tax.
2. 100% NHIL (No-Human-In-The-Loop) corporate governance eliminates manual SaaS seat overhead.
3. Physical SI embodiment unites robotics, grid telemetry, and sovereign capital velocity.

HOSTS:
• Joann Coffey — Founder & CEO, KGU International
• George Dubec — Chief Revenue Officer & Co-Host

OFFICIAL PLATFORMS:
• Interactive Broadcast Vault: http://localhost:5050/landing_page.html
• Executive Deal Desk: http://localhost:3333/admin
• Verified Audio Feed: http://localhost:5050/audio/tec_26_08_05.mp3

#TechUnfiltered #Superintelligence #PhysicalSI #KGUInternational #JoannCoffey #GeorgeDubec #AIHardware #AICallCenter"""

TAGS = [
    "Tech Unfiltered SI",
    "Tech Unfiltered",
    "Physical Superintelligence",
    "KGU International",
    "Joann Coffey",
    "George Dubec",
    "Boca Raton Studio",
    "Dedicated Sovereign Hardware Nodes",
    "AI Call Center",
    "Autonomous Enterprise",
    "Digital Twins",
    "NHIL",
    "Superintelligence",
    "Voice AI"
]

def get_authenticated_service():
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
            print(f"[!] Error: {CLIENT_SECRETS_FILE} missing.")
            return None
        print("[*] Launching browser authorization for YouTube Upload...")
        flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRETS_FILE), SCOPES)
        creds = flow.run_local_server(port=8080, open_browser=True)
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())
        print(f"[+] Token cached successfully at {TOKEN_FILE}")

    return build("youtube", "v3", credentials=creds)

def upload_episode():
    if not VIDEO_PATH.exists():
        print(f"[!] Video file not found: {VIDEO_PATH}")
        return

    print("==================================================================")
    print("TECH UNFILTERED SI — YOUTUBE UPLOAD PIPELINE (ALL FEATURES)")
    print("==================================================================")
    print(f"Video File:  {VIDEO_PATH} ({VIDEO_PATH.stat().st_size / (1024*1024):.1f} MB)")
    print(f"Thumbnail:   {THUMBNAIL_PATH}")
    print(f"Title:       {TITLE}")
    print("------------------------------------------------------------------")

    yt = get_authenticated_service()
    if not yt:
        return

    body = {
        "snippet": {
            "title": TITLE,
            "description": DESCRIPTION,
            "tags": TAGS,
            "categoryId": "28", # Science & Technology
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
        str(VIDEO_PATH),
        mimetype="video/mp4",
        chunksize=1024 * 1024 * 8, # 8MB chunks for stable resumable upload
        resumable=True
    )

    print("[*] Initiating resumable video upload chunk transmission...")
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
    print(f"[+] Video Published! Video ID: {video_id}")
    print(f"[+] Direct URL: {video_url}")

    # Set Custom Thumbnail (All Features)
    if THUMBNAIL_PATH.exists():
        try:
            print(f"[*] Setting custom high-res thumbnail ({THUMBNAIL_PATH.name})...")
            thumb_media = MediaFileUpload(str(THUMBNAIL_PATH), mimetype="image/png")
            yt.thumbnails().set(videoId=video_id, media_body=thumb_media).execute()
            print("[+] Custom thumbnail uploaded and attached successfully!")
        except Exception as e:
            print(f"[!] Warning setting thumbnail: {e}")

    # Save to uploaded records
    record = {
        "videoId": video_id,
        "videoUrl": video_url,
        "title": TITLE,
        "uploadedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "status": "PUBLISHED",
        "features": {
            "chapters": True,
            "customThumbnail": THUMBNAIL_PATH.exists(),
            "monetizationFunnel": True,
            "tagsCount": len(TAGS),
            "category": "28 (Science & Technology)"
        }
    }

    with open(BASE_DIR / "youtube_published_records.json", "a") as rf:
        rf.write(json.dumps(record) + "\n")

    print("==================================================================")
    print("SUCCESS: Tech Unfiltered SI Episode 01 is Live on YouTube with All Features!")
    print(f"URL: {video_url}")
    print("==================================================================")
    return video_url

if __name__ == "__main__":
    upload_episode()
