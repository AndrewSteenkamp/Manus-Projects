# Scheduling Strategy for SwitchGuild Automation

This document outlines a proposed scheduling strategy for the automated tasks within the SwitchGuild gaming channel automation system. The goal is to ensure timely content delivery and efficient resource utilization.

## 1. Automated News Content Generation

**Task:** Fetching Nintendo Switch deals and generating news articles.

**Frequency:** Daily.

**Rationale:** Deals and sales on the eShop can change frequently, and daily updates ensure the news content remains fresh and relevant to the audience. Running it daily also allows for capturing limited-time offers.

**Proposed Schedule:** Once a day, preferably during off-peak hours (e.g., early morning) to minimize impact on system resources and ensure content is ready for review before the main content creation workday begins.

## 2. Gameplay Footage Ingestion and Initial Processing

**Task:** Transferring recorded gameplay from devices (Retroid Pocket 5, PC with capture card) and performing initial processing (e.g., merging segments, basic trimming).

**Frequency:** On-demand or nightly.

**Rationale:**
*   **On-demand:** For immediate processing of critical footage.
*   **Nightly:** To process accumulated footage without interrupting recording sessions or other daytime activities. This leverages idle system resources.

**Proposed Schedule:**
*   **Retroid Pocket 5 Transfer:** Can be triggered manually after a recording session, or set up for automated sync when the device is connected to the network/charging.
*   **PC Footage Transfer/Processing:** A nightly scheduled task (e.g., 2:00 AM local time) to move files from the recording directory to a processing queue and perform initial FFmpeg operations.

## 3. Walkthrough Generation

**Task:** Generating text-based walkthroughs from processed video segments.

**Frequency:** On-demand, after a game's long-form content is finalized and segmented.

**Rationale:** Walkthrough generation is a computationally intensive task that depends on the completion of long-form video processing and segmentation. It's not a continuous process but rather a per-game activity.

**Proposed Schedule:** Manually triggered by the content creator once the prerequisite video segments are ready. This allows for human oversight and quality control before committing resources to AI-driven text generation.

## 4. Content Review and Publishing

**Task:** Manual review of generated news, long-form videos, and walkthroughs, followed by publishing to platforms.

**Frequency:** Daily (for news), On-demand (for videos/walkthroughs).

**Rationale:** Human oversight is critical for maintaining content quality, accuracy, and brand voice. Automated publishing should only occur after explicit human approval.

**Proposed Schedule:** Integrated into the content creator's daily workflow. Automated systems will prepare content, but final publishing will be a manual step.

## 5. System Maintenance and Cleanup

**Task:** Deleting old raw footage, clearing temporary files, database backups.

**Frequency:** Weekly or monthly.

**Rationale:** To maintain system performance, free up storage, and ensure data integrity.

**Proposed Schedule:** Weekly (e.g., Sunday night) for general cleanup, monthly for comprehensive backups.

