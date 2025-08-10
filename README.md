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
