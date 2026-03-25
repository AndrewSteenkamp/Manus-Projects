import os
import shutil

def simulate_transfer(source_file, destination_dir):
    if not os.path.exists(source_file):
        print(f"Error: Source file '{source_file}' not found.")
        return
    if not os.path.isdir(destination_dir):
        print(f"Error: Destination directory '{destination_dir}' not found.")
        return

    try:
        shutil.move(source_file, destination_dir)
        print(f"Successfully moved '{source_file}' to '{destination_dir}'.")
    except Exception as e:
        print(f"Error moving file: {e}")

if __name__ == "__main__":
    source_file = "retroid_gameplay_20250910_001.mp4"
    destination_dir = "processed_retroid_videos"
    simulate_transfer(source_file, destination_dir)


