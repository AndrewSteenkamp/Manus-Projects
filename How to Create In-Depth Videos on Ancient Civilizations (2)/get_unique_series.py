
import pandas as pd

df = pd.read_csv('/home/ubuntu/ancient_civilizations_video_scripts_rewrite.csv')

for series in df["Series"].unique():
    print(series)
