# FinSage Frontend

This is the frontend for **FinSage – AI Money Mentor**, built with React and Vite.

## Features

- Modern React UI for financial planning and analysis
- Interactive dashboards, agent panels, and chat
- Connects to FastAPI backend via `/api` proxy

## Requirements

- Node.js 18+
- npm 9+

## Setup

1. **Install dependencies:**
   ```sh
   cd frontend
   npm install
   ```
2. **Run the development server:**

   ```sh
   npm run dev
   ```

   - App runs at [http://localhost:3000](http://localhost:3000)
   - API requests are proxied to [http://localhost:8000](http://localhost:8000)

3. **Build for production:**
   ```sh
   npm run build
   ```

   - Output in `frontend/dist`

## Project Structure

- `src/` – React components, context, utils, styles
- `api/` – API client for backend
- `components/` – UI modules (AgentPanel, Chat, Dashboard, etc.)
- `styles/` – Global CSS

## Environment Variables

- `.env` (optional):
  - `VITE_API_URL` (default: `http://localhost:8000`)

## License

MIT
