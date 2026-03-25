# 🚀 DEPLOYMENT GUIDE

This guide provides a comprehensive, step-by-step process to deploy the AI-Powered UGC Advertising Agency using Docker. This method ensures a consistent and reliable setup, regardless of your local machine's configuration.

**Target Audience:** Users with minimal technical experience.
**Time to Deploy:** 15-20 minutes.

---

## 📋 Prerequisites

Before you begin, you need to have two pieces of software installed on your computer.

### 1. Git
Git is a version control system used to download the project files from GitHub.

-   **How to check if it's installed:** Open your terminal (Command Prompt, PowerShell, or Terminal on Mac/Linux) and type `git --version`. If you see a version number (e.g., `git version 2.34.1`), you're all set.
-   **How to install:** If not installed, download it from [git-scm.com](https://git-scm.com/downloads) and follow the installation instructions for your operating system.

### 2. Docker
Docker is a platform that allows us to package the application and all its dependencies into a container, which can then be run anywhere.

-   **How to check if it's installed:** Open your terminal and type `docker --version`. If you see a version number (e.g., `Docker version 20.10.17`), you're good to go.
-   **How to install:** Download and install **Docker Desktop** from the official website: [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop).
    -   **Important:** After installing Docker Desktop, make sure it is running. You should see a small whale icon in your system tray or menu bar.

---

## ⚙️ Step-by-Step Deployment

### Step 1: Clone the Repository

First, you need to download the project files to your computer.

1.  **Open your terminal**.
2.  **Navigate to the directory** where you want to store the project. A good place is your `Documents` folder.
    ```bash
    cd Documents
    ```
3.  **Clone the project** from GitHub using the `git clone` command. (Note: The URL will be provided once the repository is public).
    ```bash
    git clone https://github.com/your-username/ai-ugc-agency.git
    ```
4.  **Navigate into the project directory**:
    ```bash
    cd ai-ugc-agency
    ```

### Step 2: Configure API Keys

The AI agents need API keys to connect to various services. You only need to provide one to get started.

1.  **Find the example file:** In the project folder, you will find a file named `.env.example`. This is a template.

2.  **Create your own `.env` file:**
    -   **Windows:** In the terminal, type:
        ```bash
        copy .env.example .env
        ```
    -   **Mac/Linux:** In the terminal, type:
        ```bash
        cp .env.example .env
        ```

3.  **Get a Free API Key (Hugging Face is Recommended):**
    -   Go to [huggingface.co](https://huggingface.co/) and sign up for a free account.
    -   Navigate to your profile settings, then to **Access Tokens**.
    -   Create a new token with "Read" permissions.
    -   Copy the token (it will start with `hf_`).

4.  **Edit the `.env` file:**
    -   Open the newly created `.env` file in a text editor (like Notepad, VS Code, or Spyder).
    -   Find the line `HF_API_KEY="your_huggingface_token_here"`.
    -   Replace `your_huggingface_token_here` with the key you just copied.
    -   Save and close the file.

### Step 3: Build and Run the Application with Docker

This is the final step, where Docker will build the application and run it.

1.  **Make sure Docker Desktop is running** on your computer.

2.  **In your terminal**, ensure you are still inside the `ai-ugc-agency` project directory.

3.  **Run the Docker Compose command:**
    ```bash
    docker-compose up --build
    ```
    -   `--build`: This tells Docker to build the application from scratch based on the `Dockerfile`.
    -   This command will first download all the necessary base images, then install the Python packages, and finally start the application.
    -   This process might take 5-10 minutes the first time you run it.

4.  **Wait for the build to complete.** You will see a lot of text scrolling in your terminal. The process is finished when you see lines indicating that the web server is running, like:
    ```
    web_1  |  * Running on http://0.0.0.0:5000/
    ```

### Step 4: Access Your Autonomous Agency

Once the application is running, you can access the web dashboard.

1.  **Open your web browser** (Chrome, Firefox, etc.).
2.  **Navigate to:**
    ```
    http://localhost:5000
    ```

You should now see the main dashboard of your AI-Powered UGC Agency. The system is live and the AI agents are running within the Docker container.

---

## 🔧 Managing the Application

-   **To stop the application:**
    -   Go to your terminal window where the application is running.
    -   Press `Ctrl + C`.
    -   To ensure all containers are stopped and removed, run:
        ```bash
        docker-compose down
        ```

-   **To restart the application:**
    -   Navigate back to the project directory in your terminal.
    -   Run:
        ```bash
        docker-compose up
        ```
    -   You don't need to add `--build` unless you have made changes to the code.

---

## 🎉 Congratulations!

You have successfully deployed your own autonomous advertising agency. The AI agents are now managing the simulated business operations. You can monitor their progress and the company's performance through the web dashboard.
