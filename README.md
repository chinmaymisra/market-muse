# 📘 MarketMuse Codebase Documentation – Technical Bible

This guide provides a comprehensive, production-grade walkthrough of the **MarketMuse** full-stack application. It explains the purpose and interrelation of each folder, file, and function across the backend and frontend.

---

## 📁 Backend – FastAPI

The backend is implemented using **FastAPI**, located under `backend/app/`, and follows a modular structure with separation of concerns.

### Folder Structure

```
backend/app/
├── routers/        # API route handlers (users, stocks, watchlist)
├── models/         # SQLAlchemy ORM models
├── schemas/        # Pydantic response/request models
├── services/       # Business logic & external API integration
├── auth.py         # Firebase authentication logic
├── database.py     # SQLAlchemy DB connection setup
└── main.py         # Application entrypoint
```

---

### 🔐 `auth.py`

**Purpose:** Securely authenticates users using Firebase and retrieves (or creates) corresponding user records in the DB.

**Key Functions:**
- `get_db()` – Provides a database session as a dependency.
- `verify_token()` – Verifies Firebase ID tokens using Admin SDK.
- `get_current_user()` – Fetches or creates the user from DB.
- `require_admin()` – Validates admin access via `is_admin` flag.

**Used By:**
- `users.py`, `watchlist.py`, `stocks.py` routes

---

### 💾 `database.py`

**Purpose:** Sets up the SQLAlchemy engine and base.

- `engine` – Uses `DATABASE_URL` from `.env`
- `SessionLocal()` – DB session factory
- `Base` – Declarative base class for models

---

### 🚦 `main.py`

**Purpose:** Entry point for the FastAPI backend app.

- Registers routers: `stocks`, `users`, `watchlist`
- Adds CORS support for frontend integration
- Uses `lifespan()` event to create DB tables
- Logs incoming requests and status codes

---

### 🧱 `models/`

**Purpose:** Database schema via SQLAlchemy models.

- `user.py` – `uid`, `email`, `name`, `picture`, `is_admin`
- `stock_cache.py` – `symbol`, `price`, `pe_ratio`, `history`, etc.
- `watchlist.py` – User-stock mapping (composite key: `user_id`, `symbol`)

---

### 🧩 `routers/`

**Purpose:** Groups related endpoints.

- `stocks.py`  
  `GET /stocks` – Returns cached stock data

- `users.py`  
  `GET /users/me` – Registers and returns user info  
  Flags admins using `ADMIN_EMAILS` in `.env`

- `watchlist.py`  
  `POST /watchlist/add/{symbol}` – Add to watchlist  
  `POST /watchlist/remove/{symbol}` – Remove from watchlist  
  `GET /watchlist/` – Get all watched stocks

---

### 🧠 `services/`

**Purpose:** Core logic for interacting with APIs and DB.

- `finnhub_service.py`  
  `get_stock_info(symbol)` – Fetches quote, metrics, and profile

- `stock_service.py`  
  `get_stock_data(symbols, db)` – Updates DB cache using `get_stock_info()`

---

### ⚙️ Scheduled Scripts

- `refresh_all_stocks.py` – Batch updates all symbols (one-time/ad hoc)
- `refresh_stock_cache.py` – Refreshes one symbol per minute (rate-limited)
- `test_finnhub_fetch.py` – Manual test for fetching stock data

---

## 🎨 Frontend – React + Vite + Tailwind

The frontend is built with **Vite**, **React**, and **TailwindCSS**, and lives in the `frontend/` directory.

### Key Files

- `App.tsx`  
  Core logic: data fetching, search, watchlist filtering, theming  
  Wraps everything with `AuthProvider` and `WatchlistProvider`

- `components/StockCard.tsx`  
  Shows stock details, sparkline chart, badges, and watchlist toggle

- `components/LoginButton.tsx`  
  Uses `signInWithPopup()` and sends token to `/users/me`

- `pages/LoginPage.tsx`  
  Login UI

- `pages/WatchlistTab.tsx`  
  Displays only stocks in user's watchlist (client-side filtered)

---

### 🧩 Contexts

- `context/AuthContext.tsx`  
  Tracks auth state using `onAuthStateChanged()`  
  Exposes user object and loading state

- `context/WatchlistContext.tsx`  
  Fetches and stores user’s watchlist  
  Handles add/remove API calls and state updates

---

## 🔄 System Flow Overview

### 🔐 Authentication Flow
1. User logs in via Firebase (Google)
2. Token is sent to `/users/me`
3. User is created/fetched from DB
4. Admins identified via `ADMIN_EMAILS` in `.env`

---

### 📊 Stock Fetching Flow
1. `App.tsx` fetches `/stocks` after login
2. Backend reads from `stock_cache` (auto-refreshed in background)
3. Frontend renders data using Recharts

---

### ⭐ Watchlist Flow
1. `+` button toggles watchlist status via backend
2. `WatchlistContext` updates local state
3. `WatchlistTab.tsx` filters stocks by current user’s watchlist

---

## 🧩 Technologies Used

- **Backend:** FastAPI, SQLAlchemy, Alembic, PostgreSQL, Firebase Auth
- **Frontend:** React, Vite, TailwindCSS, Firebase SDK, Recharts
- **Deployment:** Render, GitHub Actions, Namecheap (DNS + SSL)
- **APIs:** Finnhub

---
