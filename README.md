# 🎬 StreamVault — Netflix OTT Platform Prototype & Frontend

A premium, Netflix-style frontend and prototype application designed for DBMS academic and portfolio projects. Built with **Python (Streamlit)** and backed by an embedded relational **SQLite database (`netflix.db`)** that perfectly implements the provided Entity-Relationship (ER) diagram.

---

## 🗃️ ER Diagram Schema & Mapping

All 11 entities, attributes, primary keys (PK), foreign keys (FK), and 3 junction tables from the ER diagram are fully implemented:

```
                ┌────────────────┐
                │    SUBS_PLAN   │
                │   (PLAN_ID)    │
                └───────┬────────┘
                        │ 1:M
                ┌───────┴────────┐
                │  SUBSCRIPTION  │
                │   (SUBS_ID)    │
                └───────┬────────┘
                        │ FK
┌──────────┐    ┌───────┴────────┐    ┌──────────────┐
│ PROFILES │────│     USER       │────│   PAYMENTS   │
│(PROF_ID) │ 1:M│  (USER_ID)    │ 1:M│ (PAYMENT_ID) │
└──────────┘    └──┬─────────┬──┘    └──────────────┘
                   │         │
              1:M  │         │  1:M
        ┌──────────┘         └──────────┐
┌───────┴────────┐           ┌──────────┴─────┐
│ REVIEW_RATING  │           │  WATCH_HISTORY │
│  (REVIEW_ID)   │           │  (HISTORY_ID)  │
└───────┬────────┘           └──────────┬─────┘
        │ FK                            │ FK
┌───────┴────────────────────────────────┴──────┐
│                   CONTENT                     │
│                (CONTENT_ID)                   │
└──────┬──────────────┬───────────────┬─────────┘
       │ M:M          │ M:M           │ M:M
┌──────┴─────┐ ┌──────┴──────┐ ┌──────┴──────┐
│   GENRES   │ │  DIRECTORS  │ │   ACTORS    │
│ (GENRE_ID) │ │(DIRECTOR_ID)│ │ (ACTOR_ID)  │
└────────────┘ └─────────────┘ └─────────────┘
```

### Entity Table Specification

| Entity | Primary Key | Foreign Keys | Attributes |
|--------|-------------|--------------|------------|
| **`USER`** | `user_id` | — | `name`, `email`, `password`, `phone`, `reg_date` |
| **`PROFILES`** | `profile_id` | `user_id` → `USER` | `profile_name`, `profile_type` ('Adult', 'Kids') |
| **`SUBS_PLAN`** | `plan_id` | — | `plan_name`, `price`, `duration_mon`, `max_screen`, `video_qual` |
| **`SUBSCRIPTION`** | `subs_id` | `user_id` → `USER`<br>`plan_id` → `SUBS_PLAN` | `start_date`, `end_date`, `status` ('Active', 'Expired', 'Cancelled') |
| **`PAYMENTS`** | `payment_id` | `user_id` → `USER`<br>`subs_id` → `SUBSCRIPTION` | `amount`, `pay_date`, `pay_method`, `status` ('Success', 'Failed') |
| **`CONTENT`** | `content_id` | — | `title`, `description`, `duration`, `language`, `type`, `release_year`, `maturity`, `rating`, `poster_url`, `backdrop_url` |
| **`GENRES`** | `genre_id` | — | `genre_name` |
| **`DIRECTORS`** | `director_id` | — | `director_name` |
| **`ACTORS`** | `actor_id` | — | `actor_name` |
| **`CONTENT_GENRES`** | `(content_id, genre_id)` | `content_id` → `CONTENT`<br>`genre_id` → `GENRES` | M:M relationship |
| **`CONTENT_DIRECTORS`** | `(content_id, director_id)` | `content_id` → `CONTENT`<br>`director_id` → `DIRECTORS` | M:M relationship |
| **`CONTENT_ACTORS`** | `(content_id, actor_id)` | `content_id` → `CONTENT`<br>`actor_id` → `ACTORS` | M:M relationship |
| **`REVIEW_RATING`** | `review_id` | `content_id` → `CONTENT`<br>`user_id` → `USER` | `rating` (1–10), `review_text`, `review_date` |
| **`WATCH_HISTORY`** | `history_id` | `content_id` → `CONTENT`<br>`user_id` → `USER` | `watch_date`, `progress_min`, `completed` (0/1) |

---

## 🚀 How to Run

### Method 1: One-Click (Windows)
Double-click `run.bat` or run:
```powershell
.\run.bat
```

### Method 2: PowerShell
```powershell
.\run.ps1
```

### Method 3: Direct Streamlit CLI
```bash
cd netflix-frontend
.venv\Scripts\streamlit.exe run app.py
```
Open **[http://localhost:8501](http://localhost:8501)** in your browser.

---

## 🎨 Interactive Features

1. **Exact Netflix Login Screen (Python & Streamlit)**
   - **Authentic Backdrop**: Full-bleed darkened movie grid collage with radial/linear dark vignette gradients.
   - **Official Red Logo**: Vector SVG wordmark in `#E50914` curved arc styling.
   - **Translucent Card**: `rgba(0, 0, 0, 0.78)` box with Netflix Sans typography and styling.
   - **Authentication**: Checks credentials against the `USER` entity table, supports password checks, and includes a **Sign Up** mode for registering new user records.
   - **⚡ Quick Demo Login**: Dropdown with 10 sample database users (Aarav, Priya, Rohan, etc.) for instant one-click evaluation without typing.
   - **Classic Netflix Footer**: Help lines, terms, privacy, cookie preferences, and language toggles.

2. **Iconic "Who's Watching?" Profile Screen**
   - Profile avatar tiles (Adult/Kids) pulled directly from the `PROFILES` database table.
   - Scale animations on hover.
   - "+ Add Profile" tile to create custom profiles on the fly.
   - Profile gating before entering the main streaming platform.

3. **User & Profile Management**
   - Real-time active subscription plan, allowed screen count, and video quality in the sidebar.
   - "🔄 Switch Profile" and "🚪 Sign Out" buttons in the navigation sidebar.

2. **Home Page**
   - Featured dynamic Hero banner with backdrop, rating, and metadata.
   - Platform Overview KPI cards (Total Users, Titles, Genres, Subscriptions, Reviews).
   - Horizontal carousels for Trending Titles, 2024 New Releases, and TV Series.

3. **Browse Content Catalogue**
   - Multi-parameter filters: Genre, Type (Movie/Series), Language, and Sorting.
   - Expandable title inspector displaying Cast, Director, Description, and Reviews.
   - **▶️ Watch Simulator**: Interactive progress slider that updates `WATCH_HISTORY` in real time.
   - **⭐ Rate & Review Form**: Live rating (1–10 stars) and feedback submission into `REVIEW_RATING`.

4. **User Profiles**
   - Profile card with avatar colors and member registration details.
   - Profile cards list with Adult/Kids icons.
   - **➕ Create Profile Form**: Add custom profiles under the active account.

5. **Subscription Plans & ACID Payment Gateway**
   - Comparison cards for Mobile, Basic, Standard, Premium, Student, and Family plans.
   - Full attribute comparison table.
   - **⚡ Transaction Checkout Simulator**: Select plan, choose payment method (UPI, Card, Net Banking), and process simulated payment. Supports testing transaction failure/rollback.

6. **Payments & Watch History**
   - Payment timeline and method breakdown charts (Plotly).
   - Detailed history tables with status indicators.
   - Watch history progress bars showing minutes watched vs. total duration.

7. **Reviews & Ratings**
   - Rating distribution bar chart (1 to 10 stars).
   - Global review submission form.
   - Formatted review cards with reviewer names and timestamps.

8. **Analytics Dashboard**
   - Content Analytics: Genre breakdown donut chart, Movies vs. Series split, rating comparisons.
   - User Analytics: Monthly user registrations, profiles-per-user chart, most active watchers.
   - Subscription Analytics: Status distribution and plan popularity.
   - Revenue Analytics: Revenue by payment method and monthly revenue curve.

9. **Database Schema & Live SQL Console**
   - Interactive visual ER diagram cards highlighting PKs (🔑) and FKs (🔗).
   - Live SQLite table inspector for all 14 tables.
   - **⚡ Interactive SQL Sandbox**: Execute pre-crafted SQL queries (multi-table JOINs, aggregations, subqueries) or custom queries with execution metrics.
   - **🔄 Reset Database**: One-click reset to clean initial sample state anytime.
