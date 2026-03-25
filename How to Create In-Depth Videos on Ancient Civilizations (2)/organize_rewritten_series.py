'''
import csv
import os

series_content = {}

# The CSV file has a peculiar format where the video package is a long string that contains newlines.
# We need to read the file line by line and handle the multiline video packages.

with open('/home/ubuntu/ancient_civilizations_video_scripts_rewrite.csv', 'r') as f:
    lines = f.readlines()
    header = lines[0].strip().split(',')
    
    # Find the indices of the columns we need
    try:
        series_index = header.index("Series")
        video_package_index = header.index("Video Package")
    except ValueError:
        # If the headers are not found, we can't proceed.
        print("Error: Could not find 'Series' or 'Video Package' in the CSV header.")
        exit()

    # We will process the file by finding the start of each record
    # A record starts with a line that is not part of a video package.
    # We can identify this by checking if the line starts with a quote.
    for i in range(1, len(lines)):
        line = lines[i]
        if not line.startswith('"'):
            parts = line.strip().split(',')
            if len(parts) > max(series_index, video_package_index):
                series = parts[series_index]
                video_package = parts[video_package_index]
                
                # The video package might be split across multiple lines
                # We will read the next lines until we find the start of the next record
                j = i + 1
                while j < len(lines) and lines[j].startswith('"'):
                    video_package += lines[j]
                    j += 1
                
                if series not in series_content:
                    series_content[series] = []
                series_content[series].append(video_package)

output_dir = '/home/ubuntu/rewritten_series_documents'

for series, packages in series_content.items():
    # Sanitize the series name to create a valid filename
    filename = series.replace(" ", "_") + ".md"
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w') as f:
        f.write(f"# {series}\n\n")
        for package in packages:
            f.write(package)
            f.write("\n\n---\n\n")
'''
