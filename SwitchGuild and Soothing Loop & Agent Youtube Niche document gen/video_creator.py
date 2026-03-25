import subprocess
import os

def create_video_from_audio_image(audio_path, image_path, output_video_path, duration_s):
    """Creates a video file from an audio file and a static image.

    Args:
        audio_path (str): Path to the input audio file.
        image_path (str): Path to the input image file.
        output_video_path (str): Path to save the output video file.
        duration_s (int): Duration of the output video in seconds.
    """
    try:
        command = [
            "ffmpeg",
            "-loop", "1",                # Loop the image indefinitely
            "-i", image_path,           # Input image
            "-i", audio_path,           # Input audio
            "-c:v", "libx264",          # Video codec
            "-tune", "stillimage",      # Optimize for still images
            "-preset", "ultrafast",     # Faster encoding
            "-crf", "18",               # Constant Rate Factor for quality
            "-c:a", "aac",              # Audio codec
            "-b:a", "192k",             # Audio bitrate
            "-pix_fmt", "yuv420p",      # Pixel format for broad compatibility
            "-shortest",                # End video when shortest input (audio) ends
            "-t", str(duration_s),      # Set video duration
            output_video_path
        ]
        subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Successfully created video \'{output_video_path}\' from \'{audio_path}\' and \'{image_path}\\'")
    except subprocess.CalledProcessError as e:
        print(f"Error creating video: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")

if __name__ == "__main__":
    # Create dummy audio and image files for testing
    # Ensure noise_generator.py and media_generate_image (or dummy files) have been run
    # For demonstration, we'll create dummy files if they don't exist

    dummy_audio = "test_audio.wav"
    dummy_image = "test_image.png"
    output_video = "test_video.mp4"

    if not os.path.exists(dummy_audio):
        # Create a dummy audio file (e.g., 60 seconds of white noise)
        from pydub import AudioSegment
        import numpy as np
        samples = np.random.uniform(-1, 1, int(60 * 44100)).astype(np.float32)
        samples_int16 = (samples * 32767).astype(np.int16)
        audio = AudioSegment(samples_int16.tobytes(), frame_rate=44100, sample_width=2, channels=1)
        audio.export(dummy_audio, format="wav")
        print(f"Created dummy audio: {dummy_audio}")

    if not os.path.exists(dummy_image):
        # Create a dummy image file (simple black image)
        from PIL import Image
        img = Image.new("RGB", (1920, 1080), color = (0, 0, 0))
        img.save(dummy_image)
        print(f"Created dummy image: {dummy_image}")

    # Example usage:
    create_video_from_audio_image(dummy_audio, dummy_image, output_video, 60)

    # Clean up dummy files
    if os.path.exists(dummy_audio):
        os.remove(dummy_audio)
    if os.path.exists(dummy_image):
        os.remove(dummy_image)
    if os.path.exists(output_video):
        os.remove(output_video)


