# Content Packaging and Publishing System Documentation

This document outlines the tools developed for packaging audio content with visuals into video files and generating associated metadata for the Lo-fi and baby sounds YouTube channel.

## 1. Image Generation (`image_generator.py`)

### 1.1. Overview

The `image_generator.py` script (or rather, the direct calls to the `media_generate_image` tool) is responsible for creating static background images for the video content. These images are designed to complement the audio, providing a visually appealing and thematic backdrop for Lo-fi music, baby sounds, and white noise videos.

### 1.2. Functionality:

This component leverages the `media_generate_image` tool to create images based on textual prompts. The images are generated with a `landscape` aspect ratio, suitable for YouTube video formats.

*   **Lo-fi Video Background:** Prompts are crafted to generate images reflecting a cozy, calm, and atmospheric setting, often featuring elements like rain, warm lighting, and study environments.
*   **Baby Sound Video Background:** Prompts focus on peaceful nursery scenes, sleeping babies, and soft, dreamy aesthetics.
*   **White Noise Video Background:** Prompts aim for abstract, minimalist patterns of soft colors that are calming and non-distracting.

### 1.3. Usage:

Image generation is performed by direct calls to the `media_generate_image` tool with specific prompts and output paths. For example:

```python
# Example call for Lo-fi video background
default_api.media_generate_image(
    brief="Generating image for Lo-fi video background.",
    images=[{"aspect_ratio": "landscape", "path": "/home/ubuntu/lofi_video_background.png", "prompt": "A cozy, dimly lit room with a window showing gentle rain, a warm cup of tea on a desk, and a subtle glow from a laptop. Lo-fi aesthetic, calm colors."}]
)
```

## 2. Video Creation (`video_creator.py`)

### 2.1. Overview

The `video_creator.py` script combines a static background image with an audio track to produce a video file. This is the core component for transforming the generated audio loops and images into publishable YouTube content.

### 2.2. Function:

*   `create_video_from_audio_image(audio_path, image_path, output_video_path, duration_s)`:
    *   Takes an audio file and a static image, and generates an MP4 video file.
    *   `audio_path`: Path to the input audio file (e.g., a looped Lo-fi track or white noise).
    *   `image_path`: Path to the static image to be used as the video background.
    *   `output_video_path`: Path where the final video file will be saved.
    *   `duration_s`: The desired duration of the output video in seconds. The video will be created to match the audio duration.

### 2.3. Usage:

```python
from video_creator import create_video_from_audio_image

# Example: Create a Lo-fi video
create_video_from_audio_image(
    "path/to/looped_lofi_audio.wav",
    "/home/ubuntu/lofi_video_background.png",
    "lofi_video_final.mp4",
    3600 # 1 hour duration
)

# Example: Create a baby sound video
create_video_from_audio_image(
    "path/to/looped_white_noise.wav",
    "/home/ubuntu/baby_sound_video_background.png",
    "baby_white_noise_video.mp4",
    7200 # 2 hour duration
)
```

### 2.4. Dependencies:

*   `ffmpeg` (must be installed on the system)
*   `pydub` (used for dummy audio generation in `if __name__ == "__main__"` block)
*   `PIL` (Pillow library, used for dummy image generation in `if __name__ == "__main__"` block)

## 3. Metadata Generation (`metadata_generator.py`)

### 3.1. Overview

The `metadata_generator.py` script provides functions to automatically generate relevant titles, descriptions, and tags for YouTube videos. This streamlines the publishing process and helps optimize content for search and discoverability.

### 3.2. Functions:

*   `generate_lofi_metadata(title_prefix, duration_minutes, keywords=None)`:
    *   Generates metadata tailored for Lo-fi music videos.
    *   `title_prefix`: The main descriptive part of the video title (e.g., "Cozy Rain Lo-fi").
    *   `duration_minutes`: The total duration of the video in minutes.
    *   `keywords`: An optional list of additional keywords to include in the tags.

*   `generate_baby_sound_metadata(sound_type, duration_minutes, keywords=None)`:
    *   Generates metadata specifically for baby sound or white noise videos.
    *   `sound_type`: The type of sound featured (e.g., "White Noise", "Rain Sound", "Lullaby").
    *   `duration_minutes`: The total duration of the video in minutes.
    *   `keywords`: An optional list of additional keywords to include in the tags.

### 3.3. Usage:

```python
from metadata_generator import generate_lofi_metadata, generate_baby_sound_metadata

# Example: Generate Lo-fi video metadata
lofi_meta = generate_lofi_metadata("Rainy Day Chill", 180, ["rain", "cozy", "fireplace"])
print(lofi_meta["title"])
print(lofi_meta["description"])
print(lofi_meta["tags"])

# Example: Generate Baby Sound video metadata
baby_meta = generate_baby_sound_metadata("Pink Noise", 360, ["infant sleep", "pink noise machine"])
print(baby_meta["title"])
print(baby_meta["description"])
print(baby_meta["tags"])
```

### 3.4. Output:

Both functions return a dictionary containing `title`, `description`, and `tags` (as a comma-separated string), ready for use when uploading videos to YouTube.

