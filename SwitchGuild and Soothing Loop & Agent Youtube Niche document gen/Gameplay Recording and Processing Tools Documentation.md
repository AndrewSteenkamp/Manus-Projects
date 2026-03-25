# Gameplay Recording and Processing Tools Documentation

This document outlines the tools and setup instructions for capturing and processing gameplay footage for the SwitchGuild channel.

## 1. Retroid Pocket 5 Gameplay Transfer Simulation

### 1.1. Overview

This tool simulates the automated transfer of recorded gameplay footage from a Retroid Pocket 5 device to a designated processing directory. In a real-world scenario, this would involve setting up an automated sync solution on the Android-based Retroid Pocket 5 (e.g., cloud sync, FTP server, or ADB scripting).

### 1.2. `simulate_retroid_transfer.py`

**Purpose:** Moves a specified dummy video file, representing a recorded gameplay session, from the current directory to a `processed_retroid_videos` directory.

**Usage:**

```bash
python3 simulate_retroid_transfer.py
```

**Example Output:**

```
Successfully moved 'retroid_gameplay_20250910_001.mp4' to 'processed_retroid_videos'.
```

**Note:** For actual Retroid Pocket 5 integration, consider using Android Debug Bridge (ADB) for scripting file transfers, or cloud synchronization apps available on the Android Play Store to automatically upload recorded videos to a cloud storage service, which can then be accessed by your processing environment.

## 2. Nintendo Switch Gameplay Recording Setup

### 2.1. Overview

Recording high-quality, long-form gameplay from the Nintendo Switch (and future Switch 2) requires an external capture card and recording software. OBS Studio is recommended for its flexibility and open-source nature.

### 2.2. Setup Instructions

Detailed instructions for connecting your Nintendo Switch to a capture card and configuring OBS Studio for recording can be found in the `switch_recording_setup.md` document.

## 3. Basic Video Processing with FFmpeg

### 3.1. Overview

FFmpeg is a powerful open-source command-line tool for handling multimedia data. The `video_processor.py` script demonstrates basic video merging functionality using FFmpeg, which can be extended for other tasks like trimming, format conversion, or basic enhancements.

### 3.2. Installation (FFmpeg)

FFmpeg can be installed on Ubuntu-based systems using the following commands:

```bash
sudo apt-get update
sudo apt-get install -y ffmpeg
```

### 3.3. `video_processor.py`

**Purpose:** Merges multiple video files into a single output file using FFmpeg's concat demuxer.

**Function:** `merge_videos(input_files, output_file)`

*   `input_files`: A list of paths to the video files to be merged.
*   `output_file`: The desired path for the merged output video.

**Usage (within a Python script):**

```python
from video_processor import merge_videos

input_videos = ["path/to/video1.mp4", "path/to/video2.mp4"]
output_merged_video = "path/to/merged_gameplay.mp4"
merge_videos(input_videos, output_merged_video)
```

**Example (for testing):**

The `if __name__ == "__main__":` block in `video_processor.py` includes a self-contained example that creates two dummy video files and then merges them. You can run it directly to test the merging functionality:

```bash
python3 video_processor.py
```

**Note:** This script uses FFmpeg's `concat` demuxer, which is efficient for merging videos with identical codecs and parameters without re-encoding. For more complex operations (e.g., trimming specific segments, adding overlays), FFmpeg commands would need to be tailored accordingly within the script.

