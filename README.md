# YouTube Audio Extractor

## Overview

This script downloads a YouTube video, extracts its audio, converts it to MP3, and separates it into stems using Demucs. It is useful for audio analysis, remixing, or instrumental extraction.

## Features

- Downloads YouTube videos as audio files using `yt-dlp`
- Converts the extracted audio to MP3 format
- Separates the audio into stems (vocals, bass, drums, etc.) using `Demucs`
- Logs the entire process for debugging and tracking

## Requirements

Make sure you have the following dependencies installed:

```
pip install -r requirements.txt
```

Additionally, `ffmpeg` may be required for `moviepy` to function properly. Install it via:

- **Linux/macOS**: `sudo apt install ffmpeg` or `brew install ffmpeg`
- **Windows**: Download from [FFmpeg.org](https://ffmpeg.org/download.html) and add it to your system path.

## Installation

1. Clone the repository or download the script.
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Ensure `demucs` is installed:
   ```sh
   pip install demucs
   ```

## Usage

Run the script by providing a YouTube video URL:

```sh
python main.py
```

Enter the YouTube URL when prompted, and the script will:

1. Download the video
2. Extract and convert the audio to MP3
3. Separate the audio into stems

## Output

- The MP3 file will be saved as `audio.mp3`.
- Separated stems will be stored in `stems_/video_id/`.

## Logging

All operations are logged in `process.log`. You can check this file for debugging or monitoring the process.

## License

This project is open-source and available under the MIT License.

## Author

Yani Stratev

