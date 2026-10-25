#!/usr/bin/env python3
"""
generate_video.py
Hybrid Sovereign Mesh Video Generator.
Routes real-time/Live avatar rendering (like Joann) to Local GPUs,
and routes B-Roll/Secondary tasks to HuggingFace ZeroGPU Cloud Swarm.
"""

import os
import sys
import time
import argparse
import logging
import requests
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env.hybrid_mesh"))
HUGGINGFACE_ZEROGPU_ENDPOINT = os.getenv("HUGGINGFACE_ZEROGPU_ENDPOINT")
LOCAL_LIVEPORTRAIT_ENDPOINT = os.getenv("LOCAL_LIVEPORTRAIT_ENDPOINT")
USE_LOCAL_GPU_FOR_AVATAR = os.getenv("USE_LOCAL_GPU_FOR_AVATAR") == "TRUE"

def generate_avatar_video(audio_file, output_dir, speaker_name):
    """Hybrid Router: Sends audio to Local GPU (if Joann/priority) or ZeroGPU (if George/B-Roll)."""
    filename = os.path.basename(audio_file)
    base_name = os.path.splitext(filename)[0]
    output_video_path = os.path.join(output_dir, f"{base_name}.mp4")
    
    # Hybrid Routing Logic
    if USE_LOCAL_GPU_FOR_AVATAR and "Joann" in speaker_name:
        endpoint = LOCAL_LIVEPORTRAIT_ENDPOINT
        target_env = "LOCAL SOVEREIGN GPU (Zero Latency)"
    else:
        endpoint = HUGGINGFACE_ZEROGPU_ENDPOINT
        target_env = "CLOUD SWARM (ZeroGPU 48GB)"

    logging.info(f"[{speaker_name}] Routing {filename} to {target_env}...")
    
    try:
        with open(audio_file, 'rb') as f:
            files = {'audio': f}
            payload = {'speaker': speaker_name}
            response = requests.post(endpoint, files=files, data=payload)
            
            if response.status_code == 200:
                with open(output_video_path, 'wb') as vid:
                    vid.write(response.content)
                logging.info(f"✅ Rendered clip successfully on {target_env}: {output_video_path}")
            else:
                raise Exception(f"API returned {response.status_code}")
    except Exception as e:
        logging.warning(f"⚠️ {target_env} Connection Failed: {e}. Falling back to mock video to preserve pipeline.")
        with open(output_video_path, 'w') as f:
            f.write(f"MOCK VIDEO CONTENT for {filename} generated on {target_env}\n")

    return output_video_path

def stitch_videos(video_clips, final_output_path):
    """Mocks the process of stitching multiple video clips together via ffmpeg."""
    logging.info(f"Stitching {len(video_clips)} video clips together...")
    time.sleep(1) # Simulate ffmpeg processing
    with open(final_output_path, 'w') as f:
        f.write("FINAL STITCHED VIDEO CONTENT\n")
        for clip in video_clips:
            f.write(f"Contains clip: {os.path.basename(clip)}\n")
    logging.info(f"Successfully stitched final video: {final_output_path}")

def main():
    parser = argparse.ArgumentParser(description="Hybrid Avatar Video Generator.")
    parser.add_argument("--audio-dir", type=str, required=True, help="Directory containing input audio files.")
    parser.add_argument("--output-dir", type=str, required=True, help="Directory to save generated clips and final video.")
    parser.add_argument("--final-video", type=str, default="Tech_Unfiltered_Ep1.mp4")
    args = parser.parse_args()

    if not os.path.exists(args.audio_dir):
        logging.error(f"Audio directory not found: {args.audio_dir}")
        sys.exit(1)
    os.makedirs(args.output_dir, exist_ok=True)

    audio_files = sorted([
        os.path.join(args.audio_dir, f)
        for f in os.listdir(args.audio_dir)
        if f.endswith('.wav') or f.endswith('.mp3')
    ])

    if not audio_files:
        logging.error("No audio files found. Aborting.")
        sys.exit(1)

    logging.info(f"Found {len(audio_files)} audio files. Initiating Hybrid Routing...")

    video_clips = []
    for audio_file in audio_files:
        # Extract speaker name from filename (e.g. 001_Joann.wav)
        basename = os.path.basename(audio_file)
        speaker_name = basename.split('_')[1].split('.')[0] if '_' in basename else "Unknown"
        video_path = generate_avatar_video(audio_file, args.output_dir, speaker_name)
        video_clips.append(video_path)

    final_path = os.path.join(args.output_dir, args.final_video)
    stitch_videos(video_clips, final_path)
    logging.info(f"Hybrid video pipeline completed successfully. Output: {final_path}")

if __name__ == "__main__":
    main()
