'''
import re

with open("/home/ubuntu/ancient_civilizations_content_plan.md", "r") as f:
    content = f.read()

topics = re.findall(r'\"(.*?)\"', content)

print(topics)

with open("/home/ubuntu/video_topics.txt", "w") as f:
    for topic in topics:
        f.write(topic + "\n")
'''
