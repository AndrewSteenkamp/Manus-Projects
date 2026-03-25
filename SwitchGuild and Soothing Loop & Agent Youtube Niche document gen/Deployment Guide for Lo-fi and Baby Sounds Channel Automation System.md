# Deployment Guide for Lo-fi and Baby Sounds Channel Automation System

This guide provides instructions for deploying the various components of the Lo-fi and Baby Sounds Channel Automation System. It covers setting up the environment, deploying scripts, and configuring scheduled tasks.

## 1. Prerequisites

Before deployment, ensure you have the following:

*   **Operating System:** A Linux-based system (e.g., Ubuntu) is recommended for server-side components and cron job scheduling.
*   **Python 3:** Installed and configured.
*   **pip3:** Python package installer.
*   **FFmpeg:** Installed on your system. FFmpeg is crucial for audio and video processing. Instructions for Ubuntu:
    ```bash
    sudo apt-get update
    sudo apt-get install -y ffmpeg
    ```
*   **cron:** Installed for scheduling tasks. Instructions for Ubuntu:
    ```bash
    sudo apt-get update
    sudo apt-get install -y cron
    ```
*   **Git (Optional but Recommended):** For version control and easy deployment of scripts from a repository.

## 2. Project Setup

1.  **Create a Project Directory:** Choose a suitable location on your system for the project files. For example:
    ```bash
    mkdir -p /opt/lofi_baby_sounds_automation
    cd /opt/lofi_baby_sounds_automation
    ```
2.  **Place Scripts:** Copy all developed Python scripts (`noise_generator.py`, `audio_looper.py`, `audio_combiner.py`, `video_creator.py`, `metadata_generator.py`) and shell scripts (`daily_content_gen.sh`) into this directory.

## 3. Python Dependencies

Install the necessary Python libraries:

```bash
pip3 install pydub numpy scipy Pillow
```

## 4. Configuring Scheduled Tasks (Cron)

Cron is used to automate recurring tasks. Here's how to set up a daily content generation task:

1.  **Make Shell Script Executable:**
    ```bash
    chmod +x /opt/lofi_baby_sounds_automation/daily_content_gen.sh
    ```
2.  **Edit Crontab:** Open your user's crontab for editing:
    ```bash
    crontab -e
    ```
    If prompted, select a text editor (e.g., `nano` or `vim`).
3.  **Add the Cron Job:** Add the following line to the end of the file. This example schedules the script to run daily at 1 AM (01:00).
    ```cron
    0 1 * * * /opt/lofi_baby_sounds_automation/daily_content_gen.sh >> /opt/lofi_baby_sounds_automation/cron_content.log 2>&1
    ```
    *   `0 1 * * *`: Specifies the schedule (minute 0, hour 1, every day of the month, every month, every day of the week).
    *   `>> /opt/lofi_baby_sounds_automation/cron_content.log 2>&1`: Redirects both standard output and standard error to a log file for debugging.
4.  **Save and Exit:** Save the crontab file. Cron will automatically pick up the changes.

## 5. Manual Execution of Content Generation Scripts

While some tasks can be scheduled, you might want to manually trigger content generation for specific needs or testing. You can execute these scripts directly from your project directory:

*   **Generate Noise:**
    ```bash
    python3 noise_generator.py
    ```
*   **Create Seamless Audio Loops:**
    ```bash
    python3 audio_looper.py
    ```
*   **Combine Audio Elements:**
    ```bash
    python3 audio_combiner.py
    ```
*   **Create Video from Audio and Image:**
    ```bash
    python3 video_creator.py
    ```
*   **Generate Video Metadata:**
    ```bash
    python3 metadata_generator.py
    ```

## 6. Monitoring and Maintenance

*   **Check Cron Logs:** Regularly check `cron_content.log` for output and errors from scheduled tasks.
*   **Monitor Disk Space:** Video and audio files can consume significant disk space. Implement a strategy for archiving or deleting old raw files after processing.
*   **Review Generated Content:** Always manually review generated videos and their metadata before publishing to ensure quality and accuracy.
*   **YouTube API Integration (Future):** For automated uploading and scheduling of videos, you would need to integrate with the YouTube Data API. This involves setting up OAuth authentication and handling API quotas. This is beyond the scope of the current automated scripts but is a crucial next step for full automation.

