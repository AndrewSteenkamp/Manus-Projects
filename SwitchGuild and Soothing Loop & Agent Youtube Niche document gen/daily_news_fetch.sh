#!/bin/bash

LOG_FILE="/home/ubuntu/daily_news_fetch.log"
DATE=$(date)

echo "[$DATE] Running daily news fetch simulation..." >> $LOG_FILE

# In a real scenario, this would call the Python script to fetch news:
# python3 /home/ubuntu/fetch_switch_deals.py >> $LOG_FILE 2>&1

echo "[$DATE] Daily news fetch simulation completed." >> $LOG_FILE


