# AI-Powered UGC Ads Agency Platform

## 1. Overview

This document provides a comprehensive technical overview of the AI-powered UGC ads agency platform. The platform is designed to automate the entire process of creating and managing UGC-style video ads for e-commerce brands across all major platforms.

## 2. System Architecture

The platform is built on a modern, scalable architecture that consists of the following components:

*   **Frontend:** A React-based client dashboard for managing clients, projects, and ads.
*   **Backend:** A Flask-based API for handling business logic, data storage, and integrations.
*   **AI Automation Service:** A Python service that integrates with Perplexity AI, Claude, and MakeUGC.ai to automate the ad creation process.
*   **Lead Generation Service:** A Python service that integrates with BuiltWith, Apollo.io, and Million Verifier to find and validate leads.
*   **Cold Outreach Service:** A Python service that integrates with Instantly, Smartlead, InboxApp, Drippy.ai, and Phantom Buster to automate cold email and social media outreach.
*   **Database:** A SQLite database for storing all platform data.
*   **Workflow Automation:** An n8n workflow for orchestrating the entire ad creation process.

## 3. Frontend

The frontend is a single-page application (SPA) built with React. It uses the following libraries:

*   **React:** For building the user interface.
*   **Vite:** For fast development and bundling.
*   **Tailwind CSS:** For styling.
*   **Shadcn/ui:** For UI components.
*   **Lucide Icons:** For icons.
*   **Recharts:** For data visualization.

## 4. Backend

The backend is a RESTful API built with Flask. It uses the following libraries:

*   **Flask:** For building the API.
*   **Flask-SQLAlchemy:** For database integration.
*   **Flask-CORS:** For handling cross-origin requests.

## 5. AI Automation Service

The AI automation service is a Python script that uses the following AI tools:

*   **Perplexity AI:** For market research and pain point analysis.
*   **Claude:** For ad scriptwriting.
*   **MakeUGC.ai:** For AI UGC video generation.

## 6. Lead Generation Service

The lead generation service is a Python script that uses the following tools:

*   **BuiltWith:** For identifying e-commerce stores across all platforms.
*   **Apollo.io:** For contact discovery.
*   **Million Verifier:** For email validation.

## 7. Cold Outreach Service

The cold outreach service is a Python script that uses the following tools:

*   **Instantly:** For sending cold emails.
*   **Smartlead.ai:** For sending cold emails.
*   **InboxApp:** For social media outreach.
*   **Drippy.ai:** For social media outreach.
*   **Phantom Buster:** For LinkedIn automation.

## 8. Deployment

The platform is designed to be deployed on a cloud server. The frontend and backend can be deployed as separate services, and the AI automation, lead generation, and cold outreach services can be run as background processes.

## 9. Getting Started

To get started with the platform, you will need to:

1.  Clone the repository.
2.  Install the required dependencies for the frontend and backend.
3.  Set up the database.
4.  Configure the API keys for the AI tools and outreach services.
5.  Run the backend server.
6.  Run the frontend development server.
7.  Run the AI automation, lead generation, and cold outreach services.


