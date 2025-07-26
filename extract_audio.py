#!/usr/bin/env python3
"""
Audio Extractor from Video Files
Extracts high-quality audio from video files using ffmpeg with optimal settings.
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path


def extract_audio(video_path: str, output_path: str = None, quality: str = "high") -> str:
    """
    Extract audio from video file with specified quality.
    
    Args:
        video_path: Path to the video file
        output_path: Path for the output audio file (optional)
        quality: Audio quality ('high', 'medium', 'low')
        
    Returns:
        Path to the extracted audio file
    """
    video_path = Path(video_path)
    
    if not video_path.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")
    
    # Determine output path
    if output_path is None:
        output_path = video_path.parent / f"{video_path.stem}_audio.wav"
    else:
        output_path = Path(output_path)
    
    # Quality settings
    quality_settings = {
        "high": {
            "sample_rate": "48000",
            "bit_depth": "24",
            "filters": "highpass=f=80,lowpass=f=8000,volume=1.2,compand=0.3|0.3:1|1:-90/-60/-40/-30/-20/-10/-3/0:6:0:-90:0.2"
        },
        "medium": {
            "sample_rate": "44100", 
            "bit_depth": "16",
            "filters": "highpass=f=100,lowpass=f=6000,volume=1.1"
        },
        "low": {
            "sample_rate": "16000",
            "bit_depth": "16", 
            "filters": "highpass=f=200,lowpass=f=3000,volume=1.0"
        }
    }
    
    settings = quality_settings.get(quality, quality_settings["medium"])
    
    print(f"Extracting {quality} quality audio from: {video_path}")
    print(f"Output: {output_path}")
    
    # Build ffmpeg command
    cmd = [
        'ffmpeg',
        '-i', str(video_path),
        '-vn',  # No video
        '-acodec', 'pcm_s16le' if settings["bit_depth"] == "16" else 'pcm_s24le',
        '-ar', settings["sample_rate"],
        '-ac', '1',  # Mono
        '-af', settings["filters"],
        '-y',  # Overwrite output file
        str(output_path)
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✓ Audio extracted successfully!")
        print(f"  Sample rate: {settings['sample_rate']} Hz")
        print(f"  Bit depth: {settings['bit_depth']} bit")
        print(f"  Channels: Mono")
        return str(output_path)
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Error extracting audio: {e}")
        if e.stderr:
            print(f"ffmpeg error: {e.stderr}")
        raise


def check_ffmpeg():
    """Check if ffmpeg is installed."""
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def main():
    parser = argparse.ArgumentParser(description="Extract high-quality audio from video files")
    parser.add_argument("video_path", help="Path to the video file")
    parser.add_argument("-o", "--output", help="Output audio file path (optional)")
    parser.add_argument("-q", "--quality", default="high", 
                       choices=["high", "medium", "low"],
                       help="Audio quality (default: high)")
    parser.add_argument("--check-ffmpeg", action="store_true",
                       help="Check if ffmpeg is installed and exit")
    
    args = parser.parse_args()
    
    if args.check_ffmpeg:
        if check_ffmpeg():
            print("✓ ffmpeg is installed")
        else:
            print("✗ ffmpeg is not installed")
            print("  Install with: brew install ffmpeg (macOS) or sudo apt install ffmpeg (Ubuntu)")
        return
    
    if not check_ffmpeg():
        print("✗ ffmpeg is required but not installed")
        print("  Install with: brew install ffmpeg (macOS) or sudo apt install ffmpeg (Ubuntu)")
        sys.exit(1)
    
    try:
        audio_path = extract_audio(args.video_path, args.output, args.quality)
        print(f"\nAudio file ready: {audio_path}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 