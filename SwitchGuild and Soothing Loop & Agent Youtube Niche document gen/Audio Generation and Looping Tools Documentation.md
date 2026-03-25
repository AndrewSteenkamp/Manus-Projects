# Audio Generation and Looping Tools Documentation

This document details the Python scripts developed for generating various types of colored noise, creating seamless audio loops, and combining multiple audio elements. These tools are fundamental for creating the diverse audio content required for the Lo-fi and baby sounds YouTube channel.

## 1. Noise Generator (`noise_generator.py`)

### 1.1. Overview

The `noise_generator.py` script provides functions to synthesize white, pink, and brown noise. These colored noises are essential for creating soothing background sounds, particularly for baby sleep content, as they can effectively mask other environmental sounds.

### 1.2. Functions:

*   `generate_white_noise(duration_ms, volume_db)`:
    *   Generates white noise, which has equal intensity across all frequencies, sounding like a steady hiss or static.
    *   `duration_ms`: Duration of the noise in milliseconds.
    *   `volume_db`: Volume adjustment in decibels (e.g., -10 for quieter).

*   `generate_pink_noise(duration_ms, volume_db)`:
    *   Generates pink noise, which has more energy at lower frequencies, sounding deeper and often compared to rainfall or a gentle waterfall.
    *   `duration_ms`: Duration of the noise in milliseconds.
    *   `volume_db`: Volume adjustment in decibels.

*   `generate_brown_noise(duration_ms, volume_db)`:
    *   Generates brown noise, which has even more energy at lower frequencies than pink noise, resulting in a deeper, rumbling sound like a strong waterfall.
    *   `duration_ms`: Duration of the noise in milliseconds.
    *   `volume_db`: Volume adjustment in decibels.

### 1.3. Usage:

To generate and save noise files, run the script directly:

```bash
python3 noise_generator.py
```

This will create `white_noise.wav`, `pink_noise.wav`, and `brown_noise.wav` files in the current directory, each 5 seconds long with a volume of -10 dB.

### 1.4. Dependencies:

*   `pydub`
*   `numpy`
*   `scipy`

## 2. Audio Looper (`audio_looper.py`)

### 2.1. Overview

The `audio_looper.py` script is designed to create seamlessly looped audio files from an input audio track. This is critical for generating continuous background music (Lo-fi) and uninterrupted soothing sounds (baby sounds, white noise) for extended YouTube videos.

### 2.2. Function:

*   `create_seamless_loop(input_file, output_file, loop_duration_ms)`:
    *   Takes an input audio file and creates a new audio file that loops seamlessly for a specified duration.
    *   `input_file`: Path to the source audio file.
    *   `output_file`: Path to save the looped audio file.
    *   `loop_duration_ms`: Desired total duration of the looped audio in milliseconds.

### 2.3. Usage:

To test the looping functionality, run the script directly:

```bash
python3 audio_looper.py
```

This will create `looped_audio_15s.wav` (15-second loop) and `looped_audio_3s.wav` (3-second loop) from a dummy audio file.

### 2.4. Dependencies:

*   `pydub`
*   `ffmpeg` (must be installed on the system for pydub to handle various audio formats)

## 3. Audio Combiner (`audio_combiner.py`)

### 3.1. Overview

The `audio_combiner.py` script provides functionalities to combine multiple audio elements, either by overlaying one audio track onto another or by concatenating them sequentially. This is useful for mixing Lo-fi music with ambient sounds (like rain) or creating longer sequences of baby sounds.

### 3.2. Functions:

*   `combine_audio_elements(base_audio_path, overlay_audio_path, output_path, overlay_volume_db=0, position=0)`:
    *   Overlays `overlay_audio_path` onto `base_audio_path`.
    *   `base_audio_path`: Path to the base audio file.
    *   `overlay_audio_path`: Path to the audio file to overlay.
    *   `output_path`: Path to save the combined audio file.
    *   `overlay_volume_db`: Volume adjustment for the overlay audio in decibels (default is 0 dB).
    *   `position`: Start position of the overlay audio on the base audio in milliseconds (default is 0).

*   `concatenate_audio_elements(audio_files, output_path)`:
    *   Concatenates a list of audio files sequentially.
    *   `audio_files`: A list of paths to audio files to concatenate.
    *   `output_path`: Path to save the concatenated audio file.

### 3.3. Usage:

To test the combining functionality, run the script directly:

```bash
python3 audio_combiner.py
```

This will create `lofi_with_rain.wav`, `baby_with_whitenoise.wav`, and `concatenated_audio.wav` from dummy audio files, demonstrating both overlay and concatenation.

### 3.4. Dependencies:

*   `pydub`
*   `ffmpeg` (must be installed on the system for pydub to handle various audio formats)


