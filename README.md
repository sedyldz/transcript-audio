# Video Sesini Metne Dönüştürücü

Video dosyalarınızdan yüksek kaliteli altyazılar oluşturmak için geliştirilmiş basit ve etkili bir araç. OpenAI'nin Whisper modelini kullanarak Türkçe dilinde optimize edilmiş transkripsiyon yapar.

## 🎯 Ne İşe Yarar?

Bu araç ile şunları yapabilirsiniz:

- **Video altyazıları oluşturma**: YouTube videoları, eğitim içerikleri, toplantı kayıtları
- **Ses dosyası transkripsiyonu**: Podcast'ler, röportajlar, sesli notlar
- **Farklı formatlarda çıktı**: TXT, JSON, SRT, VTT formatlarında altyazı
- **Modüler kullanım**: İhtiyacınıza göre sadece ses çıkarma veya sadece transkripsiyon

## 🚀 Başlangıç

### 1. Gereksinimler

**macOS için:**

```bash
brew install ffmpeg
```

**Ubuntu/Debian için:**

```bash
sudo apt update && sudo apt install ffmpeg
```

**Windows için:**
[ffmpeg.org](https://ffmpeg.org/download.html) adresinden indirin

### 2. Kurulum

```bash
# Sanal ortam oluştur
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Gereksinimleri yükle
pip install -r requirements.txt
```

## 📖 Nasıl Kullanılır?

### Basit Kullanım (Önerilen)

**Video dosyanızdan altyazı oluşturmak için:**

```bash
python video_to_transcript.py videonuz.mp4
```

Bu komut:

1. Videodan ses çıkarır
2. Sesi metne çevirir
3. Altyazı dosyasını oluşturur

### Farklı Formatlarda Altyazı

**SRT formatında (YouTube için):**

```bash
python video_to_transcript.py videonuz.mp4 --format srt
```

**VTT formatında (web için):**

```bash
python video_to_transcript.py videonuz.mp4 --format vtt
```

### Sadece Ses Dosyası Varsa

Eğer zaten ses dosyanız varsa, doğrudan transkripsiyon yapabilirsiniz:

```bash
python transcribe_audio.py sesiniz.wav
```

### Modüler Kullanım

**Sadece ses çıkarmak için:**

```bash
python extract_audio.py videonuz.mp4
```

**Sadece transkripsiyon için:**

```bash
python transcribe_audio.py sesiniz.wav --format srt
```

## 🎬 Kullanım Senaryoları

### 1. YouTube Video Altyazıları

```bash
python video_to_transcript.py youtube_video.mp4 --format srt
```

### 2. Eğitim İçerikleri

```bash
python video_to_transcript.py ders_kaydi.mp4 --quality high --model large-v3
```

### 3. Toplantı Kayıtları

```bash
python video_to_transcript.py toplanti.mp4 --format txt
```

### 4. Podcast Transkripsiyonu

```bash
python transcribe_audio.py podcast.wav --format json
```

### 5. Sesli Notlar

```bash
python transcribe_audio.py notlar.wav --model medium
```

## ⚙️ Kalite Seçenekleri

### Ses Kalitesi

- **high**: En iyi kalite (48kHz, 24-bit) - Önerilen
- **medium**: Orta kalite (44.1kHz, 16-bit) - Dengeli
- **low**: Düşük kalite (16kHz, 16-bit) - Hızlı

### Model Boyutları

- **tiny**: En hızlı, temel doğruluk
- **base**: Hızlı, iyi doğruluk
- **small**: Orta hız, daha iyi doğruluk
- **medium**: Yavaş, yüksek doğruluk
- **large-v3**: En yavaş, en iyi doğruluk (Önerilen)

## 📁 Çıktı Dosyaları

Program şu dosyaları oluşturur:

1. **Ses dosyası**: `video_adi_audio.wav`
2. **Altyazı dosyası**: `video_adi_audio_transcript.txt`

### Format Örnekleri

**TXT formatı:**

---

# Video to Text Converter

A simple and effective tool developed to create high-quality subtitles from your video files. It performs transcription optimized for Turkish language using OpenAI's Whisper model.

## 🎯 What Does It Do?

With this tool, you can:

- **Create video subtitles**: YouTube videos, educational content, meeting recordings
- **Audio file transcription**: Podcasts, interviews, voice notes
- **Output in different formats**: Subtitles in TXT, JSON, SRT, VTT formats
- **Modular usage**: Extract audio only or transcription only according to your needs

## 🚀 Getting Started

### 1. Requirements

**For macOS:**

```bash
brew install ffmpeg
```

**For Ubuntu/Debian:**

```bash
sudo apt update && sudo apt install ffmpeg
```

**For Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html)

### 2. Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

## 📖 How to Use?

### Simple Usage (Recommended)

**To create subtitles from your video file:**

```bash
python video_to_transcript.py yourvideo.mp4
```

This command:

1. Extracts audio from video
2. Converts audio to text
3. Creates subtitle file

### Subtitles in Different Formats

**In SRT format (for YouTube):**

```bash
python video_to_transcript.py yourvideo.mp4 --format srt
```

**In VTT format (for web):**

```bash
python video_to_transcript.py yourvideo.mp4 --format vtt
```

### If You Only Have Audio File

If you already have an audio file, you can transcribe directly:

```bash
python transcribe_audio.py youraudio.wav
```

### Modular Usage

**To extract audio only:**

```bash
python extract_audio.py yourvideo.mp4
```

**For transcription only:**

```bash
python transcribe_audio.py youraudio.wav --format srt
```

## 🎬 Usage Scenarios

### 1. YouTube Video Subtitles

```bash
python video_to_transcript.py youtube_video.mp4 --format srt
```

### 2. Educational Content

```bash
python video_to_transcript.py lesson_recording.mp4 --quality high --model large-v3
```

### 3. Meeting Recordings

```bash
python video_to_transcript.py meeting.mp4 --format txt
```

### 4. Podcast Transcription

```bash
python transcribe_audio.py podcast.wav --format json
```

### 5. Voice Notes

```bash
python transcribe_audio.py notes.wav --model medium
```

## ⚙️ Quality Options

### Audio Quality

- **high**: Best quality (48kHz, 24-bit) - Recommended
- **medium**: Medium quality (44.1kHz, 16-bit) - Balanced
- **low**: Low quality (16kHz, 16-bit) - Fast

### Model Sizes

- **tiny**: Fastest, basic accuracy
- **base**: Fast, good accuracy
- **small**: Medium speed, better accuracy
- **medium**: Slow, high accuracy
- **large-v3**: Slowest, best accuracy (Recommended)

## 📁 Output Files

The program creates the following files:

1. **Audio file**: `video_name_audio.wav`
2. **Subtitle file**: `video_name_audio_transcript.txt`

### Format Examples

**TXT format:**

```
00:00:00,000 --> 00:00:03,000
Hello, this is a test video.

00:00:03,000 --> 00:00:06,000
We are testing our video transcription tool.
```

**SRT format:**

```
1
00:00:00,000 --> 00:00:03,000
Hello, this is a test video.

2
00:00:03,000 --> 00:00:06,000
We are testing our video transcription tool.
```

**VTT format:**

```
WEBVTT

00:00:00.000 --> 00:00:03.000
Hello, this is a test video.

00:00:03.000 --> 00:00:06.000
We are testing our video transcription tool.
```

## Advanced Options

### Command Line Arguments

```bash
python video_to_transcript.py video.mp4 [OPTIONS]

Options:
  --format FORMAT     Output format (txt, srt, vtt, json) [default: txt]
  --quality QUALITY   Audio quality (low, medium, high) [default: medium]
  --model MODEL       Whisper model size [default: base]
  --language LANG     Language code (tr, en, etc.) [default: tr]
  --output OUTPUT     Output filename
```

### Examples

```bash
# High quality transcription with large model
python video_to_transcript.py video.mp4 --quality high --model large-v3

# English transcription
python video_to_transcript.py video.mp4 --language en

# Custom output filename
python video_to_transcript.py video.mp4 --output my_transcript.txt
```

## Contributing

Feel free to contribute to this project by:

1. Forking the repository
2. Creating a feature branch
3. Making your changes
4. Submitting a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the existing issues
2. Create a new issue with detailed information
3. Include your operating system and Python version

---

_This tool is optimized for Turkish language but supports multiple languages through OpenAI's Whisper model._
