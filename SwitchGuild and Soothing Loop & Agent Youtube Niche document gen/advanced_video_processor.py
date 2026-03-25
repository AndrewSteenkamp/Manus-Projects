import subprocess
import os

def trim_video(input_file, start_time, end_time, output_file):
    """Trims a video from start_time to end_time."""
    command = [
        "ffmpeg",
        "-i", input_file,
        "-ss", str(start_time),
        "-to", str(end_time),
        "-c", "copy",
        output_file
    ]
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Successfully trimmed \'{input_file}\' from {start_time} to {end_time} as \'{output_file}\'")
    except subprocess.CalledProcessError as e:
        print(f"Error trimming video: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")

def segment_video(input_file, segment_duration, output_prefix):
    """Segments a video into chunks of specified duration."""
    command = [
        "ffmpeg",
        "-i", input_file,
        "-c", "copy",
        "-map", "0",
        "-segment_time", str(segment_duration),
        "-f", "segment",
        f"{output_prefix}_%03d.mp4"
    ]
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Successfully segmented \'{input_file}\' into {segment_duration}s chunks with prefix \'{output_prefix}\'")
    except subprocess.CalledProcessError as e:
        print(f"Error segmenting video: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")

if __name__ == "__main__":
    # Create a dummy video file for testing
    dummy_video = "dummy_gameplay.mp4"
    subprocess.run(["ffmpeg", "-f", "lavfi", "-i", "testsrc=duration=10:size=1280x720:rate=30", "-c:v", "libx264", "-preset", "ultrafast", dummy_video], check=True)

    # Test trimming
    trimmed_video = "trimmed_gameplay.mp4"
    trim_video(dummy_video, 2, 7, trimmed_video)

    # Test segmenting
    segment_video(dummy_video, 3, "segmented_gameplay")

    # Clean up dummy files
    os.remove(dummy_video)
    if os.path.exists(trimmed_video):
        os.remove(trimmed_video)
    # Clean up segmented files (assuming 10s video, 3s segments -> 4 files)
    for i in range(4):
        segment_file = f"segmented_gameplay_{i:03d}.mp4"
        if os.path.exists(segment_file):
            os.remove(segment_file)


