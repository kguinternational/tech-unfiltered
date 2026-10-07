import os
import re
import argparse

def mock_tts_generate(speaker, text, output_filename):
    """
    Mock function to simulate TTS generation.
    In a real implementation, this would interact with a local TTS engine 
    (like Coqui TTS, Voicebox, etc.) to synthesize audio and save it to the output file.
    """
    print(f"[MOCK TTS] Speaker: {speaker} | Output: {output_filename}")
    print(f"           Text: {text}")
    # Example of actual TTS call:
    # tts.tts_to_file(text=text, speaker=speaker, file_path=output_filename)

def parse_and_generate(markdown_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(markdown_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Matches lines like:
    # [George]: text
    # **[Joann]**: text
    # **[George]:** text
    dialogue_pattern = re.compile(r'^\s*[\*]*\[(George|Joann)\][\*]*\s*:[\*]*\s*(.*)', re.IGNORECASE)
    
    line_count = 1
    for line in lines:
        match = dialogue_pattern.match(line)
        if match:
            speaker = match.group(1).capitalize()
            text = match.group(2).strip()
            
            # Clean up text for TTS (remove markdown asterisks and underscores)
            text = re.sub(r'[*_]', '', text)
            
            # Ignore empty lines
            if not text:
                continue
                
            output_filename = os.path.join(output_dir, f"{line_count:03d}_{speaker}.wav")
            mock_tts_generate(speaker, text, output_filename)
            line_count += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse podcast script and generate TTS audio.")
    parser.add_argument(
        "--script", 
        default="/Users/jccoffey/Documents/KGU International/1. Internal Operations & Tech/Tech Unfiltered/podcast_scripts/Ep1_The_Unimaginable.md",
        help="Path to the markdown script."
    )
    parser.add_argument(
        "--output", 
        default="./audio_output",
        help="Directory to save the generated wav files."
    )
    
    args = parser.parse_args()
    
    print(f"Reading script from: {args.script}")
    print(f"Outputting audio to: {args.output}")
    
    if not os.path.exists(args.script):
        print(f"Error: Script file not found at {args.script}")
    else:
        parse_and_generate(args.script, args.output)
        print("Done processing script.")
