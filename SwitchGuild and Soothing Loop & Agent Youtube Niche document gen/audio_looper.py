from pydub import AudioSegment

def create_seamless_loop(input_file, output_file, loop_duration_ms):
    """Creates a seamlessly looped audio file."""
    try:
        audio = AudioSegment.from_file(input_file)

        # If the audio is shorter than the loop duration, repeat it
        if len(audio) < loop_duration_ms:
            num_repeats = (loop_duration_ms // len(audio)) + 1
            looped_audio = audio * num_repeats
        else:
            looped_audio = audio

        # Trim to the exact loop duration
        final_loop = looped_audio[:loop_duration_ms]

        # Apply a short crossfade at the loop point to ensure seamlessness
        # This assumes the original audio is long enough to crossfade within the loop_duration_ms
        # For very short source audio, this might need more complex logic (e.g., crossfading the original ends)
        crossfade_duration = min(500, len(final_loop) // 4) # 500ms or 1/4 of loop duration, whichever is smaller
        if len(final_loop) > crossfade_duration * 2:
            final_loop = final_loop.fade_in(crossfade_duration).fade_out(crossfade_duration)

        final_loop.export(output_file, format="wav")
        print(f"Successfully created seamless loop from \'{input_file}\' to \'{output_file}\' with duration {loop_duration_ms}ms.")

    except Exception as e:
        print(f"Error creating seamless loop: {e}")

if __name__ == "__main__":
    # Create a dummy audio file for testing (e.g., a short sine wave)
    # Requires ffmpeg to be installed
    import subprocess
    import os

    dummy_audio_file = "dummy_short_audio.wav"
    subprocess.run(["ffmpeg", "-f", "lavfi", "-i", "sine=frequency=440:duration=5", "-c:a", "pcm_s16le", "-ar", "44100", dummy_audio_file], check=True)

    # Test with a loop duration longer than the source audio
    create_seamless_loop(dummy_audio_file, "looped_audio_15s.wav", 15000) # 15 seconds

    # Test with a loop duration shorter than the source audio (should just trim)
    create_seamless_loop(dummy_audio_file, "looped_audio_3s.wav", 3000) # 3 seconds

    # Clean up dummy files
    os.remove(dummy_audio_file)
    if os.path.exists("looped_audio_15s.wav"):
        os.remove("looped_audio_15s.wav")
    if os.path.exists("looped_audio_3s.wav"):
        os.remove("looped_audio_3s.wav")


