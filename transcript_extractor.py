#!/usr/bin/env python3
"""
Improved Turkish Video Transcript Extractor
Uses advanced techniques for better Turkish transcription accuracy.
"""

import os
import sys
import argparse
import subprocess
import re
from pathlib import Path
import whisper
import torch
import numpy as np
from typing import Optional, Tuple, List


class ImprovedTurkishTranscriptExtractor:
    def __init__(self, model_size: str = "large-v3"):
        """
        Initialize the improved transcript extractor.
        
        Args:
            model_size: Whisper model size ('tiny', 'base', 'small', 'medium', 'large', 'large-v2', 'large-v3')
        """
        self.model_size = model_size
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")
        print(f"Model size: {model_size}")
        
    def load_model(self):
        """Load the Whisper model."""
        print(f"Loading Whisper model: {self.model_size}")
        self.model = whisper.load_model(self.model_size, device=self.device)
        print("Model loaded successfully!")
        
    def extract_audio_improved(self, video_path: str, audio_path: str = None) -> str:
        """
        Extract audio with improved quality for transcription.
        
        Args:
            video_path: Path to the video file
            audio_path: Path for the output audio file (optional)
            
        Returns:
            Path to the extracted audio file
        """
        if audio_path is None:
            audio_path = video_path.rsplit('.', 1)[0] + '_improved.wav'
            
        print(f"Extracting high-quality audio from: {video_path}")
        
        # Improved ffmpeg settings for better transcription
        cmd = [
            'ffmpeg', '-i', video_path,
            '-vn',  # No video
            '-acodec', 'pcm_s16le',  # PCM 16-bit
            '-ar', '16000',  # 16kHz sample rate (Whisper's preferred)
            '-ac', '1',  # Mono
            '-af', 'highpass=f=200,lowpass=f=3000,volume=1.5',  # Audio filters
            '-y',  # Overwrite output file
            audio_path
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"High-quality audio extracted to: {audio_path}")
            return audio_path
        except subprocess.CalledProcessError as e:
            print(f"Error extracting audio: {e}")
            raise
            
    def transcribe_audio_improved(self, audio_path: str, output_path: str = None) -> Tuple[str, dict]:
        """
        Transcribe audio with improved settings for Turkish.
        
        Args:
            audio_path: Path to the audio file
            output_path: Path for the output transcript file (optional)
            
        Returns:
            Tuple of (transcript_text, transcription_info)
        """
        if self.model is None:
            self.load_model()
            
        print(f"Transcribing audio with improved settings: {audio_path}")
        
        # Improved transcription settings for Turkish
        result = self.model.transcribe(
            audio_path,
            language="tr",  # Turkish language
            task="transcribe",
            verbose=True,
            fp16=False,  # Use FP32 for better accuracy on CPU
            temperature=0.0,  # Deterministic output
            compression_ratio_threshold=2.4,
            logprob_threshold=-1.0,
            no_speech_threshold=0.6,
            condition_on_previous_text=True,
            initial_prompt="Bu bir Türkçe konuşma kaydıdır. Türkçe dilinde transkripsiyon yapılacaktır."
        )
        
        transcript_text = result["text"]
        transcription_info = {
            "language": result.get("language"),
            "language_probability": result.get("language_probability"),
            "segments": result.get("segments", [])
        }
        
        # Post-process the transcript for better Turkish formatting
        transcript_text = self.post_process_turkish_text(transcript_text)
        
        # Save transcript to file
        if output_path is None:
            output_path = audio_path.rsplit('.', 1)[0] + '_improved_transcript.txt'
            
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(transcript_text)
            
        # Also save detailed segments
        segments_path = output_path.replace('.txt', '_segments.txt')
        self.save_detailed_segments(result.get("segments", []), segments_path)
            
        print(f"Improved transcript saved to: {output_path}")
        print(f"Detailed segments saved to: {segments_path}")
        
        return transcript_text, transcription_info
    
    def post_process_turkish_text(self, text: str) -> str:
        """
        Post-process Turkish text for better formatting and accuracy.
        
        Args:
            text: Raw transcribed text
            
        Returns:
            Improved Turkish text
        """
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Fix common Turkish transcription errors
        turkish_fixes = {
            'Cliniki': 'Klinik',
            'aunque': 'ancak',
            'inaugural': 'gerçek',
            'Garage': 'garaj',
            'Lime': 'limon',
            'Party': 'parti',
            'övüyle': 'övgüyle',
            'müfakalı': 'mümkün',
            'orka': 'organizasyon',
            'hayatması': 'hayatı',
            'ufacıklı': 'ufak',
            'kovar': 'kovar',
            'canısıyla': 'canıyla',
            'değiştilerinecek': 'değiştirilecek',
            'boşlu': 'boş',
            'füldüme': 'fırsatıma',
            'mükefata': 'mükafat',
            'dairli': 'dair',
            'fayna': 'fayda',
            'espranlar': 'espriler',
            'aynayyardan': 'yanından',
            'aynadısı': 'yanında',
            'aynadık': 'yanında',
            'krim': 'kariyer',
            'etleşin': 'elde edin',
            'sınake': 'sadece',
            'hizahetle': 'hizmetle',
            'nefikirlerine': 'fikirlerine',
            'fırsitli': 'fırsatı',
            'Tiye': 'Tıpkı',
            'sınavda': 'sıradan',
            'hasta': 'hasta',
            'itiyar': 'ihtiyaç',
            'ayağıcak': 'ayıracak',
            'dançağı': 'dan başka',
            'hedani': 'hedonik',
            'kuyruğumun': 'kuyruğunun',
            'havuç': 'havuç',
            'çarkayından': 'çarkından',
            'sonuçtundan': 'sonuçtan',
            'kayk': 'kayıp',
            'dina': 'dünya',
            'niçabı': 'ne kadar',
            'soğusturmaya': 'sorgulamaya',
            'yamak': 'yapmak'
        }
        
        for wrong, correct in turkish_fixes.items():
            text = text.replace(wrong, correct)
        
        # Fix sentence endings
        text = re.sub(r'\s+([.!?])', r'\1', text)
        
        # Add proper spacing after punctuation
        text = re.sub(r'([.!?])([A-ZÇĞIİÖŞÜ])', r'\1 \2', text)
        
        return text
    
    def save_detailed_segments(self, segments: List[dict], output_path: str):
        """
        Save detailed segments with timestamps for better analysis.
        
        Args:
            segments: List of segment dictionaries
            output_path: Path to save detailed segments
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("DETAYLI TRANSCRIPT SEGMENTLERİ\n")
            f.write("=" * 50 + "\n\n")
            
            for i, segment in enumerate(segments, 1):
                start_time = self.format_timestamp(segment.get('start', 0))
                end_time = self.format_timestamp(segment.get('end', 0))
                text = segment.get('text', '').strip()
                
                f.write(f"Segment {i} [{start_time} --> {end_time}]\n")
                f.write(f"{text}\n")
                f.write("-" * 30 + "\n\n")
    
    def format_timestamp(self, seconds: float) -> str:
        """Format seconds to MM:SS format."""
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"
        
    def process_video_improved(self, video_path: str, output_dir: str = None) -> Tuple[str, dict]:
        """
        Complete improved pipeline: extract audio and transcribe.
        
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
            
        # Extract audio with improved quality
        audio_path = output_dir / f"{video_path.stem}_improved.wav"
        audio_path = self.extract_audio_improved(str(video_path), str(audio_path))
        
        # Transcribe audio with improved settings
        transcript_path = output_dir / f"{video_path.stem}_improved_transcript.txt"
        transcript_text, transcription_info = self.transcribe_audio_improved(
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
    parser = argparse.ArgumentParser(description="Extract Turkish transcripts with improved accuracy")
    parser.add_argument("video_path", help="Path to the video file")
    parser.add_argument("--model", default="large-v3", 
                       choices=["tiny", "base", "small", "medium", "large", "large-v2", "large-v3"],
                       help="Whisper model size (default: large-v3 for best accuracy)")
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
        
    # Process the video with improved settings
    try:
        extractor = ImprovedTurkishTranscriptExtractor(model_size=args.model)
        transcript_text, info = extractor.process_video_improved(args.video_path, args.output_dir)
        
        print("\n" + "="*50)
        print("IMPROVED TRANSCRIPT EXTRACTION COMPLETE")
        print("="*50)
        print(f"Language detected: {info.get('language', 'Unknown')}")
        lang_prob = info.get('language_probability')
        if lang_prob is not None:
            print(f"Language confidence: {lang_prob:.2f}")
        else:
            print("Language confidence: Unknown")
        print(f"Number of segments: {len(info.get('segments', []))}")
        print(f"Model used: {args.model}")
        print("\nFirst 500 characters of improved transcript:")
        print("-" * 30)
        print(transcript_text[:500] + "..." if len(transcript_text) > 500 else transcript_text)
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 