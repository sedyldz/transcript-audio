#!/usr/bin/env python3
"""
Video to Transcript Pipeline
Combines audio extraction and transcription in two separate steps.
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path


def run_audio_extraction(video_path: str, quality: str = "high") -> str:
    """Run audio extraction step."""
    print("=" * 50)
    print("STEP 1: EXTRACTING AUDIO")
    print("=" * 50)
    
    cmd = [sys.executable, "extract_audio.py", video_path, "-q", quality]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Audio extraction failed: {result.stderr}")
        raise RuntimeError("Audio extraction failed")
    
    print(result.stdout)
    
    # Extract the audio file path from output
    video_path = Path(video_path)
    audio_path = video_path.parent / f"{video_path.stem}_audio.wav"
    
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not created: {audio_path}")
    
    return str(audio_path)


def run_transcription(audio_path: str, model: str = "large-v3", format_output: str = "txt") -> str:
    """Run transcription step."""
    print("=" * 50)
    print("STEP 2: TRANSCRIBING AUDIO")
    print("=" * 50)
    
    cmd = [
        sys.executable, "transcribe_audio.py", 
        audio_path, 
        "-m", model,
        "-f", format_output
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Transcription failed: {result.stderr}")
        raise RuntimeError("Transcription failed")
    
    print(result.stdout)
    
    # Extract the transcript file path from output
    audio_path = Path(audio_path)
    transcript_path = audio_path.parent / f"{audio_path.stem}_transcript.{format_output}"
    
    if not transcript_path.exists():
        raise FileNotFoundError(f"Transcript file not created: {transcript_path}")
    
    return str(transcript_path)


def main():
    parser = argparse.ArgumentParser(description="Convert video to transcript in two steps")
    parser.add_argument("video_path", help="Path to the video file")
    parser.add_argument("-q", "--quality", default="high",
                       choices=["high", "medium", "low"],
                       help="Audio quality (default: high)")
    parser.add_argument("-m", "--model", default="large-v3",
                       choices=["tiny", "base", "small", "medium", "large", "large-v2", "large-v3"],
                       help="Whisper model size (default: large-v3)")
    parser.add_argument("-f", "--format", default="txt",
                       choices=["txt", "json", "srt", "vtt"],
                       help="Output format (default: txt)")
    parser.add_argument("--audio-only", action="store_true",
                       help="Only extract audio, don't transcribe")
    parser.add_argument("--transcribe-only", help="Transcribe existing audio file (skip extraction)")
    
    args = parser.parse_args()
    
    try:
        if args.transcribe_only:
            # Only transcribe existing audio file
            audio_path = args.transcribe_only
            transcript_path = run_transcription(audio_path, args.model, args.format)
            print(f"\n✓ Transcription completed: {transcript_path}")
            
        else:
            # Full pipeline: extract audio then transcribe
            video_path = Path(args.video_path)
            if not video_path.exists():
                raise FileNotFoundError(f"Video file not found: {video_path}")
            
            # Step 1: Extract audio
            audio_path = run_audio_extraction(args.video_path, args.quality)
            
            if args.audio_only:
                print(f"\n✓ Audio extraction completed: {audio_path}")
                print("Use --transcribe-only to transcribe this audio file later")
                return
            
            # Step 2: Transcribe audio
            transcript_path = run_transcription(audio_path, args.model, args.format)
            
            print("\n" + "=" * 50)
            print("PIPELINE COMPLETED SUCCESSFULLY")
            print("=" * 50)
            print(f"Video: {args.video_path}")
            print(f"Audio: {audio_path}")
            print(f"Transcript: {transcript_path}")
            print(f"Model: {args.model}")
            print(f"Format: {args.format}")
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 