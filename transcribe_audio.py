#!/usr/bin/env python3
"""
Audio Transcriber using Whisper
Transcribes audio files using OpenAI's Whisper model with optimal settings for Turkish.
"""

import os
import sys
import argparse
import json
from pathlib import Path
import whisper
import torch


def transcribe_audio(audio_path: str, output_path: str = None, model_size: str = "large-v3", 
                    language: str = "tr", format_output: str = "txt") -> dict:
    """
    Transcribe audio file using Whisper with optimal settings.
    
    Args:
        audio_path: Path to the audio file
        output_path: Path for the output transcript file (optional)
        model_size: Whisper model size
        language: Language code (default: "tr" for Turkish)
        format_output: Output format ("txt", "json", "srt", "vtt")
        
    Returns:
        Dictionary containing transcription results
    """
    audio_path = Path(audio_path)
    
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    # Determine output path
    if output_path is None:
        output_path = audio_path.parent / f"{audio_path.stem}_transcript.{format_output}"
    else:
        output_path = Path(output_path)
    
    print(f"Loading Whisper model: {model_size}")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    
    # Load model
    model = whisper.load_model(model_size, device=device)
    print("Model loaded successfully!")
    
    print(f"Transcribing: {audio_path}")
    
    # Optimal transcription settings for Turkish
    result = model.transcribe(
        str(audio_path),
        language=language,
        task="transcribe",
        verbose=True,
        fp16=False,  # Use FP32 for better accuracy on CPU
        temperature=0.0,  # Deterministic output
        compression_ratio_threshold=2.4,
        logprob_threshold=-1.0,
        no_speech_threshold=0.6,
        condition_on_previous_text=True
    )
    
    # Save output in requested format
    save_transcript(result, output_path, format_output)
    
    return result


def save_transcript(result: dict, output_path: Path, format_output: str):
    """Save transcript in the specified format."""
    
    if format_output == "txt":
        # Simple text format
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result["text"])
    
    elif format_output == "json":
        # Detailed JSON format with all metadata
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
    
    elif format_output == "srt":
        # SubRip subtitle format
        with open(output_path, 'w', encoding='utf-8') as f:
            for i, segment in enumerate(result["segments"], 1):
                start_time = format_timestamp(segment["start"])
                end_time = format_timestamp(segment["end"])
                text = segment["text"].strip()
                
                f.write(f"{i}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{text}\n\n")
    
    elif format_output == "vtt":
        # WebVTT subtitle format
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("WEBVTT\n\n")
            for i, segment in enumerate(result["segments"], 1):
                start_time = format_timestamp(segment["start"], vtt=True)
                end_time = format_timestamp(segment["end"], vtt=True)
                text = segment["text"].strip()
                
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{text}\n\n")
    
    print(f"✓ Transcript saved: {output_path}")


def format_timestamp(seconds: float, vtt: bool = False) -> str:
    """Format seconds to timestamp string."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    
    if vtt:
        # WebVTT format: HH:MM:SS.mmm
        return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"
    else:
        # SRT format: HH:MM:SS,mmm
        return f"{hours:02d}:{minutes:02d}:{secs:06.3f}".replace('.', ',')


def check_whisper():
    """Check if whisper is installed."""
    try:
        import whisper
        return True
    except ImportError:
        return False


def main():
    parser = argparse.ArgumentParser(description="Transcribe audio files using Whisper")
    parser.add_argument("audio_path", help="Path to the audio file")
    parser.add_argument("-o", "--output", help="Output transcript file path (optional)")
    parser.add_argument("-m", "--model", default="large-v3",
                       choices=["tiny", "base", "small", "medium", "large", "large-v2", "large-v3"],
                       help="Whisper model size (default: large-v3)")
    parser.add_argument("-l", "--language", default="tr",
                       help="Language code (default: tr for Turkish)")
    parser.add_argument("-f", "--format", default="txt",
                       choices=["txt", "json", "srt", "vtt"],
                       help="Output format (default: txt)")
    parser.add_argument("--check-whisper", action="store_true",
                       help="Check if whisper is installed and exit")
    
    args = parser.parse_args()
    
    if args.check_whisper:
        if check_whisper():
            print("✓ whisper is installed")
        else:
            print("✗ whisper is not installed")
            print("  Install with: pip install openai-whisper")
        return
    
    if not check_whisper():
        print("✗ whisper is required but not installed")
        print("  Install with: pip install openai-whisper")
        sys.exit(1)
    
    try:
        result = transcribe_audio(
            args.audio_path, 
            args.output, 
            args.model, 
            args.language, 
            args.format
        )
        
        print(f"\nTranscription completed!")
        print(f"Language detected: {result.get('language', 'Unknown')}")
        lang_prob = result.get('language_probability')
        if lang_prob is not None:
            print(f"Language confidence: {lang_prob:.2f}")
        print(f"Duration: {result.get('segments', [{}])[-1].get('end', 0):.1f} seconds")
        print(f"Segments: {len(result.get('segments', []))}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 