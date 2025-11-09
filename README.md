# ShopAlert
This project was created for UB Hacking 2025. 

## Project Setup

### Prerequisites
- [pnpm](https://pnpm.io/) (Node.js package manager)
- [Python 3.11+](https://www.python.org/)
- [Docker](https://www.docker.com/) (for Postgres database)

### Getting Started

1. **Start Postgres**
   ```bash
   docker compose up db -d
   ```
   Database runs at localhost:5432

2. **Backend setup (from `api/` folder)**
   ```bash
   cd api
   # Copy and configure environment
   cp .env.example .env
   
   # Create virtual environment and install dependencies
   python -m venv .venv
   # Windows:
   .\.venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate
   
   pip install --upgrade pip
   pip install -r requirements.txt
   
   # Run migrations
   pnpm migrate
   
   # Start dev server
   pnpm dev
   ```
   Backend runs at http://localhost:8000/

3. **Frontend setup (from `web/` folder)**
   ```bash
   cd web
   
   pnpm install
   pnpm dev
   ```
   Frontend runs at http://localhost:5173/

### Cleanup

1. **Clean up Postgres**
   ```bash
   docker compose down -v
   ```

2. **Clean up api/web**
   Interrupt the active processes using CTRL+C (Windows) or Command+. (macOS)