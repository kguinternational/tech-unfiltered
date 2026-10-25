import os
import re
import argparse
import requests
from dotenv import load_dotenv

# Load the Hybrid Sovereign Mesh Router config
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env.hybrid_mesh"))

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
COLAB_T4_ENDPOINT = os.getenv("COLAB_T4_ENDPOINT")
LOCAL_XTTS_ENDPOINT = os.getenv("LOCAL_XTTS_ENDPOINT")
USE_LOCAL_GPU_FOR_VOICE = os.getenv("USE_LOCAL_GPU_FOR_VOICE") == "TRUE"

def generate_tts(speaker, text, output_filename):
    """
    Hybrid Router: Sends the payload to the Local GPU (Tier 1) for primary hosts, 
    or to the free Colab T4 endpoint (Tier 2) for others.
    """
    if USE_LOCAL_GPU_FOR_VOICE and speaker == "Joann":
        endpoint = LOCAL_XTTS_ENDPOINT
        target_env = "LOCAL SOVEREIGN GPU (Zero Latency)"
    else:
        endpoint = COLAB_T4_ENDPOINT
        target_env = "CLOUD SWARM (Colab T4)"

    print(f"[HYBRID TTS] Routing {speaker} to {target_env} | Output: {output_filename}")
    
    payload = {
        "text": text,
        "speaker": speaker,
        "api_key": OPENROUTER_API_KEY # Fallback authentication if routing to cloud
    }
    
    try:
        response = requests.post(endpoint, json=payload)
        
        if response.status_code == 200:
            with open(output_filename, 'wb') as f:
                f.write(response.content)
            print(f"✅ Successfully generated audio for {speaker} on {target_env}")
        else:
            print(f"⚠️ Warning: {target_env} returned {response.status_code}. Generating fallback silent audio...")
            write_fallback_audio(output_filename)
    except Exception as e:
        print(f"⚠️ Connection to {target_env} Failed: {e}. Generating fallback silent audio...")
        write_fallback_audio(output_filename)

def write_fallback_audio(output_filename):
    import wave, struct
    if output_filename.endswith(".wav"):
        with wave.open(output_filename, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(24000)
            wf.writeframes(struct.pack('<h', 0) * 12000)
    else:
        with open(output_filename, 'wb') as f:
            f.write(b'\x00' * 1024)

def parse_and_generate(markdown_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(markdown_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    dialogue_pattern = re.compile(r'^\s*[\*]*\[(George|Joann)\][\*]*\s*:[\*]*\s*(.*)', re.IGNORECASE)
    
    line_count = 1
    for line in lines:
        match = dialogue_pattern.match(line)
        if match:
            speaker = match.group(1).capitalize()
            text = match.group(2).strip()
            text = re.sub(r'[*_]', '', text)
            
            if not text:
                continue
                
            output_filename = os.path.join(output_dir, f"{line_count:03d}_{speaker}.wav")
            generate_tts(speaker, text, output_filename)
            line_count += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse podcast script and generate Hybrid TTS audio.")
    parser.add_argument("--script", default="/Users/jccoffey/Documents/KGU International/1. Internal Operations & Tech/Tech Unfiltered/podcast_scripts/Ep1_The_Unimaginable.md")
    parser.add_argument("--output", default="./audio_output")
    args = parser.parse_args()
    
    print(f"Reading script from: {args.script}")
    if os.path.exists(args.script):
        parse_and_generate(args.script, args.output)
    else:
        print(f"Error: Script file not found at {args.script}")
