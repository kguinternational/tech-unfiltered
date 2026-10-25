#!/usr/bin/env bash
# ========================================================================================
# TECH UNFILTERED SI & KGU INTERNATIONAL — VIDIQ FLEET UPLOAD LAUNCHER
# ========================================================================================
# Uploads all 6 studio episodes + trailer in exact chronological order starting with EP-001
# with complete VidIQ metadata, custom 1280x720 thumbnails, chapter timestamps,
# and high-ticket day-1 monetization funnels.
# ========================================================================================

set -euo pipefail
cd "/Users/jccoffey/Documents/KGU International/1. Internal Operations & Tech/Tech Unfiltered"

echo "=================================================================================="
echo "🚀 TECH UNFILTERED SI — VIDIQ MASTER FLEET UPLOAD ENGINE"
echo "=================================================================================="
echo "Starting Episode Order: EP-001 through EP-006 + Official Trailer"
echo "----------------------------------------------------------------------------------"

python3 services/vidiq_fleet_upload_pipeline.py --upload-all "$@"
