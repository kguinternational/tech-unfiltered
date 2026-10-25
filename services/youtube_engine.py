#!/usr/bin/env python3
"""
Autonomous YouTube Automation Engine for Tech Unfiltered SI
Powered by KGU International · Physical Superintelligence Division
Channel ID: UCbqX5P2ISaU5QGHEIVh3MoA
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Optional, Dict, Any

try:
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
except ImportError:
    print("Error: Missing Google API dependencies. Run:")
    print("python3 -m pip install --user --break-system-packages google-api-python-client google-auth-oauthlib google-auth-httplib2")
    sys.exit(1)

SCOPES = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtubepartner",
]

CHANNEL_ID = "UCbqX5P2ISaU5QGHEIVh3MoA"
BASE_DIR = Path(__file__).resolve().parent
TOKEN_FILE = BASE_DIR / "token.json"
CLIENT_SECRETS_FILE = BASE_DIR / "client_secrets.json"
ENV_FILE = BASE_DIR.parent / ".env"

def load_env() -> Dict[str, str]:
    env = {}
    if ENV_FILE.exists():
        with open(ENV_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env[k.strip()] = v.strip().strip("'\"")
    return env

def get_credentials() -> Optional[Credentials]:
    """Retrieve or generate valid user OAuth credentials."""
    creds = None
    env = load_env()

    # 1. Check cached token
    if TOKEN_FILE.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
        except Exception as e:
            print(f"[!] Warning reading {TOKEN_FILE}: {e}")

    # 2. Check environment credentials
    client_id = os.environ.get("YOUTUBE_CLIENT_ID") or env.get("YOUTUBE_CLIENT_ID")
    client_secret = os.environ.get("YOUTUBE_CLIENT_SECRET") or env.get("YOUTUBE_CLIENT_SECRET")
    refresh_token = os.environ.get("YOUTUBE_REFRESH_TOKEN") or env.get("YOUTUBE_REFRESH_TOKEN")

    if not creds and client_id and client_secret and refresh_token:
        creds = Credentials(
            None,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=client_id,
            client_secret=client_secret,
            scopes=SCOPES,
        )

    # 3. Refresh if expired
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            with open(TOKEN_FILE, "w") as token:
                token.write(creds.to_json())
        except Exception as e:
            print(f"[!] Failed to refresh token: {e}")
            creds = None

    # 4. If still invalid, check client_secrets.json
    if not creds:
        if CLIENT_SECRETS_FILE.exists():
            print("[*] Launching browser OAuth consent flow via client_secrets.json...")
            flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRETS_FILE), SCOPES)
            creds = flow.run_local_server(port=8080)
            with open(TOKEN_FILE, "w") as token:
                token.write(creds.to_json())
            print(f"[+] Credentials saved to {TOKEN_FILE}")
        elif client_id and client_secret:
            client_config = {
                "installed": {
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": ["http://localhost:8080/"]
                }
            }
            flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
            creds = flow.run_local_server(port=8080)
            with open(TOKEN_FILE, "w") as token:
                token.write(creds.to_json())
            print(f"[+] Credentials saved to {TOKEN_FILE}")

    return creds

def get_youtube_service():
    creds = get_credentials()
    if not creds or not creds.valid:
        print("[!] No valid YouTube credentials found.")
        print("[!] To authorize:")
        print(f"    1. Place client_secrets.json in {CLIENT_SECRETS_FILE}")
        print("    2. Or set YOUTUBE_CLIENT_ID & YOUTUBE_CLIENT_SECRET in .env")
        print("    3. Then run: python3 services/youtube_engine.py --login")
        return None
    return build("youtube", "v3", credentials=creds)

def cmd_status():
    """Fetch live channel information and branding status."""
    yt = get_youtube_service()
    if not yt:
        return
    res = yt.channels().list(
        part="snippet,statistics,brandingSettings",
        id=CHANNEL_ID
    ).execute()
    
    items = res.get("items", [])
    if not items:
        print(f"[!] Channel {CHANNEL_ID} not found.")
        return
    ch = items[0]
    snippet = ch.get("snippet", {})
    stats = ch.get("statistics", {})
    branding = ch.get("brandingSettings", {})

    print("\n" + "="*60)
    print(" TECH UNFILTERED SI — YOUTUBE CHANNEL STATUS")
    print(" Powered by KGU International")
    print("="*60)
    print(f"Title:        {snippet.get('title')}")
    print(f"Custom URL:   {snippet.get('customUrl', 'N/A')}")
    print(f"Subscribers:  {stats.get('subscriberCount', 0)}")
    print(f"Total Views:  {stats.get('viewCount', 0)}")
    print(f"Videos:       {stats.get('videoCount', 0)}")
    print(f"Banner URL:   {branding.get('image', {}).get('bannerExternalUrl', 'Not set')}")
    print("="*60 + "\n")

def cmd_update_banner(image_path: str):
    """Upload banner image and attach to channel."""
    yt = get_youtube_service()
    if not yt:
        return
    path = Path(image_path).resolve()
    if not path.exists():
        print(f"[!] Image not found: {path}")
        return

    print(f"[*] Uploading banner image: {path.name} ({path.stat().st_size / (1024*1024):.2f} MB)...")
    media = MediaFileUpload(str(path), mimetype="image/png", resumable=True)
    
    # 1. Insert channel banner
    banner_res = yt.channelBanners().insert(channelId=CHANNEL_ID, media_body=media).execute()
    banner_url = banner_res.get("url")
    print(f"[+] Banner uploaded successfully: {banner_url}")

    # 2. Update channel branding settings
    print("[*] Applying banner to channel brandingSettings...")
    yt.channels().update(
        part="brandingSettings",
        body={
            "id": CHANNEL_ID,
            "brandingSettings": {
                "image": {
                    "bannerExternalUrl": banner_url
                }
            }
        }
    ).execute()
    print("[+] Channel banner updated successfully!")

def cmd_upload_video(file_path: str, title: str, description: str, tags: str, category_id: str = "28"):
    """Upload a video with automated Physical SI metadata."""
    yt = get_youtube_service()
    if not yt:
        return
    path = Path(file_path).resolve()
    if not path.exists():
        print(f"[!] Video file not found: {path}")
        return

    tag_list = [t.strip() for t in tags.split(",") if t.strip()]
    if "Tech Unfiltered" not in tag_list:
        tag_list.extend(["Tech Unfiltered SI", "Physical Superintelligence", "KGU International", "Embodied AI", "Joann Coffey", "George Dubec"])

    body = {
        "snippet": {
            "title": title,
            "description": f"{description}\n\n---\nTech Unfiltered SI · Physical Superintelligence\nPowered by KGU International\nhttps://techunfiltered.si",
            "tags": tag_list,
            "categoryId": category_id
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False
        }
    }

    print(f"[*] Uploading video: {title} ({path.name})...")
    media = MediaFileUpload(str(path), chunksize=-1, resumable=True)
    request = yt.videos().insert(part="snippet,status", body=body, media_body=media)
    
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"    Upload progress: {int(status.progress() * 100)}%")
            
    print(f"[+] Video uploaded successfully! Video ID: {response.get('id')}")
    print(f"    URL: https://youtu.be/{response.get('id')}")

def main():
    parser = argparse.ArgumentParser(description="Tech Unfiltered SI — Autonomous YouTube Engine")
    # Also support top-level flags for convenience
    parser.add_argument("--login", action="store_true", help="Launch interactive OAuth consent flow")
    parser.add_argument("--status", action="store_true", help="Get channel status and statistics")
    parser.add_argument("--sync-branding", action="store_true", help="Sync staged branding assets")

    subparsers = parser.add_subparsers(dest="command")

    # Status
    subparsers.add_parser("status", help="Get channel status and statistics")

    # Login
    subparsers.add_parser("login", help="Launch interactive OAuth consent flow")

    # Update Banner
    p_banner = subparsers.add_parser("update-banner", help="Upload and set new channel banner")
    p_banner.add_argument("image", help="Path to 2048x1152 banner image")

    # Upload Video
    p_video = subparsers.add_parser("upload-video", help="Upload a video to the channel")
    p_video.add_argument("file", help="Path to MP4 video file")
    p_video.add_argument("--title", required=True, help="Video title")
    p_video.add_argument("--description", default="Tech Unfiltered SI Episode Master.", help="Video description")
    p_video.add_argument("--tags", default="AI,Physical SI,Robotics,KGU", help="Comma-separated tags")

    # Sync All Branding
    subparsers.add_parser("sync-branding", help="Sync all staged branding assets to YouTube Studio")

    args = parser.parse_args()

    cmd = args.command
    if args.login:
        cmd = "login"
    elif args.status:
        cmd = "status"
    elif args.sync_branding:
        cmd = "sync-branding"

    if cmd == "status":
        cmd_status()
    elif cmd == "login":
        creds = get_credentials()
        if creds and creds.valid:
            print("[+] Successfully authenticated and cached token!")
            cmd_status()
    elif cmd == "update-banner":
        cmd_update_banner(args.image)
    elif cmd == "upload-video":
        cmd_upload_video(args.file, args.title, args.description, args.tags)
    elif cmd == "sync-branding":
        staged_banner = Path.home() / "Downloads" / "YouTube_Branding_Tech_Unfiltered_SI" / "1_BANNER_2048x1152_6MB.png"
        if staged_banner.exists():
            cmd_update_banner(str(staged_banner))
        else:
            print(f"[!] Staged banner not found at {staged_banner}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
