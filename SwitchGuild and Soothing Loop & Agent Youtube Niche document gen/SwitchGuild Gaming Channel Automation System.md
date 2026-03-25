# SwitchGuild Gaming Channel Automation System

This repository contains the design, development, and deployment documentation and scripts for automating various aspects of the SwitchGuild gaming channel. The system aims to streamline gameplay recording, content packaging (long-form videos and walkthroughs), and automated news content generation for Nintendo Switch deals and game recommendations.

## Project Overview

The automation system is designed to assist with:

*   **Gameplay Capture:** Recording footage from Retroid Pocket 5 and Nintendo Switch/Switch 2.
*   **Content Processing:** Trimming, segmenting, and integrating commentary into gameplay videos.
*   **Walkthrough Generation:** Creating text-based walkthroughs from video segments.
*   **Automated News:** Generating news content on Nintendo Switch deals and game recommendations (feature to be fully implemented).

## Documentation

*   **Design Document (`design_document.md`):** Provides a detailed overview of the system's architecture and workflow for each component.
*   **Gameplay Recording and Processing Tools Documentation (`gameplay_tools_documentation.md`):** Explains the developed tools for gameplay capture and initial video processing.
*   **Content Packaging and Walkthrough Generation Tools Documentation (`content_packaging_tools_documentation.md`):** Details the scripts for advanced video processing, walkthrough generation, and commentary integration.
*   **Deployment and Scheduling System Documentation (`deployment_and_scheduling_documentation.md`):** Outlines the scheduling strategy and deployment instructions for the automated system.
*   **Deployment Guide (`deployment_guide.md`):** A practical guide for setting up and deploying the system.
*   **Nintendo Switch Recording Setup (`switch_recording_setup.md`):** Specific instructions for recording Nintendo Switch gameplay using a capture card and OBS Studio.

## Scripts

*   `simulate_retroid_transfer.py`: Python script to simulate file transfer from Retroid Pocket 5.
*   `video_processor.py`: Python script for basic video merging using FFmpeg.
*   `advanced_video_processor.py`: Python script for advanced video trimming and segmenting using FFmpeg.
*   `walkthrough_generator.py`: Python script for generating text-based walkthroughs (currently a placeholder for AI integration).
*   `commentary_integrator.py`: Python script for integrating audio commentary with video files.
*   `fetch_switch_deals.py`: Python script for fetching Nintendo Switch deals and generating news content (currently facing API challenges).
*   `daily_news_fetch.sh`: Shell script to be used with cron for scheduling daily news updates.

## Getting Started

Refer to the `deployment_guide.md` for detailed instructions on setting up the environment, deploying the scripts, and configuring scheduled tasks.

## Future Enhancements

*   Full implementation of automated news content generation with a reliable data source.
*   Integration of AI for advanced video analysis (object detection, OCR, speech-to-text) to enhance walkthrough generation.
*   Development of a user interface for easier management and monitoring of the automation system.

---

**Author:** Manus AI
**Date:** September 10, 2025


