
import pandas as pd
import os

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('/home/ubuntu/ancient_civilizations_video_scripts_rewrite.csv')

# Group the DataFrame by the 'Series' column
grouped = df.groupby('Series')

output_dir = '/home/ubuntu/rewritten_series_documents'

# Iterate over each group and create a markdown file for each series
for series_name, group in grouped:
    # Sanitize the series name to create a valid filename
    filename = series_name.replace(" ", "_") + ".md"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w') as f:
        f.write(f"# {series_name}\n\n")
        for index, row in group.iterrows():
            f.write(row['Video Package'])
            f.write("\n\n---\n\n")
