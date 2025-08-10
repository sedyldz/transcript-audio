# Video Transcript Extractor

A powerful tool for extracting high-quality transcripts from any video file. This project uses OpenAI's Whisper model optimized for Turkish language transcription with advanced audio processing capabilities.

## Features

- 🎥 **Video to Audio Extraction**: High-quality audio extraction using ffmpeg with optimized settings
- 🎤 **Advanced Transcription**: Uses OpenAI's Whisper model with Turkish language optimization
- 📝 **Multiple Output Formats**: Support for TXT, JSON, SRT, and VTT formats
- 🔧 **Flexible Pipeline**: Can run full pipeline or individual steps
- 🎯 **Quality Options**: Configurable audio quality and transcription model sizes
- 🚀 **GPU Support**: Automatic CUDA detection for faster processing

## Prerequisites

### System Requirements

- Python 3.8 or higher
- ffmpeg (for audio extraction)
- CUDA-compatible GPU (optional, for faster processing)

### Install ffmpeg

**macOS:**

```bash
brew install ffmpeg
```

**Ubuntu/Debian:**

```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html) or install via Chocolatey:

```bash
choco install ffmpeg
```

## Installation

1. **Clone the repository:**

```bash
git clone <repository-url>
cd video-transcript
```

2. **Create a virtual environment:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

## Usage

### Quick Start (Recommended)

Use the main pipeline script for the easiest experience:

```bash
python video_to_transcript.py your_video.mp4
```

This will:

1. Extract high-quality audio from your video
2. Transcribe the audio using the large-v3 Whisper model
3. Save the transcript as a text file

### Advanced Usage

#### Full Pipeline with Custom Options

```bash
python video_to_transcript.py your_video.mp4 \
    --quality high \
    --model large-v3 \
    --format txt
```

#### Audio Extraction Only

```bash
python video_to_transcript.py your_video.mp4 --audio-only
```

#### Transcribe Existing Audio File

```bash
python video_to_transcript.py --transcribe-only your_audio.wav
```

### Individual Scripts

#### Audio Extraction

```bash
python extract_audio.py your_video.mp4 -q high
```

Options:

- `-q, --quality`: Audio quality (`high`, `medium`, `low`)
- `-o, --output`: Custom output path
- `--check-ffmpeg`: Verify ffmpeg installation

#### Audio Transcription

```bash
python transcribe_audio.py your_audio.wav -m large-v3 -f txt
```

Options:

- `-m, --model`: Whisper model size (`tiny`, `base`, `small`, `medium`, `large`, `large-v2`, `large-v3`)
- `-l, --language`: Language code (default: `tr` for Turkish)
- `-f, --format`: Output format (`txt`, `json`, `srt`, `vtt`)
- `-o, --output`: Custom output path
- `--check-whisper`: Verify whisper installation

## Configuration Options

### Audio Quality Settings

- **High**: 48kHz, 24-bit, advanced filters (best for transcription)
- **Medium**: 44.1kHz, 16-bit, basic filters (balanced)
- **Low**: 16kHz, 16-bit, minimal filters (fastest)

### Whisper Model Sizes

| Model    | Size    | Speed   | Accuracy  | Use Case          |
| -------- | ------- | ------- | --------- | ----------------- |
| tiny     | 39 MB   | Fastest | Basic     | Quick tests       |
| base     | 74 MB   | Fast    | Good      | General use       |
| small    | 244 MB  | Medium  | Better    | Balanced          |
| medium   | 769 MB  | Slower  | High      | High accuracy     |
| large    | 1550 MB | Slow    | Highest   | Best results      |
| large-v2 | 1550 MB | Slow    | Very High | Enhanced accuracy |
| large-v3 | 1550 MB | Slow    | Best      | Latest model      |

### Output Formats

- **TXT**: Simple text format (default)
- **JSON**: Detailed format with timestamps and metadata
- **SRT**: SubRip subtitle format
- **VTT**: WebVTT subtitle format

## Examples

### Basic Video Transcription

```bash
# Extract and transcribe any video file
python video_to_transcript.py your_video.mp4
```

### High-Quality Processing

```bash
# Use highest quality settings
python video_to_transcript.py video.mp4 \
    --quality high \
    --model large-v3 \
    --format json
```

### Batch Processing

```bash
# Process multiple videos
for video in *.mp4; do
    python video_to_transcript.py "$video"
done
```

### Create Subtitles

```bash
# Generate SRT subtitles
python video_to_transcript.py video.mp4 --format srt
```

## Output Files

The pipeline creates the following files:

1. **Audio file**: `{video_name}_audio.wav`
2. **Transcript file**: `{video_name}_audio_transcript.{format}`

Example:
