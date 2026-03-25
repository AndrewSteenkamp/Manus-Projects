from pydub import AudioSegment

def combine_audio_elements(base_audio_path, overlay_audio_path, output_path, overlay_volume_db=0, position=0):
    """Combines a base audio track with an overlay audio track.

    Args:
        base_audio_path (str): Path to the base audio file.
        overlay_audio_path (str): Path to the audio file to overlay.
        output_path (str): Path to save the combined audio file.
        overlay_volume_db (int): Volume adjustment for the overlay audio in dB (e.g., -10 for quieter).
        position (int): Position in milliseconds where the overlay audio should start on the base audio.
    """
    try:
        base_audio = AudioSegment.from_file(base_audio_path)
        overlay_audio = AudioSegment.from_file(overlay_audio_path)

        # Adjust volume of overlay audio
        overlay_audio = overlay_audio + overlay_volume_db

        # Overlay the audio
        combined_audio = base_audio.overlay(overlay_audio, position=position)

        combined_audio.export(output_path, format="wav")
        print(f"Successfully combined {base_audio_path} with {overlay_audio_path} into {output_path}")

    except Exception as e:
        print(f"Error combining audio elements: {e}")

def concatenate_audio_elements(audio_files, output_path):
    """Concatenates multiple audio files sequentially.

    Args:
        audio_files (list): List of paths to audio files to concatenate.
        output_path (str): Path to save the concatenated audio file.
    """
    try:
        combined = AudioSegment.empty()
        for audio_file in audio_files:
            audio = AudioSegment.from_file(audio_file)
            combined += audio

        combined.export(output_path, format="wav")
        print(f"Successfully concatenated {audio_files} into {output_path}")

    except Exception as e:
        print(f"Error concatenating audio elements: {e}")

if __name__ == "__main__":
    import os
    import subprocess

    # Create dummy audio files for testing
    # Requires ffmpeg to be installed
    def create_dummy_audio(filename, duration_s, freq=440):
        subprocess.run(["ffmpeg", "-f", "lavfi", "-i", f"sine=frequency={freq}:duration={duration_s}",
                        "-c:a", "pcm_s16le", "-ar", "44100", filename], check=True)

    lofi_track = "dummy_lofi.wav"
    rain_sound = "dummy_rain.wav"
    baby_sound = "dummy_baby.wav"
    white_noise = "dummy_white_noise.wav"

    create_dummy_audio(lofi_track, 30, 220)
    create_dummy_audio(rain_sound, 30, 100)
    create_dummy_audio(baby_sound, 10, 880)
    create_dummy_audio(white_noise, 30, 50)

    # Example 1: Combine Lo-fi track with rain sound
    output_lofi_rain = "lofi_with_rain.wav"
    combine_audio_elements(lofi_track, rain_sound, output_lofi_rain, overlay_volume_db=-15)

    # Example 2: Combine baby sound with white noise (overlay baby sound on white noise)
    output_baby_whitenoise = "baby_with_whitenoise.wav"
    combine_audio_elements(white_noise, baby_sound, output_baby_whitenoise, overlay_volume_db=0, position=5000) # Start baby sound at 5 seconds

    # Example 3: Concatenate multiple short audio files
    output_concatenated = "concatenated_audio.wav"
    concatenate_audio_elements([lofi_track, baby_sound, rain_sound], output_concatenated)

    # Clean up dummy files
    for f in [lofi_track, rain_sound, baby_sound, white_noise, output_lofi_rain, output_baby_whitenoise, output_concatenated]:
        if os.path.exists(f):
            os.remove(f)


