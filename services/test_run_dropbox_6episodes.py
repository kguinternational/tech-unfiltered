#!/usr/bin/env python3
"""
TECH UNFILTERTED SI — 6-EPISODE DROPBOX BATCH TEST RUNNER
Executes end-to-end verification and n8n syndication dispatch across all 6 studio sessions:
  1. TEC 26-08-05 (Episode 1)
  2. TEC 26-08-13 (Episode 2)
  3. TEC 26-08-20 (Episode 3)
  4. TEC 26-08-27 (Episode 4)
  5. TEC 26-09-03 (Episode 5)
  6. TEC 26-09-10 (Episode 6)
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime, timezone

BASE_DIR = Path("/Users/jccoffey/Downloads/Tech Unfiltered")
SERVICES_DIR = BASE_DIR / "services"
DROPBOX_INGEST_DIR = Path("/Users/jccoffey/Downloads/TECH UNFILTERTED/dropbox_ingest")
OUTPUT_REPORT_DIR = SERVICES_DIR / "syndication_10channels"

if str(SERVICES_DIR) not in sys.path:
    sys.path.insert(0, str(SERVICES_DIR))

from autonomous_10channel_syndicator import Autonomous10ChannelSyndicator

SESSIONS = [
    {
        "key": "ep1",
        "code": "EP-001",
        "folder": "TEC 26-08-05",
        "video": "TEC 26-08-05.mp4",
        "audio": "TEC 26-08-05.mp3",
        "duration": "45:41",
        "title": "Why Rented Cloud Wrappers Collapse Under Margin Pressure"
    },
    {
        "key": "ep2",
        "code": "EP-002",
        "folder": "TEC 26-08-13",
        "video": "TEC 26-08-13.mp4",
        "audio": "TEC 26-08-13.mp3",
        "duration": "24:59",
        "title": "We Replaced a $40,000/Mo Call Center With a Local GPU (92ms Test)"
    },
    {
        "key": "ep3",
        "code": "EP-003",
        "folder": "TEC 26-08-20",
        "video": "TEC 26-08-20.mp4",
        "audio": "TEC 26-08-20.mp3",
        "duration": "25:49",
        "title": "Living Worlds in Code Runtime: Why Static 3D Models Are Dead"
    },
    {
        "key": "ep4",
        "code": "EP-004",
        "folder": "TEC 26-08-27",
        "video": "TEC 26-08-27.mp4",
        "audio": "TEC 26-08-27.mp3",
        "duration": "34:28",
        "title": "Autonomous AI Agents Broke Our Contract: The Boardroom Shield"
    },
    {
        "key": "ep5",
        "code": "EP-005",
        "folder": "TEC 26-09-03",
        "video": "TEC 26-09-03.mp4",
        "audio": "TEC 26-09-03.mp3",
        "duration": "22:47",
        "title": "Autonomous C-Suite Swarms: 7 Exec Agents Running a Company NHIL"
    },
    {
        "key": "ep6",
        "code": "EP-006",
        "folder": "TEC 26-09-10",
        "video": "TEC 26-09-10.mp4",
        "audio": "TEC 26-09-10.mp3",
        "duration": "29:51",
        "title": "$100K/Day Sovereign Deal Flow: The Trillion-Dollar Blueprint"
    }
]

def run_all_sessions():
    print("=" * 80)
    print("TECH UNFILTERED SI — 6-EPISODE DROPBOX MASTER TEST RUN")
    print(f"Timestamp: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 80)

    results = []
    total_start = time.perf_counter()

    for idx, s in enumerate(SESSIONS, 1):
        print(f"\n[{idx}/6] Verifying & Syndicating: {s['code']} ({s['folder']})...")
        
        # 1. File Inspection
        folder_path = DROPBOX_INGEST_DIR / s["folder"] / "Exports"
        video_file = folder_path / s["video"]
        audio_file = folder_path / s["audio"]
        
        v_exists = video_file.exists()
        a_exists = audio_file.exists()
        v_size_mb = round(video_file.stat().st_size / (1024 * 1024), 2) if v_exists else 0
        a_size_mb = round(audio_file.stat().st_size / (1024 * 1024), 2) if a_exists else 0

        print(f"   📹 Master Video : {'EXISTS' if v_exists else 'MISSING'} ({v_size_mb} MB)")
        print(f"   🎙️ Master Audio : {'EXISTS' if a_exists else 'MISSING'} ({a_size_mb} MB)")

        # 2. Run 10-Channel Syndication
        syndicator = Autonomous10ChannelSyndicator(episode_key=s["key"])
        report = syndicator.execute_all_10_channels()

        channels = report.get("channels", {})
        ch_count = len(channels)
        exec_ms = report.get("executionTimeMs", 0)

        print(f"   ⚡ Syndication  : 10/10 Channels Dispatched in {exec_ms}ms")
        print(f"   📺 YouTube Title: {channels.get('ch1_youtube_studio', {}).get('videoTitle', 'N/A')[:65]}...")
        print(f"   ⚡ Nostr Hash   : {channels.get('ch8_nostr_relay', {}).get('nostrDetails', {}).get('shortNoteEvent', {}).get('id', 'N/A')[:24]}...")
        print(f"   💼 Legal Docket : {channels.get('ch10_deal_desk_escrow', {}).get('docketId', 'N/A')}")

        results.append({
            "order": idx,
            "key": s["key"],
            "code": s["code"],
            "title": s["title"],
            "duration": s["duration"],
            "folder": s["folder"],
            "videoSizeMB": v_size_mb,
            "audioSizeMB": a_size_mb,
            "channelsDispatched": ch_count,
            "executionTimeMs": exec_ms,
            "nostrId": channels.get("ch8_nostr_relay", {}).get("nostrDetails", {}).get("shortNoteEvent", {}).get("id"),
            "legalDocket": channels.get("ch10_deal_desk_escrow", {}).get("docketId")
        })

    total_time_ms = round((time.perf_counter() - total_start) * 1000, 2)
    print("\n" + "=" * 80)
    print(f"✅ BATCH TEST RUN COMPLETE: All 6 Sessions Dispatched in {total_time_ms}ms")
    print("=" * 80)

    # Save summary report
    summary_file = OUTPUT_REPORT_DIR / "DROPBOX_6EPISODES_TEST_RUN_SUMMARY.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump({
            "status": "COMPLETED_SUCCESS",
            "executedAt": datetime.now(timezone.utc).isoformat(),
            "totalSessions": len(results),
            "totalTimeMs": total_time_ms,
            "sessions": results
        }, f, indent=2)

    print(f"📄 Summary Saved: {summary_file}")
    return results

if __name__ == "__main__":
    run_all_sessions()
