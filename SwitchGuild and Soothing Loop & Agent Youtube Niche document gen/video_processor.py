import subprocess
import os

def merge_videos(input_files, output_file):
    if not all(os.path.exists(f) for f in input_files):
        print("Error: One or more input files not found.")
        return

    # Create a file list for ffmpeg concat
    file_list_path = "file_list.txt"
    with open(file_list_path, "w") as f:
        for input_file in input_files:
            f.write(f"file \'{input_file}\'\n")

    command = [
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", file_list_path,
        "-c", "copy",
        output_file
    ]

    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Successfully merged videos to \'{output_file}\'")
    except subprocess.CalledProcessError as e:
        print(f"Error merging videos: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
    finally:
        if os.path.exists(file_list_path):
            os.remove(file_list_path)

if __name__ == "__main__":
    # Create dummy video files for demonstration
    subprocess.run(["ffmpeg", "-f", "lavfi", "-i", "color=c=red:s=128x128:d=1", "-c:v", "libx264", "-preset", "ultrafast", "video1.mp4"], check=True)
    subprocess.run(["ffmpeg", "-f", "lavfi", "-i", "color=c=blue:s=128x128:d=1", "-c:v", "libx264", "-preset", "ultrafast", "video2.mp4"], check=True)

    input_videos = ["video1.mp4", "video2.mp4"]
    output_merged_video = "merged_gameplay.mp4"
    merge_videos(input_videos, output_merged_video)

    # Clean up dummy files
    os.remove("video1.mp4")
    os.remove("video2.mp4")
    if os.path.exists(output_merged_video):
        os.remove(output_merged_video)


