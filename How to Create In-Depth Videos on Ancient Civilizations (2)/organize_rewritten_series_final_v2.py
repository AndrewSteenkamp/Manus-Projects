
import pandas as pd
import os
import re

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('/home/ubuntu/ancient_civilizations_video_scripts_rewrite.csv')

# Create a mapping from the topics to the correct series names
topic_to_series = {}
with open('/home/ubuntu/ancient_civilizations_content_plan.md', 'r') as f:
    content = f.read()
    current_series = ""
    for line in content.split('\n'):
        if line.startswith('### Series'):
            current_series = line.split(':')[1].strip()
        elif line.startswith('|'):
            columns = line.split('|')
            if len(columns) > 3 and "Potential Video Topics" not in columns[3] and "---" not in columns[3]:
                potential_topics = columns[3].strip()
                topics = [t.strip().replace('"', '') for t in re.split(r',|\n', potential_topics) if t.strip()]
                for topic in topics:
                    topic_to_series[topic] = current_series

# Apply the mapping to the 'Series' column
df['Series'] = df['Topic'].map(topic_to_series)

# Group the DataFrame by the corrected 'Series' column
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
