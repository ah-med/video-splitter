# Video Splitter

A web-based tool that allows you to split videos into multiple parts based on custom timestamps.

## Features

- Upload video files (supports MP4, AVI, MOV, and MKV formats)
- Preview uploaded videos
- Add split points at specific timestamps
- Download split video parts as a ZIP file
- Modern and intuitive user interface

## Requirements

- Python 3.7 or higher
- FFmpeg (required for video processing)

## Installation

1. Clone this repository:

```bash
git clone <repository-url>
cd video-splitter
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Install FFmpeg:

- On macOS: `brew install ffmpeg`
- On Ubuntu/Debian: `sudo apt-get install ffmpeg`
- On Windows: Download from [FFmpeg website](https://ffmpeg.org/download.html)

## Usage

1. Start the application:

```bash
python app.py
```

2. Open your web browser and navigate to `http://localhost:5000`

3. Upload a video file using the file input

4. Use the video player to navigate to desired split points and click "Add Split Point"

5. Click "Split Video" to process the video

6. Download the resulting ZIP file containing all split video parts

## Notes

- Maximum file size: 500MB
- Supported video formats: MP4, AVI, MOV, MKV
- The application creates temporary files during processing, which are automatically cleaned up
