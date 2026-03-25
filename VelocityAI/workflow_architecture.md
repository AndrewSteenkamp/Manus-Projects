# AI Automation Workflow Design and Architecture

## 1. End-to-End Ad Creation Workflow

The ad creation process will be fully automated, from initial research to final video generation. The workflow is as follows:

1.  **Client Input:** The client provides the product name and a link to their Shopify product page through our platform's client portal.

2.  **Pain Point Research:** The system uses Perplexity AI to research the pain points that the client's product solves. It will scrape Reddit and other forums for authentic customer language.

3.  **Ad Script Generation:** The pain points and customer quotes are fed into Claude, which generates multiple variations of a 30-second ad script.

4.  **AI UGC Video Generation:** The ad scripts are then sent to MakeUGC.ai, which generates the video ads using AI avatars. The client's product image is also uploaded to be included in the video.

5.  **Client Review and Approval:** The generated video ads are made available to the client for review and approval in their dashboard.

## 2. n8n Workflow Architecture

The entire workflow will be orchestrated using n8n. The n8n workflow will consist of the following nodes:

*   **Webhook Node:** This node will be triggered when a client submits a new ad request through our platform.
*   **HTTP Request Nodes:** These nodes will be used to interact with the APIs of Perplexity AI, Claude, and MakeUGC.ai.
*   **Function Nodes:** These nodes will be used to process and transform the data between the different API calls.
*   **Data Store Nodes:** These nodes will be used to store and retrieve data about clients, projects, and ads.
*   **Email Node:** This node will be used to send notifications to the client and the internal team.

## 3. Data Models and API Specifications

### Data Models

*   **Client:**
    *   `id`: string (UUID)
    *   `name`: string
    *   `email`: string
    *   `shopify_store_url`: string
*   **Project:**
    *   `id`: string (UUID)
    *   `client_id`: string (foreign key)
    *   `product_name`: string
    *   `product_url`: string
    *   `status`: string (e.g., "in_progress", "completed")
*   **Ad:**
    *   `id`: string (UUID)
    *   `project_id`: string (foreign key)
    *   `script`: string
    *   `video_url`: string
    *   `status`: string (e.g., "pending_review", "approved")

### API Specifications

*   **`POST /api/projects`**: Create a new project.
*   **`GET /api/projects`**: Get a list of all projects.
*   **`GET /api/projects/{project_id}`**: Get a single project.
*   **`GET /api/projects/{project_id}/ads`**: Get all ads for a project.
*   **`POST /api/ads/{ad_id}/approve`**: Approve an ad.


