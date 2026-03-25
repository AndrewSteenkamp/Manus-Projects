# AI-Powered UGC Advertising Agency

This repository contains the complete source code and deployment instructions for a fully autonomous, AI-powered User-Generated Content (UGC) advertising agency. The system is designed to be deployed as a production-ready application, managed by a team of world-class AI agents who handle all aspects of the business, from client acquisition to content creation and financial management.

## 🚀 Features

- **Autonomous Operation:** The entire agency is run by a team of specialized AI agents.
- **World-Class Agent Team:** Includes a CEO, CFO, COO, CTO, and dedicated teams for Sales, Marketing, Creative, and Customer Success.
- **End-to-End Automation:** Automates lead generation, client onboarding, UGC video creation, campaign management, and billing.
- **Scalable Architecture:** Built with a microservices-based approach to handle a growing client base.
- **Cost-Effective AI:** Utilizes a multi-provider AI helper to switch between free and low-cost AI models, minimizing operational expenses.
- **One-Click Deployment:** Containerized with Docker for easy, repeatable deployment on any system.
- **Comprehensive Dashboard:** A web-based interface for high-level oversight and monitoring of the agency's performance.

## 📂 Project Structure

```
/ai-ugc-agency
├── agents/                  # Core AI agent implementations
│   ├── ceo_agent.py
│   ├── cfo_agent.py
│   ├── coo_agent.py
│   ├── sales_agent.py
│   ├── marketing_agent.py
│   ├── creative_agent.py
│   └── ... (other agents)
├── services/                # Business logic and core services
│   ├── lead_generation.py
│   ├── video_generator.py
│   ├── payment_processor.py
│   └── client_manager.py
├── web/                     # Web interface and API
│   ├── app.py               # Main Flask application
│   ├── templates/           # HTML templates for the dashboard
│   └── static/              # CSS and JavaScript files
├── tests/                   # Unit and integration tests
│   ├── test_agents.py
│   └── test_services.py
├── .env.example             # Example environment file for API keys
├── Dockerfile               # Docker configuration for the main application
├── docker-compose.yml       # Docker Compose for multi-container setup
├── requirements.txt         # Python package dependencies
└── README.md                # This file
```

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **AI Models:** Hugging Face (Free), Google Gemini (Free), Anthropic Claude (Low-cost)
- **Database:** SQLite (for simplicity, can be swapped for PostgreSQL)
- **Containerization:** Docker, Docker Compose
- **Frontend:** HTML, CSS, JavaScript (via Flask templates)

## 📖 Deployment

This project is designed for one-click deployment using Docker. Full instructions are provided in the `DEPLOYMENT.md` file.

1.  **Clone the repository.**
2.  **Configure API keys** in the `.env` file.
3.  **Run `docker-compose up --build`**.

Your autonomous agency will be live and accessible via `http://localhost:5000`.

---
*This project was developed by Manus AI to provide a complete, deployable, and autonomous business system.*
