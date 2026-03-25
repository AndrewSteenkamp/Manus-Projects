'''
# 🚀 Your First Autonomous AI Business: A Complete Beginner's Guide

**Welcome!**

This guide is designed for someone with **absolutely zero coding experience**. We will walk through every single step to get your AI-powered UGC (User-Generated Content) agency running.

**Your Role:** You are the Director. You will oversee the business, but you won't write any code. Your AI agents will do the work.

**What This System Does:**
This is a real, working business that automatically:
1.  **Finds clients** (leads) for your agency.
2.  **Creates UGC video packages** (scripts and voiceovers) for those clients.
3.  **Manages the business** with a team of AI agents (CEO, CFO, Sales, Creative).

**Two Modes of Operation:**
1.  **🧪 Test Mode (Default):** Runs the entire business using FAKE money and FAKE payments. This is for you to learn and test everything safely.
2.  **💰 Live Mode:** Uses REAL money and REAL payment processing once you are ready.

---

## 📝 Table of Contents

**Part 1: Getting Started (What You Need)**
*   Step 1: Understanding Your Business
*   Step 2: Required Accounts (All FREE)

**Part 2: Setting Up Your Local Computer (No Cloud Servers Needed)**
*   Step 3: Installing Anaconda (Your AI Toolbox)
*   Step 4: Creating a Safe Space (Your Anaconda Environment)
*   Step 5: Getting the Project Files

**Part 3: Running Your Autonomous Agency**
*   Step 6: Starting the Agency for the First Time
*   Step 7: Using the Director's Dashboard
*   Step 8: Running Your First Daily Operations (in Test Mode)
*   Step 9: Understanding the Reports

**Part 4: Going Live (When You're Ready)**
*   Step 10: Switching to Live Mode
*   Step 11: Setting Up Real Payments (Paystack for South Africa)

---

## Part 1: Getting Started (What You Need)

### Step 1: Understanding Your Business

Your business sells "UGC Video Packages" to other e-commerce companies. These packages contain everything a company needs to create high-quality, authentic-looking video ads.

*   **Your Product:** A set of 3-10 professional video scripts and AI-generated voiceovers.
*   **Your Price:** You can charge between R5,000 - R15,000 per package.
*   **Your Cost:** Almost zero. You only pay for the AI services, which are very cheap (around R1 per package).

### Step 2: Required Accounts (All FREE)

Before we start, you need to sign up for one free account. This will be your "key" to the AI's brain.

1.  **OpenAI API Key:**
    *   Go to `https://platform.openai.com/signup` and create a free account.
    *   After signing up, go to the [API Keys section](https://platform.openai.com/api-keys).
    *   Click "**Create new secret key**".
    *   Name it `UGC-Agency-Key`.
    *   **COPY THIS KEY IMMEDIATELY** and save it in a safe place (like a Notepad file). You will **never** see it again.

This key is like a password that lets your AI agents use the powerful GPT-4 model for making decisions and writing content.

---

## Part 2: Setting Up Your Local Computer

We will set up everything on your own computer. You don't need to pay for any servers.

### Step 3: Installing Anaconda (Your AI Toolbox)

Anaconda is a free and easy way to manage all the Python tools we need.

1.  Go to the [Anaconda Distribution page](https://www.anaconda.com/download).
2.  Download the installer for your operating system (Windows, macOS, or Linux).
3.  Run the installer and follow the on-screen instructions. **Accept all the default settings.**

### Step 4: Creating a Safe Space (Your Anaconda Environment)

We will create a dedicated "environment" for our project. This is like a clean, separate workshop where our AI agency can operate without messing up anything else on your computer.

1.  **Open Anaconda Navigator** (it was installed in the previous step).
2.  On the left-hand menu, click on **Environments**.
3.  At the bottom, click the **Create** button.
4.  In the "Name" field, type `ugc-agency`.
5.  Make sure "Python" is selected and the version is `3.11` or higher.
6.  Click **Create**. This might take a few minutes.

### Step 5: Getting the Project Files

I have packaged the entire business into a single ZIP file. You just need to download and extract it.

1.  **Download the project file:** `[A link to the downloadable ZIP file will be provided here]`
2.  **Create a folder** on your computer where you want to keep your business. For example, `C:\Users\YourName\Documents\AI_Agency`.
3.  **Extract the ZIP file** into this new folder.

You should now have a folder named `ugc_agency` with all the project files inside.

---

## Part 3: Running Your Autonomous Agency

Now for the exciting part! Let's bring your AI agents to life.

### Step 6: Starting the Agency for the First Time

We need to open a "terminal" or "command prompt" inside our special Anaconda environment.

1.  Go back to **Anaconda Navigator** -> **Environments**.
2.  Click on the `ugc-agency` environment you created.
3.  Click the **play button (▶)** next to it, and then click **Open Terminal**.

   A black window (the terminal) will appear. This is our command center.

4.  **Navigate to your project folder.** Type `cd` (which means "change directory"), followed by a space, and then the path to your project folder. It might look like this:
    ```bash
    cd C:\Users\YourName\Documents\AI_Agency\ugc_agency
    ```
    *Tip: You can drag and drop the folder from your file explorer into the terminal window to paste the path automatically.* Hit **Enter**.

5.  **Run the automatic setup.** This one-time command will install all the tools your agents need. Type the following and press **Enter**:
    ```bash
    pip install -r requirements.txt
    ```

6.  **Set your API Key.** We need to tell the system your secret OpenAI key. Type the following, replacing `YOUR_API_KEY_HERE` with the key you copied earlier:
    ```bash
    # For Windows
    set OPENAI_API_KEY=YOUR_API_KEY_HERE

    # For Mac/Linux
    export OPENAI_API_KEY=YOUR_API_KEY_HERE
    ```
    Press **Enter**.

### Step 7: Using the Director's Dashboard

Now, let's start the main dashboard. This is your control panel for the entire business.

1.  In the same terminal, type the following command and press **Enter**:
    ```bash
    python web_dashboard.py
    ```

2.  You will see some text appear, and then a message like `Running on http://127.0.0.1:5000`.

3.  **Open your web browser** (like Chrome or Firefox) and go to that address: **http://127.0.0.1:5000**

**Congratulations! You are now looking at the Director's Dashboard.**

### Step 8: Running Your First Daily Operations (in Test Mode)

The dashboard is simple. You have one main button:

*   **"Run 1 Day of Autonomous Operations"**

1.  Make sure the switch at the top is set to **"🧪 Test Mode"**.
2.  Click the button.

**What's happening now?**
In the terminal window, you will see a live log of your AI agents at work:
*   The **CEO** will review the business and set a strategy.
*   The **Sales Agent** will find new leads.
*   The **CFO** will approve a (fake) budget for the day.
*   If you have a client, the **Creative Agent** will generate a video package.

### Step 9: Understanding the Reports

After the daily operations are complete, the dashboard will update with new information:

*   **Financial Summary:** Shows your (fake) revenue, expenses, and profit.
*   **Sales Pipeline:** Shows how many new leads were found and qualified.
*   **Agent Decisions:** A log of the key decisions your AI agents made.

Click the "Run 1 Day" button a few times to simulate a full week of business operations. Watch how the numbers change.

---

## Part 4: Going Live (When You're Ready)

Once you are comfortable with how the system works in Test Mode, you can switch to Live Mode.

### Step 10: Switching to Live Mode

1.  On the Director's Dashboard, flip the switch from "🧪 Test Mode" to **"💰 Live Mode"**.
2.  The system will now use REAL data and will be ready to process REAL payments.

### Step 11: Setting Up Real Payments (Paystack for South Africa)

To accept real money from clients in South Africa, we recommend using Paystack. It's easy to set up and integrates well.

1.  **Create a Paystack Account:** Go to `https://paystack.com` and sign up for a business account.
2.  **Get Your API Keys:** In your Paystack dashboard, find your "Secret Key".
3.  **Add to Your System:** Just like you did with the OpenAI key, you will add your Paystack Secret Key to the system so the CFO agent can process payments.
    ```bash
    # In the terminal
    set PAYSTACK_SECRET_KEY=YOUR_PAYSTACK_KEY_HERE
    ```

Now, when a client pays, the money will go directly into your Paystack account.

**You are now the Director of a fully operational, autonomous AI-powered business!**
'''
