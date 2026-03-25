import subprocess
import os

def integrate_commentary(video_file, audio_file, output_file):
    """Integrates a separate audio commentary track with a video file."""
    command = [
        "ffmpeg",
        "-i", video_file,
        "-i", audio_file,
        "-c:v", "copy",
        "-c:a", "aac", # Re-encode audio to AAC for compatibility
        "-map", "0:v:0", # Map video stream from first input
        "-map", "1:a:0", # Map audio stream from second input
        "-shortest", # End encoding when the shortest input stream ends
        output_file
    ]
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Successfully integrated \'{audio_file}\' with \'{video_file}\' into \'{output_file}\'")
    except subprocess.CalledProcessError as e:
        print(f"Error integrating commentary: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")

if __name__ == "__main__":
    # Create dummy video and audio files for testing
    dummy_video = "dummy_video.mp4"
    dummy_audio = "dummy_audio.wav"
    output_integrated = "integrated_video.mp4"

    # Create a dummy video (5 seconds)
    subprocess.run(["ffmpeg", "-f", "lavfi", "-i", "testsrc=duration=5:size=640x480:rate=30", "-c:v", "libx264", "-preset", "ultrafast", dummy_video], check=True)
    # Create a dummy audio (5 seconds)
    subprocess.run(["ffmpeg", "-f", "lavfi", "-i", "sine=frequency=1000:duration=5", "-c:a", "pcm_s16le", "-ar", "44100", dummy_audio], check=True)

    integrate_commentary(dummy_video, dummy_audio, output_integrated)

    # Clean up dummy files
    os.remove(dummy_video)
    os.remove(dummy_audio)
    if os.path.exists(output_integrated):
        os.remove(output_integrated)


