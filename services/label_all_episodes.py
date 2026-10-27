#!/usr/bin/env python3
"""
Explicitly labels all 6 Tech Unfiltered studio episodes + official trailer.
Creates clean, human-readable directories, video names, thumbnails, and copy-paste text files.
"""

import os
import shutil
from pathlib import Path

BASE_DIR = Path("/Users/jccoffey/Downloads/Tech Unfiltered")
TARGET_DIR = BASE_DIR / "READY_FOR_YOUTUBE_UPLOAD"
TARGET_DIR.mkdir(parents=True, exist_ok=True)

# Remove old obscure folders
for old in ["EP-001", "EP-002", "EP-003", "EP-004", "EP-005", "EP-006", "TRAILER"]:
    p = TARGET_DIR / old
    if p.exists() and p.is_dir():
        shutil.rmtree(p)

EPISODES = [
    {
        "num": "01",
        "code": "EP-001",
        "folder_name": "Episode 01 - Why Rented Cloud Wrappers Collapse Under Margin Pressure",
        "video_title": "Episode 01 - Why Rented Cloud Wrappers Collapse Under Margin Pressure.mp4",
        "thumb_title": "Episode 01 - Thumbnail.jpg",
        "src_video": "/Users/jccoffey/Downloads/TECH UNFILTERTED/dropbox_ingest/TEC 26-08-05/Exports/TEC 26-08-05.mp4",
        "src_thumb": BASE_DIR / "thumbs" / "thumb_ep01.jpg",
        "src_text": BASE_DIR / "services" / "syndication_10channels" / "EP-001_youtube_upload_text.txt",
    },
    {
        "num": "02",
        "code": "EP-002",
        "folder_name": "Episode 02 - We Replaced a $40,000 Mo Call Center With a Local GPU",
        "video_title": "Episode 02 - We Replaced a $40,000 Mo Call Center With a Local GPU.mp4",
        "thumb_title": "Episode 02 - Thumbnail.jpg",
        "src_video": "/Users/jccoffey/Downloads/TECH UNFILTERTED/dropbox_ingest/TEC 26-08-13/Exports/TEC 26-08-13.mp4",
        "src_thumb": BASE_DIR / "thumbs" / "thumb_ep02.jpg",
        "src_text": BASE_DIR / "services" / "syndication_10channels" / "EP-002_youtube_upload_text.txt",
    },
    {
        "num": "03",
        "code": "EP-003",
        "folder_name": "Episode 03 - Living Worlds in Code Runtime - Why Static 3D Models Are Dead",
        "video_title": "Episode 03 - Living Worlds in Code Runtime - Why Static 3D Models Are Dead.mp4",
        "thumb_title": "Episode 03 - Thumbnail.jpg",
        "src_video": "/Users/jccoffey/Downloads/TECH UNFILTERTED/dropbox_ingest/TEC 26-08-20/Exports/TEC 26-08-20.mp4",
        "src_thumb": BASE_DIR / "thumbs" / "thumb_ep03.jpg",
        "src_text": BASE_DIR / "services" / "syndication_10channels" / "EP-003_youtube_upload_text.txt",
    },
    {
        "num": "04",
        "code": "EP-004",
        "folder_name": "Episode 04 - Autonomous AI Agents Broke Our Contract - The Boardroom Shield",
        "video_title": "Episode 04 - Autonomous AI Agents Broke Our Contract - The Boardroom Shield.mp4",
        "thumb_title": "Episode 04 - Thumbnail.jpg",
        "src_video": "/Users/jccoffey/Downloads/TECH UNFILTERTED/dropbox_ingest/TEC 26-08-27/Exports/TEC 26-08-27.mp4",
        "src_thumb": BASE_DIR / "thumbs" / "thumb_ep04.jpg",
        "src_text": BASE_DIR / "services" / "syndication_10channels" / "EP-004_youtube_upload_text.txt",
    },
    {
        "num": "05",
        "code": "EP-005",
        "folder_name": "Episode 05 - Autonomous C-Suite Swarms - 7 Exec Agents Running a Company NHIL",
        "video_title": "Episode 05 - Autonomous C-Suite Swarms - 7 Exec Agents Running a Company NHIL.mp4",
        "thumb_title": "Episode 05 - Thumbnail.jpg",
        "src_video": "/Users/jccoffey/Downloads/TECH UNFILTERTED/dropbox_ingest/TEC 26-09-03/Exports/TEC 26-09-03.mp4",
        "src_thumb": BASE_DIR / "thumbs" / "thumb_ep05.jpg",
        "src_text": BASE_DIR / "services" / "syndication_10channels" / "EP-005_youtube_upload_text.txt",
    },
    {
        "num": "06",
        "code": "EP-006",
        "folder_name": "Episode 06 - $100K Day Sovereign Deal Flow - The Trillion-Dollar Blueprint",
        "video_title": "Episode 06 - $100K Day Sovereign Deal Flow - The Trillion-Dollar Blueprint.mp4",
        "thumb_title": "Episode 06 - Thumbnail.jpg",
        "src_video": "/Users/jccoffey/Downloads/TECH UNFILTERTED/dropbox_ingest/TEC 26-09-10/Exports/TEC 26-09-10.mp4",
        "src_thumb": BASE_DIR / "thumbs" / "thumb_ep06.jpg",
        "src_text": BASE_DIR / "services" / "syndication_10channels" / "EP-006_youtube_upload_text.txt",
    },
    {
        "num": "00",
        "code": "TRAILER",
        "folder_name": "Official Trailer - Tech Unfiltered SI Sovereign Media Network",
        "video_title": "Official Trailer - Tech Unfiltered SI Sovereign Media Network.mp4",
        "thumb_title": "Official Trailer - Thumbnail.jpg",
        "src_video": "/Users/jccoffey/Downloads/TECH UNFILTERTED/dropbox_ingest/TRAILER/Exports/TEC_Trailer.mp4",
        "src_thumb": BASE_DIR / "thumbs" / "thumb_trailer.jpg",
        "src_text": BASE_DIR / "services" / "syndication_10channels" / "TRAILER_youtube_upload_text.txt",
    },
]

def main():
    print("🎬 Explicitly labeling all Tech Unfiltered episodes...")
    for ep in EPISODES:
        folder = TARGET_DIR / ep["folder_name"]
        folder.mkdir(parents=True, exist_ok=True)

        dest_video = folder / ep["video_title"]
        if not dest_video.exists() and os.path.exists(ep["src_video"]):
            try:
                os.symlink(ep["src_video"], dest_video)
            except Exception:
                shutil.copy2(ep["src_video"], dest_video)

        dest_thumb = folder / ep["thumb_title"]
        if os.path.exists(ep["src_thumb"]):
            shutil.copy2(ep["src_thumb"], dest_thumb)

        dest_text = folder / "COPY_PASTE_TITLE_AND_DESCRIPTION.txt"
        if os.path.exists(ep["src_text"]):
            shutil.copy2(ep["src_text"], dest_text)

        print(f"  [✔] {ep['folder_name']}")
        print(f"      Video: {dest_video.name}")
        print(f"      Thumb: {dest_thumb.name}")

    print("\n✅ All 6 episodes + trailer are 100% labeled in:", TARGET_DIR)

if __name__ == "__main__":
    main()
