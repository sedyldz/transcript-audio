#!/usr/bin/env python3
"""
Turkish Video Transcript Extractor
Extracts audio transcripts from Turkish videos using OpenAI's Whisper model.
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path
import whisper
import torch
from typing import Optional, Tuple


class TurkishTranscriptExtractor:
    def __init__(self, model_size: str = "base"):
        """
        Initialize the transcript extractor.
        
        Args:
            model_size: Whisper model size ('tiny', 'base', 'small', 'medium', 'large')
        """
        self.model_size = model_size
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")
        
    def load_model(self):
        """Load the Whisper model."""
        print(f"Loading Whisper model: {self.model_size}")
        self.model = whisper.load_model(self.model_size, device=self.device)
        print("Model loaded successfully!")
        
    def extract_audio(self, video_path: str, audio_path: str = None) -> str:
        """
        Extract audio from video file using ffmpeg.
        
        Args:
            video_path: Path to the video file
            audio_path: Path for the output audio file (optional)
            
        Returns:
            Path to the extracted audio file
        """
        if audio_path is None:
            audio_path = video_path.rsplit('.', 1)[0] + '.wav'
            
        print(f"Extracting audio from: {video_path}")
        
        # Use ffmpeg to extract audio
        cmd = [
            'ffmpeg', '-i', video_path,
            '-vn',  # No video
            '-acodec', 'pcm_s16le',  # PCM 16-bit
            '-ar', '16000',  # 16kHz sample rate
            '-ac', '1',  # Mono
            '-y',  # Overwrite output file
            audio_path
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"Audio extracted to: {audio_path}")
            return audio_path
        except subprocess.CalledProcessError as e:
            print(f"Error extracting audio: {e}")
            raise
            
    def transcribe_audio(self, audio_path: str, output_path: str = None) -> Tuple[str, dict]:
        """
        Transcribe audio using Whisper.
        
        Args:
            audio_path: Path to the audio file
            output_path: Path for the output transcript file (optional)
            
        Returns:
            Tuple of (transcript_text, transcription_info)
        """
        if self.model is None:
            self.load_model()
            
        print(f"Transcribing audio: {audio_path}")
        
        # Transcribe with Turkish language specification
        result = self.model.transcribe(
            audio_path,
            language="tr",  # Turkish language
            task="transcribe",
            verbose=True
        )
        
        transcript_text = result["text"]
        transcription_info = {
            "language": result.get("language"),
            "language_probability": result.get("language_probability"),
            "segments": result.get("segments", [])
        }
        
        # Save transcript to file
        if output_path is None:
            output_path = audio_path.rsplit('.', 1)[0] + '_transcript.txt'
            
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(transcript_text)
            
        print(f"Transcript saved to: {output_path}")
        
        return transcript_text, transcription_info
        
    def process_video(self, video_path: str, output_dir: str = None) -> Tuple[str, dict]:
        """
        Complete pipeline: extract audio and transcribe.
        
        Args:
            video_path: Path to the video file
            output_dir: Directory for output files (optional)
            
        Returns:
            Tuple of (transcript_text, transcription_info)
        """
        video_path = Path(video_path)
        
        if not video_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")
            
        if output_dir:
            output_dir = Path(output_dir)
            output_dir.mkdir(exist_ok=True)
        else:
            output_dir = video_path.parent
            
        # Extract audio
        audio_path = output_dir / f"{video_path.stem}.wav"
        audio_path = self.extract_audio(str(video_path), str(audio_path))
        
        # Transcribe audio
        transcript_path = output_dir / f"{video_path.stem}_transcript.txt"
        transcript_text, transcription_info = self.transcribe_audio(
            audio_path, str(transcript_path)
        )
        
        return transcript_text, transcription_info


def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        print("✓ ffmpeg is installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ ffmpeg is not installed. Please install ffmpeg first.")
        print("  macOS: brew install ffmpeg")
        print("  Ubuntu: sudo apt install ffmpeg")
        return False
        
    try:
        import whisper
        print("✓ whisper is installed")
    except ImportError:
        print("✗ whisper is not installed. Installing...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'openai-whisper'], check=True)
        print("✓ whisper installed successfully")
        
    return True


def main():
    parser = argparse.ArgumentParser(description="Extract Turkish transcripts from video files")
    parser.add_argument("video_path", help="Path to the video file")
    parser.add_argument("--model", default="base", 
                       choices=["tiny", "base", "small", "medium", "large"],
                       help="Whisper model size (default: base)")
    parser.add_argument("--output-dir", help="Output directory for transcript files")
    parser.add_argument("--check-deps", action="store_true", 
                       help="Check dependencies and exit")
    
    args = parser.parse_args()
    
    if args.check_deps:
        check_dependencies()
        return
        
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
        
    # Process the video
    try:
        extractor = TurkishTranscriptExtractor(model_size=args.model)
        transcript_text, info = extractor.process_video(args.video_path, args.output_dir)
        
        print("\n" + "="*50)
        print("TRANSCRIPT EXTRACTION COMPLETE")
        print("="*50)
        print(f"Language detected: {info.get('language', 'Unknown')}")
        lang_prob = info.get('language_probability')
        if lang_prob is not None:
            print(f"Language confidence: {lang_prob:.2f}")
        else:
            print("Language confidence: Unknown")
        print(f"Number of segments: {len(info.get('segments', []))}")
        print("\nFirst 500 characters of transcript:")
        print("-" * 30)
        print(transcript_text[:500] + "..." if len(transcript_text) > 500 else transcript_text)
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 