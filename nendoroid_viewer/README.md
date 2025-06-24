# Nendoroid Viewer

This project aggregates data about Nendoroid figures and provides a web interface for browsing them.

The database stores each figure's name, description, announcement and release dates as well as all image URLs scraped from the official site.

Directories:

- `scraper/` – Python scraper that collects data from the official website.
- `backend/` – FastAPI application exposing an API backed by a PostgreSQL database.
- `frontend/` – Vue 3 + Vite web application.

Each directory contains a README with setup instructions.
