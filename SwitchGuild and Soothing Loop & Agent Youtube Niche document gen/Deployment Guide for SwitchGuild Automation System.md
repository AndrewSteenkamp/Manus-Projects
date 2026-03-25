# Deployment Guide for SwitchGuild Automation System

This guide provides instructions for deploying the various components of the SwitchGuild gaming channel automation system. It covers setting up the environment, deploying scripts, and configuring scheduled tasks.

## 1. Prerequisites

Before deployment, ensure you have the following:

*   **Operating System:** A Linux-based system (e.g., Ubuntu) is recommended for server-side components and cron job scheduling.
*   **Python 3:** Installed and configured.
*   **pip3:** Python package installer.
*   **FFmpeg:** Installed on your system. Instructions for Ubuntu:
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
    mkdir -p /opt/switchguild_automation
    cd /opt/switchguild_automation
    ```
2.  **Place Scripts:** Copy all developed Python scripts (`simulate_retroid_transfer.py`, `advanced_video_processor.py`, `walkthrough_generator.py`, `commentary_integrator.py`, `fetch_switch_deals.py`) and shell scripts (`daily_news_fetch.sh`) into this directory.

## 3. Gameplay Recording Setup

### 3.1. Retroid Pocket 5

*   **Manual Transfer:** For simple setups, manually transfer recorded `.mp4` files from your Retroid Pocket 5 to the `processed_retroid_videos` directory (or a designated input directory) on your deployment machine.
*   **Automated Sync (Advanced):** Explore Android apps that can automatically sync specific folders (e.g., your screen recording output folder) to a cloud storage service (Google Drive, Dropbox, Syncthing). On your deployment machine, configure a client for that cloud service to automatically download files to your `processed_retroid_videos` directory.
*   **ADB Scripting (Advanced):** For more technical users, you can write a script using ADB (Android Debug Bridge) to pull files from the Retroid Pocket 5 when it's connected. This requires ADB to be set up on your deployment machine.

### 3.2. Nintendo Switch (and Switch 2)

Refer to the `switch_recording_setup.md` document for detailed instructions on setting up your Nintendo Switch with a capture card and OBS Studio. Ensure OBS is configured to save recordings to a designated input directory on your deployment machine (e.g., `/opt/switchguild_automation/raw_switch_footage`).

## 4. Python Dependencies

Install the necessary Python libraries:

```bash
pip3 install nintendeals
```

## 5. Configuring Scheduled Tasks (Cron)

Cron is used to automate recurring tasks. Here's how to set up the daily news fetch:

1.  **Make Shell Script Executable:**
    ```bash
    chmod +x /opt/switchguild_automation/daily_news_fetch.sh
    ```
2.  **Edit Crontab:** Open your user's crontab for editing:
    ```bash
    crontab -e
    ```
    If prompted, select a text editor (e.g., `nano` or `vim`).
3.  **Add the Cron Job:** Add the following line to the end of the file. This example schedules the script to run daily at midnight (00:00).
    ```cron
    0 0 * * * /opt/switchguild_automation/daily_news_fetch.sh >> /opt/switchguild_automation/cron.log 2>&1
    ```
    *   `0 0 * * *`: Specifies the schedule (minute 0, hour 0, every day of the month, every month, every day of the week).
    *   `>> /opt/switchguild_automation/cron.log 2>&1`: Redirects both standard output and standard error to a log file for debugging.
4.  **Save and Exit:** Save the crontab file. Cron will automatically pick up the changes.

## 6. Manual Execution of Processing Scripts

While some tasks are scheduled, content processing (video trimming, segmenting, commentary integration, walkthrough generation) is typically done on-demand after gameplay sessions. You can execute these scripts manually from your project directory:

*   **Video Merging (from `video_processor.py`):**
    ```bash
    python3 video_processor.py
    ```
*   **Advanced Video Processing (from `advanced_video_processor.py`):**
    ```bash
    python3 advanced_video_processor.py
    ```
*   **Commentary Integration (from `commentary_integrator.py`):**
    ```bash
    python3 commentary_integrator.py
    ```
*   **Walkthrough Generation (from `walkthrough_generator.py`):**
    ```bash
    python3 walkthrough_generator.py
    ```

## 7. Monitoring and Maintenance

*   **Check Cron Logs:** Regularly check `cron.log` for output and errors from scheduled tasks.
*   **Monitor Disk Space:** Video files consume significant disk space. Implement a strategy for archiving or deleting old raw footage after processing.
*   **Review Generated Content:** Always manually review generated news articles, videos, and walkthroughs before publishing to ensure quality and accuracy.


