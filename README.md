# Ecommerce AI Assistant

## Overview
The Ecommerce AI Assistant is a terminal-based customer support companion that combines a curated product catalog with OpenAI-powered natural language conversations. It showcases how modern AI agents can streamline ecommerce workflows by grounding responses in real inventory data stored locally. The project highlights practical agent tooling, conversational interfaces, and lightweight data persistence—making it relevant for both technical reviewers and non-technical stakeholders evaluating AI-centric product experiences.

## Key Highlights for Recruiters & Hiring Managers
- **Real-world scenario** – Demonstrates how an AI assistant can support shoppers with catalog discovery, order lookup, and quote creation.
- **Tool-integrated AI** – Uses LangChain to bind the conversation model to deterministic database tools, preventing hallucinations and showcasing responsible AI patterns.
- **Production awareness** – Handles environment setup, database seeding, and error messaging, illustrating readiness for productization.
- **Extensible foundation** – Clear separation between conversational logic, tool functions, and data, enabling rapid iteration on features.

## Technical Summary
- **Language & Frameworks:** Python 3.10+, LangChain, LangChain OpenAI, python-dotenv, SQLite.
- **Architecture:**
  - `app.py` seeds the SQLite product catalog and runs a terminal chat loop.
  - `controllers/agent/agent.py` configures the chat model and LangChain agent.
  - `controllers/agent/tools.py` exposes structured tools for product listings, order retrieval, and quote creation.
  - `products.json` provides the starter catalog used during database seeding.
- **Data Stores:** Lightweight SQLite databases (`products.db`, `orders.db`) created on demand for demo purposes.
- **Model Integration:** Utilizes `gpt-4o` via `ChatOpenAI`, loaded with a domain-specific system prompt to enforce tone and tool usage rules.

## Getting Started
1. **Clone & Install**
   ```bash
   git clone <repo-url>
   cd ecommerce-ai-assistant
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. **Configure Environment**
   - Create a `.env` file and define your `OPENAI_API_KEY`.
3. **Seed Data & Launch Chat**
   ```bash
   python app.py
   ```
   The script automatically seeds `products.db` with entries from `products.json` before starting the interactive chat loop.

## Using the Assistant
- Type natural language questions (e.g., “What smart home devices are available?”).
- Ask for order lookups by customer name, or request a purchase quote (requires a contact name).
- Enter `exit` or `quit` to end the session.

## Project Structure
```
.
├── app.py                  # CLI entry point and database seeding
├── controllers/
│   ├── agent/
│   │   ├── agent.py        # LangChain agent configuration
│   │   └── tools.py        # Database-backed tool implementations
│   └── utils.py            # Utility module (reserved for future helpers)
├── products.json           # Sample catalog used for seeding
└── requirements.txt        # Python dependencies
```

## Extending the Demo
- Swap the CLI for a web or messaging UI to meet different customer touchpoints.
- Add authentication, richer order workflows, or payment integrations for end-to-end commerce flows.
- Expand tooling to cover inventory updates, shipping estimates, or personalized recommendations.

## Contributing & Feedback
Pull requests are welcome! Please fork the repository, create a feature branch, and open a PR describing your updates. For questions or suggestions, feel free to reach out via issues.

