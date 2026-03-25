'''
import re

with open('/home/ubuntu/ancient_civilizations_content_plan.md', 'r') as f:
    content = f.read()

topics = []
lines = content.split('\n')
for line in lines:
    if line.startswith('|'):
        columns = line.split('|')
        if len(columns) > 3 and "Potential Video Topics" not in columns[3] and "---" not in columns[3]:
            potential_topics = columns[3].strip()
            # The topics are separated by commas or newlines in some cases
            # Let's split them and add to the list
            topics.extend([t.strip().replace('\'\'\', '') for t in re.split(r',|\n', potential_topics) if t.strip()])

# Remove duplicates and empty strings
topics = sorted(list(set(filter(None, topics))))

for topic in topics:
    print(topic)
'''
