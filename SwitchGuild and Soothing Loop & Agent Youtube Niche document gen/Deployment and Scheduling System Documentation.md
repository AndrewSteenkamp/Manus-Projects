# Deployment and Scheduling System Documentation

This document provides a comprehensive overview of the deployment and scheduling aspects of the SwitchGuild gaming channel automation system.

## 1. Scheduling Strategy

The automation system employs a hybrid scheduling approach, combining automated recurring tasks with on-demand manual triggers, to optimize resource utilization and maintain human oversight for quality control. The key components and their scheduling are as follows:

### 1.1. Automated News Content Generation

*   **Task:** Fetching the latest Nintendo Switch deals and generating news articles.
*   **Frequency:** Daily.
*   **Rationale:** To ensure the news content is always fresh and relevant, capturing dynamic changes in eShop sales and limited-time offers.
*   **Implementation:** Configured as a daily cron job, typically running during off-peak hours (e.g., midnight) to prepare content for review before the content creation workday begins.

### 1.2. Gameplay Footage Ingestion and Initial Processing

*   **Task:** Transferring raw gameplay footage from recording devices (Retroid Pocket 5, PC with capture card) and performing initial video processing (e.g., merging segments, basic trimming).
*   **Frequency:** On-demand or nightly.
*   **Rationale:** Allows for immediate processing of critical footage or leverages idle system resources during off-hours for bulk processing of accumulated recordings.
*   **Implementation:**
    *   **Retroid Pocket 5:** Can be initiated manually after a recording session or set up for automated synchronization via cloud services or ADB scripting when the device is connected.
    *   **PC Footage:** A nightly scheduled task (e.g., via cron) moves files from the recording directory to a processing queue and executes initial FFmpeg operations.

### 1.3. Walkthrough Generation

*   **Task:** Generating text-based walkthroughs from processed video segments.
*   **Frequency:** On-demand.
*   **Rationale:** This is a computationally intensive task dependent on the completion of long-form video processing and segmentation. It's a per-game activity rather than a continuous process.
*   **Implementation:** Manually triggered by the content creator once the necessary video segments are ready, allowing for human review and quality control before resource commitment.

### 1.4. Content Review and Publishing

*   **Task:** Manual review and approval of all generated content (news, long-form videos, walkthroughs) before publishing to platforms.
*   **Frequency:** Daily for news; on-demand for videos and walkthroughs.
*   **Rationale:** Human oversight is paramount for maintaining content quality, accuracy, and adherence to brand standards. Automated publishing only occurs after explicit human approval.
*   **Implementation:** Integrated into the content creator's daily workflow. Automated systems prepare content, but the final publishing step remains manual.

### 1.5. System Maintenance and Cleanup

*   **Task:** Deleting old raw footage, clearing temporary files, and performing database backups.
*   **Frequency:** Weekly or monthly.
*   **Rationale:** Essential for maintaining system performance, managing storage, and ensuring data integrity.
*   **Implementation:** Scheduled via cron (e.g., weekly on Sunday night) for general cleanup and monthly for comprehensive backups.

## 2. Deployment Instructions

This section summarizes the key steps for deploying the SwitchGuild automation system. For detailed instructions, refer to the `deployment_guide.md` document.

### 2.1. Environment Setup

*   **Operating System:** Linux (e.g., Ubuntu) is recommended.
*   **Software Installation:** Ensure Python 3, pip3, FFmpeg, and cron are installed.

### 2.2. Project Structure

*   Create a dedicated project directory (e.g., `/opt/switchguild_automation`).
*   Place all Python scripts (`simulate_retroid_transfer.py`, `advanced_video_processor.py`, `walkthrough_generator.py`, `commentary_integrator.py`, `fetch_switch_deals.py`) and shell scripts (`daily_news_fetch.sh`) within this directory.

### 2.3. Python Dependencies

*   Install required Python libraries using pip:
    ```bash
    pip3 install nintendeals
    ```

### 2.4. Gameplay Recording Configuration

*   **Retroid Pocket 5:** Configure manual transfer, cloud sync, or ADB scripting to move recorded footage to a designated input directory on the deployment machine.
*   **Nintendo Switch:** Set up a capture card with OBS Studio to record gameplay, ensuring recordings are saved to a specified input directory on the deployment machine.

### 2.5. Cron Job Setup

*   Make shell scripts executable (e.g., `chmod +x daily_news_fetch.sh`).
*   Add cron entries using `crontab -e` to schedule recurring tasks. For example, for daily news fetching:
    ```cron
    0 0 * * * /opt/switchguild_automation/daily_news_fetch.sh >> /opt/switchguild_automation/cron.log 2>&1
    ```

### 2.6. Manual Script Execution

*   Video processing, commentary integration, and walkthrough generation scripts are designed for on-demand execution. They can be run directly from the project directory as needed.

## 3. Monitoring and Maintenance

*   Regularly check cron logs for task execution status and errors.
*   Monitor disk space usage, especially for video files, and implement archiving or cleanup routines.
*   Always perform manual review of all generated content before publishing to maintain quality and accuracy.

