"""
StreamVault - Netflix OTT Relational Database Platform
Python Streamlit Frontend backed by SQLite (netflix.db)
Full compliance with DPDP Act 2023, zero gradients, zero pill buttons, zero emojis,
authentic reviews and copy, accessible high-contrast UI, security controls.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import re

# Database and seed layer
import data.database as db
from data.sample_data import (
    CONTENT_GENRES, CONTENT_ACTORS, CONTENT_DIRECTORS
)

# Authentication module
import importlib
import netflix_auth
importlib.reload(netflix_auth)
from netflix_auth import render_netflix_login, render_whos_watching, NETFLIX_LOGO_SVG, validate_email_address

# Legal policies and business details
import legal_policies as legal

# ================================================================
# ENTITY CACHE FROM SQLITE DATABASE
# ================================================================
USERS = db.get_all_users()
CONTENT = db.get_all_content()
GENRES = db.get_all_genres()
SUBS_PLANS = db.get_all_plans()
PROFILES = db.get_table_df("PROFILES").to_dict(orient="records")
SUBSCRIPTIONS = db.get_table_df("SUBSCRIPTION").to_dict(orient="records")
PAYMENTS = db.get_table_df("PAYMENTS").to_dict(orient="records")
DIRECTORS = db.get_table_df("DIRECTORS").to_dict(orient="records")
ACTORS = db.get_table_df("ACTORS").to_dict(orient="records")
REVIEW_RATINGS = db.get_all_reviews()
WATCH_HISTORY = db.get_table_df("WATCH_HISTORY").to_dict(orient="records")

get_content_genres = db.get_content_genres
get_content_actors = db.get_content_actors
get_content_director = db.get_content_director
get_user_profiles = db.get_user_profiles
get_user_subscription = db.get_user_subscription
get_plan_details = db.get_plan_details
get_content_reviews = db.get_content_reviews
get_user_watch_history = db.get_user_watch_history
get_user_payments = db.get_user_payments

# ================================================================
# PAGE CONFIGURATION & METADATA
# ================================================================
is_auth = "authenticated_user_id" in st.session_state and st.session_state.authenticated_user_id is not None
is_prof = "active_profile_id" in st.session_state and st.session_state.active_profile_id is not None

st.set_page_config(
    page_title="StreamVault - Netflix OTT Relational Database Platform",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enforce HTTPS, CSP, Meta Tags, and Accessibility Viewport
st.markdown("""
<head>
    <meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests">
    <meta name="description" content="StreamVault is an academic relational DBMS platform for OTT streaming services implementing 11 ER entities and ACID transaction handling.">
    <meta name="author" content="StreamVault Media Technologies Private Limited">
    <meta property="og:title" content="StreamVault - OTT DBMS Platform">
    <meta property="og:description" content="Relational database implementation of an OTT streaming platform conforming to an 11-entity ER diagram.">
    <meta property="og:type" content="website">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' fill='%23141414'/><path d='M25 20h15l35 60h-15z' fill='%23e50914'/><path d='M25 20h15v60h-15z' fill='%23b80710'/><path d='M60 20h15v60h-15z' fill='%23e50914'/></svg>">
</head>
""", unsafe_allow_html=True)

# Authentication & Profile Selection Gates
if not is_auth:
    render_netflix_login()
    st.stop()

current_user = db.get_user_by_id(st.session_state.authenticated_user_id)
if not current_user:
    st.session_state.authenticated_user_id = None
    render_netflix_login()
    st.stop()

if not is_prof:
    render_whos_watching(current_user)
    st.stop()

current_profiles = db.get_user_profiles(current_user["user_id"])
current_profile = next((p for p in current_profiles if p["profile_id"] == st.session_state.active_profile_id), None)
if not current_profile and current_profiles:
    current_profile = current_profiles[0]
    st.session_state.active_profile_id = current_profile["profile_id"]
elif not current_profile:
    current_profile = {"profile_name": current_user["name"].split()[0], "profile_type": "Adult", "profile_id": 0}

# ================================================================
# SOLID WCAG AA STYLESHEET (NO GRADIENTS, NO PILL BUTTONS)
# ================================================================
st.markdown("""
<style>
    /* -------- Base System Typography & Contrast Palette -------- */
    :root {
        --bg-main: #141414;
        --bg-surface: #1f1f1f;
        --bg-surface-hover: #292929;
        --bg-alt: #262626;
        --border-color: #333333;
        --border-focus: #ffffff;
        --accent-red: #e50914;
        --accent-red-hover: #b80710;
        --text-white: #ffffff;
        --text-secondary: #b3b3b3;
        --text-muted: #888888;
        --radius-standard: 4px;
    }

    body, .stApp {
        background-color: var(--bg-main) !important;
        background-image: none !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
        color: var(--text-white) !important;
    }

    /* Accessibility focus rings */
    *:focus-visible {
        outline: 2px solid var(--border-focus) !important;
        outline-offset: 2px !important;
    }

    /* Full-width container */
    .main .block-container {
        padding-top: 0.5rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 1440px !important;
    }

    /* Hide default Streamlit sidebar */
    section[data-testid="stSidebar"], div[data-testid="collapsedControl"] {
        display: none !important;
    }

    /* Hide Streamlit default branding */
    #MainMenu, footer, header {
        visibility: hidden !important;
    }

    /* -------- Sticky Top Bar (Matte Solid) -------- */
    .top-bar-container {
        position: sticky;
        top: 0;
        z-index: 999;
        background-color: #181818 !important;
        background-image: none !important;
        border-bottom: 1px solid var(--border-color) !important;
        padding: 12px 20px !important;
        margin: -0.5rem -2rem 1.5rem -2rem !important;
    }

    /* Navigation Tabs: Square Rectangular Buttons */
    div[data-testid="stPills"] {
        display: flex !important;
        align-items: center !important;
        gap: 4px !important;
        flex-wrap: wrap !important;
    }
    div[data-testid="stPills"] button,
    div[data-testid="stPills"] [data-baseweb="tag"],
    div[data-testid="stPills"] div[role="button"] {
        background-color: #242424 !important;
        background-image: none !important;
        color: #cccccc !important;
        border: 1px solid #3a3a3a !important;
        border-radius: 4px !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        padding: 7px 12px !important;
        transition: background-color 0.15s ease, color 0.15s ease !important;
    }
    div[data-testid="stPills"] button:hover {
        background-color: #333333 !important;
        color: #ffffff !important;
        border-color: #555555 !important;
    }
    div[data-testid="stPills"] button[aria-pressed="true"],
    div[data-testid="stPills"] button[data-checked="true"],
    div[data-testid="stPills"] button[aria-selected="true"] {
        background-color: var(--accent-red) !important;
        background-image: none !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border: 1px solid var(--accent-red) !important;
        box-shadow: none !important;
    }

    /* Standard Buttons */
    button {
        border-radius: 4px !important;
        font-family: inherit !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        transition: background-color 0.15s ease !important;
    }
    button[kind="primary"] {
        background-color: var(--accent-red) !important;
        background-image: none !important;
        color: #ffffff !important;
        border: 1px solid var(--accent-red) !important;
    }
    button[kind="primary"]:hover {
        background-color: var(--accent-red-hover) !important;
        border-color: var(--accent-red-hover) !important;
    }
    button[kind="secondary"] {
        background-color: #2b2b2b !important;
        background-image: none !important;
        color: #ffffff !important;
        border: 1px solid #444444 !important;
    }
    button[kind="secondary"]:hover {
        background-color: #383838 !important;
        border-color: #666666 !important;
    }

    /* Top Bar Action Buttons */
    .nav-action-btn button {
        background-color: #2b2b2b !important;
        color: #e5e5e5 !important;
        border: 1px solid #444444 !important;
        border-radius: 4px !important;
        font-size: 12px !important;
        height: 36px !important;
        padding: 4px 10px !important;
        white-space: nowrap !important;
    }
    .nav-action-btn button:hover {
        background-color: #3a3a3a !important;
        border-color: #777777 !important;
    }

    /* Content Cards (Solid surface, 4px radius) */
    .content-card {
        background-color: var(--bg-surface);
        background-image: none;
        border: 1px solid var(--border-color);
        border-radius: 4px;
        overflow: hidden;
        margin-bottom: 1rem;
    }
    .content-card:hover {
        border-color: #555555;
    }
    .content-card img {
        width: 100%;
        height: 270px;
        object-fit: cover;
        display: block;
    }
    .card-body {
        padding: 12px 14px;
    }
    .card-title {
        font-size: 15px;
        font-weight: 700;
        color: #ffffff;
        margin: 0 0 4px 0;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .card-metadata {
        font-size: 12px;
        color: var(--text-secondary);
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 6px;
    }
    .card-rating-badge {
        font-weight: 700;
        color: #ffffff;
        background-color: #2e2e2e;
        border: 1px solid #444444;
        padding: 1px 6px;
        border-radius: 2px;
        font-size: 11px;
    }
    .tag-badge {
        display: inline-block;
        background-color: #262626;
        color: #cccccc;
        border: 1px solid #3d3d3d;
        border-radius: 2px;
        padding: 1px 6px;
        font-size: 11px;
        margin-right: 4px;
    }

    /* Hero Banner: Flat overlay */
    .hero-container {
        position: relative;
        background-color: #000000;
        border: 1px solid var(--border-color);
        border-radius: 4px;
        overflow: hidden;
        margin-bottom: 24px;
    }
    .hero-container img {
        width: 100%;
        height: 380px;
        object-fit: cover;
        opacity: 0.45;
        display: block;
    }
    .hero-content {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 24px 28px;
        background-color: rgba(20, 20, 20, 0.92);
        border-top: 1px solid #2a2a2a;
    }
    .hero-title-text {
        font-size: 32px;
        font-weight: 800;
        color: #ffffff;
        margin: 0 0 8px 0;
    }
    .hero-desc-text {
        font-size: 14px;
        color: #cccccc;
        max-width: 750px;
        line-height: 1.5;
        margin: 0 0 12px 0;
    }

    /* Section Headers */
    .section-title {
        font-size: 20px;
        font-weight: 700;
        color: #ffffff;
        margin: 24px 0 14px 0;
        border-left: 3px solid var(--accent-red);
        padding-left: 10px;
    }

    /* Stat Inventory Box */
    .inventory-stat-card {
        background-color: var(--bg-surface);
        border: 1px solid var(--border-color);
        border-radius: 4px;
        padding: 14px;
        text-align: center;
    }
    .inventory-stat-num {
        font-size: 26px;
        font-weight: 800;
        color: #ffffff;
        margin: 0;
    }
    .inventory-stat-lbl {
        font-size: 12px;
        color: var(--text-secondary);
        margin: 4px 0 0 0;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    /* Cookie Banner */
    .cookie-banner-box {
        background-color: #1c1c1c;
        border: 1px solid #3d3d3d;
        border-radius: 4px;
        padding: 14px 18px;
        margin-bottom: 18px;
    }
    .cookie-banner-title {
        font-weight: 700;
        font-size: 13px;
        color: #ffffff;
        display: block;
        margin-bottom: 4px;
    }
    .cookie-banner-text {
        font-size: 12px;
        color: #b3b3b3;
        line-height: 1.5;
        margin: 0;
    }

    /* Modal Dialog Overrides */
    div[data-testid="stDialog"] > div:first-child,
    div[data-testid="stDialog"] [role="dialog"],
    div[role="dialog"] {
        background-color: #181818 !important;
        background-image: none !important;
        border: 1px solid #383838 !important;
        border-radius: 4px !important;
        box-shadow: 0 16px 40px rgba(0, 0, 0, 0.9) !important;
        color: #ffffff !important;
    }
    div[data-testid="stDialog"] header {
        background: transparent !important;
        color: #ffffff !important;
        border-bottom: 1px solid #2a2a2a !important;
    }
    div[data-testid="stDialog"] h1,
    div[data-testid="stDialog"] h2,
    div[data-testid="stDialog"] h3,
    div[data-testid="stDialog"] p,
    div[data-testid="stDialog"] label,
    div[data-testid="stDialog"] span {
        color: #e5e5e5;
    }
    div[data-testid="stDialog"] button[aria-label="Close"] {
        border-radius: 2px !important;
        color: #ffffff !important;
    }

    /* Mobile Responsive Rules */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        .top-bar-container {
            margin: -0.5rem -1rem 1rem -1rem !important;
            padding: 10px 12px !important;
        }
        .hero-title-text {
            font-size: 24px !important;
        }
        .content-card img {
            height: 220px !important;
        }
    }
</style>
""", unsafe_allow_html=True)


# ================================================================
# MODAL DIALOG: MOVIE DETAILS AND RELATIONAL MAPPING
# ================================================================
@st.dialog("Catalog Title Details and Relational Record", width="large")
def show_movie_detail_dialog(content_id):
    item = db.get_content_by_id(content_id)
    if not item:
        st.error("Title not found in database catalog.")
        return

    genres_full = db.get_content_genres_full(content_id)
    actors_full = db.get_content_actors_full(content_id)
    director_rec = db.get_content_director_full(content_id)
    reviews = db.get_content_reviews(content_id)
    user_hist = [h for h in db.get_user_watch_history(current_user["user_id"]) if h["content_id"] == content_id]
    current_progress = user_hist[0]["progress_min"] if user_hist else 0
    is_completed = user_hist[0]["completed"] if user_hist else False
    raw_mappings = db.get_content_raw_mapping(content_id)

    genre_names = [g["genre_name"] for g in genres_full]
    actor_names = [a["actor_name"] for a in actors_full]

    # Banner with accessible alt text
    st.markdown(f"""
    <div style="position:relative; border-radius:4px; overflow:hidden; margin-bottom:16px; border:1px solid #333333; background-color:#000000;">
        <img src="{item['backdrop_url']}" alt="Backdrop still for {item['title']}" style="width:100%; height:240px; object-fit:cover; opacity:0.55; display:block;">
        <div style="position:absolute; bottom:0; left:0; right:0; padding:16px 20px; background-color:rgba(18,18,18,0.95); border-top:1px solid #282828;">
            <h2 style="font-size:24px; font-weight:700; margin:0 0 6px 0; color:#ffffff;">{item['title']}</h2>
            <div style="display:flex; gap:6px; align-items:center; flex-wrap:wrap;">
                <span class="card-rating-badge">Rating: {item['rating']} / 10</span>
                <span class="tag-badge">{item['type']}</span>
                <span class="tag-badge">Rated {item['maturity']}</span>
                <span style="font-size:12px; color:#cccccc;">{item['duration']} min | {item['release_year']} | {item['language']}</span>
                <span style="font-size:11px; color:#888888; margin-left:auto;">PK: content_id = {item['content_id']}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_m1, col_m2 = st.columns([2, 1])
    with col_m1:
        st.markdown(f"**Synopsis:**\n{item['description']}")
        st.markdown(f"**Genres (GENRES via CONTENT_GENRES):** {', '.join(genre_names) if genre_names else 'Uncategorized'}")
        st.markdown(f"**Director (DIRECTORS via CONTENT_DIRECTORS):** {director_rec['director_name']} (director_id: {director_rec['director_id']})")
        st.markdown(f"**Cast (ACTORS via CONTENT_ACTORS):** {', '.join(actor_names) if actor_names else 'Uncredited'}")
    with col_m2:
        st.markdown(f"""
        <div style="background-color:#202020; padding:14px; border-radius:4px; border:1px solid #333333;">
            <div style="font-size:11px; color:#aaaaaa; font-weight:700; text-transform:uppercase; margin-bottom:8px;">CONTENT Table Record</div>
            <div style="font-size:13px; color:#cccccc; margin-bottom:4px;"><strong>Type:</strong> {item['type']}</div>
            <div style="font-size:13px; color:#cccccc; margin-bottom:4px;"><strong>Duration:</strong> {item['duration']} minutes</div>
            <div style="font-size:13px; color:#cccccc; margin-bottom:4px;"><strong>Maturity:</strong> {item['maturity']}</div>
            <div style="font-size:13px; color:#cccccc; margin-bottom:4px;"><strong>Language:</strong> {item['language']}</div>
            <div style="font-size:13px; color:#cccccc; margin-bottom:4px;"><strong>Release Year:</strong> {item['release_year']}</div>
            <div style="font-size:13px; color:#cccccc;"><strong>Catalog Rating:</strong> {item['rating']} / 10</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='border:none; border-top:1px solid #2e2e2e; margin:16px 0;'>", unsafe_allow_html=True)

    # Watch Simulator (WATCH_HISTORY entity)
    st.markdown("#### Playback Simulation (WATCH_HISTORY Entity)")
    st.caption("Records playback progress for the active user account, fulfilling the PLAYED relationship.")
    if user_hist:
        pct = min(100, int((user_hist[0]['progress_min'] / item['duration']) * 100)) if item['duration'] > 0 else 0
        status_txt = "Completed" if user_hist[0]['completed'] else "In Progress"
        st.markdown(f"**Current Status:** {status_txt} | Logged: `{user_hist[0]['progress_min']} / {item['duration']} minutes` ({pct}%) | Last Recorded: `{user_hist[0]['watch_date']}`")
    else:
        st.markdown("**Current Status:** Not yet recorded in user watch history.")

    col_w1, col_w2 = st.columns([3, 1])
    with col_w1:
        new_progress = st.slider(
            "Playback Minutes",
            min_value=0, max_value=int(item["duration"]),
            value=min(int(current_progress), int(item["duration"])),
            key=f"modal_watch_slider_{item['content_id']}"
        )
    with col_w2:
        mark_completed = st.checkbox(
            "Mark as Completed",
            value=is_completed,
            key=f"modal_watch_comp_{item['content_id']}"
        )

    if st.button("Save Watch Progress", key=f"modal_save_watch_{item['content_id']}", type="primary"):
        final_prog = item["duration"] if mark_completed else new_progress
        succ, msg = db.log_watch_progress(item["content_id"], current_user["user_id"], final_prog, mark_completed)
        if succ:
            st.success(f"WATCH_HISTORY updated: User {current_user['user_id']}, Content {item['content_id']}, Progress {final_prog} min.")
            st.rerun()
        else:
            st.error(f"Error saving progress: {msg}")

    st.markdown("<hr style='border:none; border-top:1px solid #2e2e2e; margin:16px 0;'>", unsafe_allow_html=True)

    # Reviews and Ratings (REVIEW_RATING entity)
    st.markdown(f"#### Verified User Reviews (REVIEW_RATING Entity: {len(reviews)} Entries)")
    st.caption("Fulfills RATED_ON relationship. Submissions update the catalog rating atomically via SQLite transaction.")

    with st.expander("Submit a Review for this Title", expanded=False):
        with st.form(key=f"modal_rev_form_{item['content_id']}"):
            rev_stars = st.slider("Rating Score (1 to 10)", min_value=1, max_value=10, value=8)
            rev_body = st.text_area("Review Assessment", placeholder="Provide factual evaluation of script, acting, or technical merits...")
            btn_sub_rev = st.form_submit_button("Submit Review", type="primary")
            if btn_sub_rev:
                if not rev_body.strip():
                    st.warning("Please provide review text.")
                else:
                    succ, msg = db.add_user_review(item["content_id"], current_user["user_id"], rev_stars, rev_body.strip())
                    if succ:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(f"Submission error: {msg}")

    if reviews:
        for r in reviews:
            st.markdown(f"""
            <div style="background-color:#202020; border:1px solid #2e2e2e; border-radius:4px; padding:10px 14px; margin-bottom:8px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-weight:600; color:#ffffff;">{r['user_name']}</span>
                    <span class="card-rating-badge">Rating: {r['rating']} / 10</span>
                </div>
                <p style="color:#cccccc; margin:6px 0 4px 0; font-size:13px; line-height:1.45;">"{r['review_text']}"</p>
                <div style="color:#777777; font-size:11px;">Date: {r['review_date']} | Review ID: {r['review_id']} | User ID: {r['user_id']}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No reviews recorded yet for this title.")

    # ER Relational Inspector
    with st.expander("ER Diagram Relational Mappings (Raw SQL Record)", expanded=False):
        st.markdown("**1. Raw CONTENT Row:**")
        st.json(item)
        st.markdown("**2. Junction Table Mappings (CONTENT_GENRES, CONTENT_ACTORS, CONTENT_DIRECTORS):**")
        st.json(raw_mappings)


# ================================================================
# TOP NAVIGATION BAR (STICKY, TRANSPARENT SOLID, NO EMOJIS)
# ================================================================
st.markdown('<div class="top-bar-container">', unsafe_allow_html=True)
col_nav_logo, col_nav_tabs, col_nav_user = st.columns([1.1, 7.5, 3.4])

with col_nav_logo:
    st.markdown(f'<div style="padding-top:4px;">{NETFLIX_LOGO_SVG}</div>', unsafe_allow_html=True)

nav_tabs = [
    "Home",
    "Browse Content",
    "User Profile",
    "Subscription Plans",
    "Payments",
    "Watch History",
    "Reviews and Ratings",
    "Analytics Dashboard",
    "Database Schema",
    "Legal and Compliance"
]

cur_nav = st.session_state.get("nav_page", "Home")
if cur_nav not in nav_tabs:
    cur_nav = "Home"

with col_nav_tabs:
    selected_nav = st.pills(
        "Platform Navigation",
        nav_tabs,
        default=cur_nav,
        label_visibility="collapsed",
        key="top_nav_pills"
    )
    if selected_nav and selected_nav != st.session_state.get("nav_page"):
        st.session_state["nav_page"] = selected_nav
        st.rerun()

with col_nav_user:
    col_u_meta, col_u_prof, col_u_exit = st.columns([1.5, 0.95, 0.95])
    with col_u_meta:
        sub = get_user_subscription(current_user["user_id"])
        plan_badge = sub["plan_name"] if sub else "No Active Plan"
        st.markdown(f"""
        <div style="background-color:#222222; padding:4px 10px; border-radius:4px; border:1px solid #383838; line-height:1.2;">
            <div style="font-size:12px; font-weight:700; color:#ffffff; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{current_profile['profile_name']}</div>
            <div style="font-size:11px; color:#aaaaaa;">{plan_badge}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_u_prof:
        st.markdown('<div class="nav-action-btn">', unsafe_allow_html=True)
        if st.button("Profiles", key="top_switch_prof", help="Switch Profile", use_container_width=True):
            st.session_state.active_profile_id = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with col_u_exit:
        st.markdown('<div class="nav-action-btn">', unsafe_allow_html=True)
        if st.button("Sign Out", key="top_signout", help="Sign Out", use_container_width=True):
            st.session_state.authenticated_user_id = None
            st.session_state.active_profile_id = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

page = st.session_state.get("nav_page", "Home")

# ================================================================
# COOKIE CONSENT BANNER (DPDP ACT 2023 COMPLIANT)
# ================================================================
if "cookie_consent" not in st.session_state:
    st.markdown("""
    <div class="cookie-banner-box">
        <span class="cookie-banner-title">Cookie and Data Privacy Notice</span>
        <p class="cookie-banner-text">
            StreamVault utilizes strictly necessary session cookies for account authentication, request security, 
            and CSRF mitigation. Under the Digital Personal Data Protection (DPDP) Act, 2023, no third-party behavioral 
            trackers or cross-site advertising beacons are deployed.
        </p>
    </div>
    """, unsafe_allow_html=True)
    col_c1, col_c2, col_c3 = st.columns([1.6, 1.4, 6])
    with col_c1:
        if st.button("Accept Essential Cookies", key="cookie_accept_btn", type="primary", use_container_width=True):
            st.session_state["cookie_consent"] = "accepted"
            st.rerun()
    with col_c2:
        if st.button("Review Cookie Policy", key="cookie_policy_btn", type="secondary", use_container_width=True):
            st.session_state["nav_page"] = "Legal and Compliance"
            st.rerun()


# ================================================================
# PAGE: HOME
# ================================================================
if page == "Home":
    featured = CONTENT[2]  # Shadow Agent
    genres = get_content_genres(featured["content_id"])
    director = get_content_director(featured["content_id"])
    actors = get_content_actors(featured["content_id"])

    # Hero Banner with clean, realistic copy
    st.markdown(f"""
    <div class="hero-container">
        <img src="{featured['backdrop_url']}" alt="Promotional still for {featured['title']}">
        <div class="hero-content">
            <div class="hero-title-text">{featured['title']}</div>
            <div style="margin-bottom:8px; display:flex; gap:6px; flex-wrap:wrap; align-items:center;">
                <span class="card-rating-badge">Rating: {featured['rating']} / 10</span>
                <span class="tag-badge">{featured['type']}</span>
                <span class="tag-badge">{featured['maturity']}</span>
                {''.join(f'<span class="tag-badge">{g}</span>' for g in genres)}
            </div>
            <p class="hero-desc-text">{featured['description']}</p>
            <div style="font-size:12px; color:#999999;">
                Director: <strong style="color:#ffffff;">{director}</strong> | 
                Cast: <strong style="color:#ffffff;">{', '.join(actors[:3])}</strong> | 
                Runtime: {featured['duration']} min | 
                Language: {featured['language']} | 
                Year: {featured['release_year']}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_h1, col_h2, col_h3, col_h_pad = st.columns([1.2, 1.5, 1.3, 5])
    with col_h1:
        if st.button("Play Stream", key="hero_btn_play", type="primary", use_container_width=True):
            succ, msg = db.log_watch_progress(featured["content_id"], current_user["user_id"], 45, False)
            st.toast(f"Playing '{featured['title']}'. Progress updated in WATCH_HISTORY.")
            st.rerun()
    with col_h2:
        if st.button("View Details", key="hero_btn_info", type="secondary", use_container_width=True):
            show_movie_detail_dialog(featured["content_id"])
    with col_h3:
        if st.button("Add to Watchlist", key="hero_btn_list", type="secondary", use_container_width=True):
            st.toast(f"Added '{featured['title']}' to your watchlist index.")

    # Factual Relational Database Inventory (No fake consumer metrics)
    st.markdown('<div class="section-title">Relational Database Inventory (SQLite Backend)</div>', unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5)
    inventory_items = [
        (c1, len(USERS), "Registered Users"),
        (c2, len(CONTENT), "Catalog Titles"),
        (c3, len(SUBS_PLANS), "Active Plans"),
        (c4, len(SUBSCRIPTIONS), "Subscriptions"),
        (c5, len(REVIEW_RATINGS), "Verified Reviews"),
    ]
    for col, count_val, label_text in inventory_items:
        with col:
            st.markdown(f"""
            <div class="inventory-stat-card">
                <p class="inventory-stat-num">{count_val}</p>
                <p class="inventory-stat-lbl">{label_text}</p>
            </div>
            """, unsafe_allow_html=True)

    # Trending Titles
    st.markdown('<div class="section-title">Trending Titles</div>', unsafe_allow_html=True)
    trending = sorted(CONTENT, key=lambda x: x["rating"], reverse=True)[:5]
    cols_t = st.columns(5)
    for i, item in enumerate(trending):
        with cols_t[i]:
            item_genres = get_content_genres(item["content_id"])
            st.markdown(f"""
            <div class="content-card">
                <img src="{item['poster_url']}" alt="Official poster for {item['title']}">
                <div class="card-body">
                    <div class="card-title">{item['title']}</div>
                    <div class="card-metadata">
                        <span>{item['release_year']} | {item['duration']} min</span>
                        <span class="card-rating-badge">{item['rating']} / 10</span>
                    </div>
                    <div>
                        {''.join(f'<span class="tag-badge">{g}</span>' for g in item_genres[:2])}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("View Details", key=f"btn_trend_{item['content_id']}", type="secondary", use_container_width=True):
                show_movie_detail_dialog(item["content_id"])

    # Recent Releases (2024)
    st.markdown('<div class="section-title">Recent Releases (2024)</div>', unsafe_allow_html=True)
    new_releases = [c for c in CONTENT if c["release_year"] == 2024][:5]
    cols_n = st.columns(5)
    for i, item in enumerate(new_releases):
        with cols_n[i]:
            item_genres = get_content_genres(item["content_id"])
            st.markdown(f"""
            <div class="content-card">
                <img src="{item['poster_url']}" alt="Official poster for {item['title']}">
                <div class="card-body">
                    <div class="card-title">{item['title']}</div>
                    <div class="card-metadata">
                        <span>{item['duration']} min | {item['language']}</span>
                        <span class="card-rating-badge">{item['rating']} / 10</span>
                    </div>
                    <div>
                        {''.join(f'<span class="tag-badge">{g}</span>' for g in item_genres[:2])}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("View Details", key=f"btn_new_{item['content_id']}", type="secondary", use_container_width=True):
                show_movie_detail_dialog(item["content_id"])

    # Series Section
    st.markdown('<div class="section-title">Television Series</div>', unsafe_allow_html=True)
    series_items = [c for c in CONTENT if c["type"] == "Series"]
    cols_s = st.columns(len(series_items))
    for i, item in enumerate(series_items):
        with cols_s[i]:
            item_genres = get_content_genres(item["content_id"])
            st.markdown(f"""
            <div class="content-card">
                <img src="{item['poster_url']}" alt="Official poster for {item['title']}">
                <div class="card-body">
                    <div class="card-title">{item['title']}</div>
                    <div class="card-metadata">
                        <span>{item['duration']} min/ep | Series</span>
                        <span class="card-rating-badge">{item['rating']} / 10</span>
                    </div>
                    <div>
                        {''.join(f'<span class="tag-badge">{g}</span>' for g in item_genres[:2])}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("View Details", key=f"btn_ser_{item['content_id']}", type="secondary", use_container_width=True):
                show_movie_detail_dialog(item["content_id"])


# ================================================================
# PAGE: BROWSE CONTENT
# ================================================================
elif page == "Browse Content":
    st.markdown('<div class="section-title">Browse Catalog by Attributes</div>', unsafe_allow_html=True)

    filter_cols = st.columns([2, 2, 2, 2])
    with filter_cols[0]:
        genre_filter = st.selectbox("Genre Filter", ["All"] + [g["genre_name"] for g in GENRES])
    with filter_cols[1]:
        type_filter = st.selectbox("Format Filter", ["All", "Movie", "Series"])
    with filter_cols[2]:
        lang_filter = st.selectbox("Language Filter", ["All", "Hindi", "English"])
    with filter_cols[3]:
        sort_by = st.selectbox("Sort Order", ["Rating (Highest First)", "Rating (Lowest First)", "Year (Newest First)", "Year (Oldest First)", "Title (Alphabetical)"])

    filtered = CONTENT.copy()
    if genre_filter != "All":
        genre_content_ids = [cg["content_id"] for cg in CONTENT_GENRES
                             if any(g["genre_id"] == cg["genre_id"] and g["genre_name"] == genre_filter for g in GENRES)]
        filtered = [c for c in filtered if c["content_id"] in genre_content_ids]
    if type_filter != "All":
        filtered = [c for c in filtered if c["type"] == type_filter]
    if lang_filter != "All":
        filtered = [c for c in filtered if c["language"] == lang_filter]

    if sort_by == "Rating (Highest First)":
        filtered.sort(key=lambda x: x["rating"], reverse=True)
    elif sort_by == "Rating (Lowest First)":
        filtered.sort(key=lambda x: x["rating"])
    elif sort_by == "Year (Newest First)":
        filtered.sort(key=lambda x: x["release_year"], reverse=True)
    elif sort_by == "Year (Oldest First)":
        filtered.sort(key=lambda x: x["release_year"])
    elif sort_by == "Title (Alphabetical)":
        filtered.sort(key=lambda x: x["title"])

    st.caption(f"Displaying {len(filtered)} matching catalog titles.")

    for row_start in range(0, len(filtered), 5):
        row_items = filtered[row_start:row_start+5]
        cols_grid = st.columns(5)
        for i, item in enumerate(row_items):
            with cols_grid[i]:
                item_genres = get_content_genres(item["content_id"])
                director = get_content_director(item["content_id"])
                st.markdown(f"""
                <div class="content-card">
                    <img src="{item['poster_url']}" alt="Official poster for {item['title']}">
                    <div class="card-body">
                        <div class="card-title">{item['title']}</div>
                        <div class="card-metadata">
                            <span>{item['release_year']} | {item['language']}</span>
                            <span class="card-rating-badge">{item['rating']} / 10</span>
                        </div>
                        <div style="font-size:12px; color:#888888; margin-bottom:6px;">
                            Director: {director}
                        </div>
                        <div>
                            {''.join(f'<span class="tag-badge">{g}</span>' for g in item_genres[:2])}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("View Details", key=f"btn_grid_{item['content_id']}", type="secondary", use_container_width=True):
                    show_movie_detail_dialog(item["content_id"])


# ================================================================
# PAGE: USER PROFILE
# ================================================================
elif page == "User Profile":
    st.markdown('<div class="section-title">User Account & Profiles (USER and PROFILES Entities)</div>', unsafe_allow_html=True)

    profiles = get_user_profiles(current_user["user_id"])
    sub = get_user_subscription(current_user["user_id"])

    # User profile overview card
    st.markdown(f"""
    <div style="background-color:#1f1f1f; border:1px solid #333333; border-radius:4px; padding:20px 24px; margin-bottom:20px;">
        <div style="display:flex; gap:20px; align-items:center; flex-wrap:wrap;">
            <div style="background-color:#e50914; color:#ffffff; width:64px; height:64px; border-radius:4px; display:flex; align-items:center; justify-content:center; font-size:28px; font-weight:700;">
                {current_user['name'][0]}
            </div>
            <div>
                <h3 style="margin:0 0 4px 0; color:#ffffff;">{current_user['name']}</h3>
                <div style="font-size:13px; color:#cccccc;">Email: {current_user['email']}</div>
                <div style="font-size:13px; color:#cccccc;">Phone: {current_user['phone'] or 'Not provided'}</div>
                <div style="font-size:13px; color:#888888;">Registration Date: {current_user['reg_date']} | Primary User ID: {current_user['user_id']}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### USER Entity Record")
    user_df = pd.DataFrame([{
        "USER_ID (PK)": current_user["user_id"],
        "NAME": current_user["name"],
        "EMAIL": current_user["email"],
        "PASSWORD_HASH": "********",
        "PHONE": current_user["phone"] or "N/A",
        "REG_DATE": current_user["reg_date"]
    }])
    st.dataframe(user_df, use_container_width=True, hide_index=True)

    # PROFILES section
    st.markdown("#### PROFILES Entity Records")
    if profiles:
        prof_cols = st.columns(len(profiles))
        for i, profile in enumerate(profiles):
            with prof_cols[i]:
                st.markdown(f"""
                <div style="background-color:#242424; border:1px solid #383838; border-radius:4px; padding:12px; text-align:center;">
                    <div style="font-weight:700; color:#ffffff; font-size:14px;">{profile['profile_name']}</div>
                    <div style="font-size:12px; color:#888888; margin-top:2px;">Type: {profile['profile_type']}</div>
                    <div style="font-size:11px; color:#666666;">ID: {profile['profile_id']}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("")
        profiles_df = pd.DataFrame([{
            "PROFILE_ID (PK)": p["profile_id"],
            "USER_ID (FK)": p["user_id"],
            "PROFILE_NAME": p["profile_name"],
            "PROFILE_TYPE": p["profile_type"]
        } for p in profiles])
        st.dataframe(profiles_df, use_container_width=True, hide_index=True)

    # Create profile form
    with st.expander("Create New Profile (PROFILES Table)", expanded=False):
        with st.form("new_prof_form"):
            c_p1, c_p2 = st.columns(2)
            with c_p1:
                p_name_val = st.text_input("Profile Name", placeholder="e.g. Living Room, Kids")
            with c_p2:
                p_type_val = st.selectbox("Audience Category", ["Adult", "Kids"])
            btn_add_p = st.form_submit_button("Add Profile Record", type="primary")
            if btn_add_p:
                if not p_name_val.strip():
                    st.warning("Please provide a valid profile name.")
                else:
                    succ, msg = db.create_user_profile(current_user["user_id"], p_name_val.strip(), p_type_val)
                    if succ:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(f"Error: {msg}")

    # Active subscription
    st.markdown("#### SUBSCRIPTION Entity Record")
    if sub:
        plan = get_plan_details(sub["plan_id"])
        sub_df = pd.DataFrame([{
            "SUBS_ID (PK)": sub["subs_id"],
            "USER_ID (FK)": sub["user_id"],
            "PLAN_ID (FK)": sub["plan_id"],
            "PLAN_NAME": plan["plan_name"] if plan else "N/A",
            "START_DATE": sub["start_date"],
            "END_DATE": sub["end_date"],
            "STATUS": sub["status"],
        }])
        st.dataframe(sub_df, use_container_width=True, hide_index=True)
    else:
        st.info("No active subscription record found.")


# ================================================================
# PAGE: SUBSCRIPTION PLANS
# ================================================================
elif page == "Subscription Plans":
    st.markdown('<div class="section-title">Subscription Plans (SUBS_PLAN Entity)</div>', unsafe_allow_html=True)
    st.caption("All subscription tiers are modeled as rows in the SUBS_PLAN table.")

    cols_plan = st.columns(len(SUBS_PLANS))
    for i, plan in enumerate(SUBS_PLANS):
        with cols_plan[i]:
            st.markdown(f"""
            <div style="background-color:#1f1f1f; border:1px solid #333333; border-radius:4px; padding:18px 14px; text-align:center;">
                <h4 style="margin:0 0 6px 0; color:#ffffff;">{plan['plan_name']}</h4>
                <div style="font-size:22px; font-weight:800; color:#ffffff; margin-bottom:8px;">
                    INR {plan['price']:,}
                    <span style="font-size:12px; font-weight:400; color:#888888;">/{plan['duration_mon']} mo</span>
                </div>
                <div style="font-size:12px; color:#cccccc; border-top:1px solid #2a2a2a; padding:6px 0;">Max Screens: {plan['max_screen']}</div>
                <div style="font-size:12px; color:#cccccc; border-top:1px solid #2a2a2a; padding:6px 0;">Quality: {plan['video_qual']}</div>
                <div style="font-size:11px; color:#666666; padding-top:4px;">PLAN_ID: {plan['plan_id']}</div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Subscribe", key=f"btn_sub_plan_{plan['plan_id']}", type="primary", use_container_width=True):
                succ, msg = db.subscribe_and_pay(current_user["user_id"], plan["plan_id"], "Credit Card", simulate_failure=False)
                if succ:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### SUBS_PLAN Entity Schema Table")
    plans_df = pd.DataFrame([{
        "PLAN_ID (PK)": p["plan_id"],
        "PLAN_NAME": p["plan_name"],
        "PRICE (INR)": p["price"],
        "DURATION_MON": p["duration_mon"],
        "MAX_SCREEN": p["max_screen"],
        "VIDEO_QUAL": p["video_qual"],
    } for p in SUBS_PLANS])
    st.dataframe(plans_df, use_container_width=True, hide_index=True)


# ================================================================
# PAGE: PAYMENTS
# ================================================================
elif page == "Payments":
    st.markdown('<div class="section-title">Payment Transactions (PAYMENTS Entity)</div>', unsafe_allow_html=True)
    st.caption("Demonstrating ACID transaction execution and payment record persistence.")

    user_payments = get_user_payments(current_user["user_id"])
    all_payments = db.get_table_df("PAYMENTS").to_dict(orient="records")

    st.markdown("#### User Payment History")
    if user_payments:
        pay_df = pd.DataFrame([{
            "PAYMENT_ID (PK)": p["payment_id"],
            "SUBS_ID (FK)": p["subs_id"],
            "AMOUNT (INR)": f"{p['amount']:,}",
            "PAY_DATE": p["pay_date"],
            "PAY_METHOD": p["pay_method"],
            "STATUS": p["status"],
        } for p in user_payments])
        st.dataframe(pay_df, use_container_width=True, hide_index=True)
    else:
        st.info("No recorded payment transactions for the active user.")

    st.markdown("#### All Global Payment Records (Database Audit)")
    global_pay_df = pd.DataFrame([{
        "PAYMENT_ID (PK)": p["payment_id"],
        "USER_ID (FK)": p["user_id"],
        "SUBS_ID (FK)": p["subs_id"],
        "AMOUNT (INR)": f"{p['amount']:,}",
        "PAY_DATE": p["pay_date"],
        "PAY_METHOD": p["pay_method"],
        "STATUS": p["status"],
    } for p in all_payments])
    st.dataframe(global_pay_df, use_container_width=True, hide_index=True)


# ================================================================
# PAGE: WATCH HISTORY
# ================================================================
elif page == "Watch History":
    st.markdown('<div class="section-title">User Watch History (WATCH_HISTORY Entity)</div>', unsafe_allow_html=True)
    st.caption("Tracks per-user content playback and completion states, fulfilling the PLAYED relationship.")

    history = get_user_watch_history(current_user["user_id"])
    if history:
        for h in history:
            if "title" in h and "duration" in h:
                progress_pct = min((h["progress_min"] / h["duration"]) * 100, 100) if h["duration"] > 0 else 0
                status_txt = "Completed" if h.get("completed") else "In Progress"
                col_hr1, col_hr2 = st.columns([5, 1.2])
                with col_hr1:
                    st.markdown(f"""
                    <div style="background-color:#1f1f1f; border:1px solid #333333; border-radius:4px; padding:12px; margin-bottom:8px; display:flex; gap:14px; align-items:center;">
                        <img src="{h.get('poster_url', '')}" alt="Poster of {h['title']}" style="width:48px; height:68px; object-fit:cover; border-radius:2px; flex-shrink:0;">
                        <div style="flex:1;">
                            <div style="font-weight:700; color:#ffffff; font-size:14px;">{h['title']}</div>
                            <div style="font-size:12px; color:#aaaaaa;">{h['watch_date']} | {h['type']} | Progress: {h['progress_min']} / {h['duration']} min ({int(progress_pct)}%)</div>
                            <div style="font-size:11px; color:#888888;">Status: {status_txt}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_hr2:
                    st.markdown('<div style="padding-top:14px;">', unsafe_allow_html=True)
                    if st.button("View Details", key=f"btn_hist_{h['history_id']}", type="secondary", use_container_width=True):
                        show_movie_detail_dialog(h["content_id"])
                    st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("#### WATCH_HISTORY Data Table")
        hist_df = pd.DataFrame([{
            "HISTORY_ID (PK)": h["history_id"],
            "CONTENT_ID (FK)": h["content_id"],
            "USER_ID (FK)": h["user_id"],
            "TITLE": h.get("title", "N/A"),
            "WATCH_DATE": h["watch_date"],
            "COMPLETED": "Yes" if h["completed"] else "No",
            "PROGRESS_MIN": h["progress_min"],
        } for h in history])
        st.dataframe(hist_df, use_container_width=True, hide_index=True)
    else:
        st.info("No watch history records associated with active user account.")


# ================================================================
# PAGE: REVIEWS AND RATINGS
# ================================================================
elif page == "Reviews and Ratings":
    st.markdown('<div class="section-title">Verified Reviews and Ratings (REVIEW_RATING Entity)</div>', unsafe_allow_html=True)
    st.caption("Title reviews submitted by registered users, fulfilling the RATED_ON relationship.")

    with st.expander("Submit a New Review (REVIEW_RATING Table)", expanded=False):
        with st.form("global_rev_form"):
            c_r1, c_r2 = st.columns([2, 1])
            with c_r1:
                content_map = {f"{c['title']} ({c['release_year']})": c["content_id"] for c in CONTENT}
                picked_label = st.selectbox("Select Catalog Title", list(content_map.keys()))
                picked_id = content_map[picked_label]
            with c_r2:
                picked_score = st.slider("Rating Score (1 to 10)", 1, 10, 8)
            picked_comment = st.text_area("Review Assessment", placeholder="Provide factual review feedback...")
            btn_post_rev = st.form_submit_button("Post Review", type="primary")
            if btn_post_rev:
                if not picked_comment.strip():
                    st.warning("Please provide review text.")
                else:
                    succ, msg = db.add_user_review(picked_id, current_user["user_id"], picked_score, picked_comment.strip())
                    if succ:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)

    st.markdown("#### Verified User Submissions")
    for r in REVIEW_RATINGS:
        content_item = next((c for c in CONTENT if c["content_id"] == r["content_id"]), None)
        title_str = content_item["title"] if content_item else f"Content #{r['content_id']}"
        st.markdown(f"""
        <div style="background-color:#1f1f1f; border:1px solid #333333; border-radius:4px; padding:12px 16px; margin-bottom:8px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-weight:700; color:#ffffff;">{r['user_name']} on <span style="color:#e50914;">{title_str}</span></span>
                <span class="card-rating-badge">Rating: {r['rating']} / 10</span>
            </div>
            <p style="color:#cccccc; font-size:13px; margin:6px 0 4px 0; line-height:1.45;">"{r['review_text']}"</p>
            <div style="color:#777777; font-size:11px;">Date: {r['review_date']} | Review ID: {r['review_id']}</div>
        </div>
        """, unsafe_allow_html=True)


# ================================================================
# PAGE: ANALYTICS DASHBOARD
# ================================================================
elif page == "Analytics Dashboard":
    st.markdown('<div class="section-title">Relational Database Analytics & Reporting</div>', unsafe_allow_html=True)
    st.caption("Aggregated SQL reporting metrics computed directly from SQLite tables.")

    active_subs = len([s for s in SUBSCRIPTIONS if s["status"] == "Active"])
    total_rev = sum(p["amount"] for p in PAYMENTS if p["status"] == "Success")
    avg_score = sum(r["rating"] for r in REVIEW_RATINGS) / len(REVIEW_RATINGS) if REVIEW_RATINGS else 0
    total_watch = sum(h["progress_min"] for h in WATCH_HISTORY)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"<div class='inventory-stat-card'><p class='inventory-stat-num'>{active_subs}</p><p class='inventory-stat-lbl'>Active Subscriptions</p></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='inventory-stat-card'><p class='inventory-stat-num'>INR {total_rev:,}</p><p class='inventory-stat-lbl'>Total Revenue</p></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='inventory-stat-card'><p class='inventory-stat-num'>{avg_score:.1f} / 10</p><p class='inventory-stat-lbl'>Average Catalog Rating</p></div>", unsafe_allow_html=True)
    with c4:
        st.markdown(f"<div class='inventory-stat-card'><p class='inventory-stat-num'>{total_watch // 60} hrs</p><p class='inventory-stat-lbl'>Total Watch Volume</p></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_g1, col_g2 = st.columns(2)
    with col_g1:
        genre_counts = {}
        for cg in CONTENT_GENRES:
            g_item = next((g["genre_name"] for g in GENRES if g["genre_id"] == cg["genre_id"]), "Other")
            genre_counts[g_item] = genre_counts.get(g_item, 0) + 1
        g_df = pd.DataFrame([{"Genre": k, "Titles": v} for k, v in genre_counts.items()])
        fig_g = px.bar(g_df, x="Genre", y="Titles", title="Catalog Distribution by Genre")
        fig_g.update_layout(
            plot_bgcolor="#181818", paper_bgcolor="#181818",
            font=dict(color="#cccccc"),
            xaxis=dict(gridcolor="#282828"), yaxis=dict(gridcolor="#282828")
        )
        st.plotly_chart(fig_g, use_container_width=True)

    with col_g2:
        plan_counts = {}
        for s in SUBSCRIPTIONS:
            p_rec = get_plan_details(s["plan_id"])
            p_name = p_rec["plan_name"] if p_rec else f"Plan {s['plan_id']}"
            plan_counts[p_name] = plan_counts.get(p_name, 0) + 1
        p_df = pd.DataFrame([{"Plan": k, "Subscribers": v} for k, v in plan_counts.items()])
        fig_p = px.bar(p_df, x="Plan", y="Subscribers", title="Subscriber Count by Plan Tier")
        fig_p.update_layout(
            plot_bgcolor="#181818", paper_bgcolor="#181818",
            font=dict(color="#cccccc"),
            xaxis=dict(gridcolor="#282828"), yaxis=dict(gridcolor="#282828")
        )
        st.plotly_chart(fig_p, use_container_width=True)


# ================================================================
# PAGE: DATABASE SCHEMA
# ================================================================
elif page == "Database Schema":
    st.markdown('<div class="section-title">Database Schema (All 11 ER Diagram Entities)</div>', unsafe_allow_html=True)
    st.caption("Visual representation of entities, primary keys (PK), foreign keys (FK), and junction relationships.")

    entities = [
        {"name": "USER", "attrs": [("USER_ID", "PK"), ("NAME", ""), ("EMAIL", "UNIQUE"), ("PASSWORD", ""), ("PHONE", ""), ("REG_DATE", "")]},
        {"name": "PROFILES", "attrs": [("PROFILE_ID", "PK"), ("USER_ID", "FK -> USER"), ("PROFILE_NAME", ""), ("PROFILE_TYPE", "Adult/Kids")]},
        {"name": "SUBS_PLAN", "attrs": [("PLAN_ID", "PK"), ("PLAN_NAME", ""), ("PRICE", ""), ("DURATION_MON", ""), ("MAX_SCREEN", ""), ("VIDEO_QUAL", "")]},
        {"name": "SUBSCRIPTION", "attrs": [("SUBS_ID", "PK"), ("USER_ID", "FK -> USER"), ("PLAN_ID", "FK -> SUBS_PLAN"), ("START_DATE", ""), ("END_DATE", ""), ("STATUS", "")]},
        {"name": "PAYMENTS", "attrs": [("PAYMENT_ID", "PK"), ("USER_ID", "FK -> USER"), ("SUBS_ID", "FK -> SUBSCRIPTION"), ("AMOUNT", ""), ("PAY_DATE", ""), ("PAY_METHOD", ""), ("STATUS", "")]},
        {"name": "CONTENT", "attrs": [("CONTENT_ID", "PK"), ("TITLE", ""), ("DESCRIPTION", ""), ("DURATION", ""), ("LANGUAGE", ""), ("TYPE", ""), ("RELEASE_YEAR", ""), ("MATURITY", ""), ("RATING", "")]},
        {"name": "GENRES", "attrs": [("GENRE_ID", "PK"), ("GENRE_NAME", "")]},
        {"name": "DIRECTORS", "attrs": [("DIRECTOR_ID", "PK"), ("DIRECTOR_NAME", "")]},
        {"name": "ACTORS", "attrs": [("ACTOR_ID", "PK"), ("ACTOR_NAME", "")]},
        {"name": "REVIEW_RATING", "attrs": [("REVIEW_ID", "PK"), ("CONTENT_ID", "FK -> CONTENT"), ("USER_ID", "FK -> USER"), ("REVIEW_TEXT", ""), ("REVIEW_DATE", ""), ("RATING", "")]},
        {"name": "WATCH_HISTORY", "attrs": [("HISTORY_ID", "PK"), ("CONTENT_ID", "FK -> CONTENT"), ("USER_ID", "FK -> USER"), ("WATCH_DATE", ""), ("COMPLETED", ""), ("PROGRESS_MIN", "")]},
    ]

    for row_start in range(0, len(entities), 3):
        row_ents = entities[row_start:row_start+3]
        cols_ent = st.columns(3)
        for i, ent in enumerate(row_ents):
            with cols_ent[i]:
                attr_lines = "".join(f"<div style='font-size:12px; font-family:monospace; color:#cccccc;'>{name} <span style='color:#e50914;'>{typ}</span></div>" for name, typ in ent["attrs"])
                st.markdown(f"""
                <div style="background-color:#1f1f1f; border:1px solid #333333; border-radius:4px; padding:14px; margin-bottom:12px;">
                    <div style="font-weight:700; color:#ffffff; font-size:15px; margin-bottom:8px; border-bottom:1px solid #2d2d2d; padding-bottom:4px;">Entity: {ent['name']}</div>
                    {attr_lines}
                </div>
                """, unsafe_allow_html=True)


# ================================================================
# PAGE: LEGAL AND COMPLIANCE (DPDP ACT 2023, TERMS, REFUNDS)
# ================================================================
elif page == "Legal and Compliance":
    st.markdown('<div class="section-title">Legal, Regulatory & Governance Compliance</div>', unsafe_allow_html=True)
    st.caption(f"Operated by {legal.BUSINESS_DETAILS['legal_name']} (CIN: {legal.BUSINESS_DETAILS['cin']}).")

    legal_tab1, legal_tab2, legal_tab3, legal_tab4, legal_tab5, legal_tab6 = st.tabs([
        "Privacy Policy (DPDP Act)",
        "Terms and Conditions",
        "Cookie Policy",
        "Refund Policy",
        "Corporate & Grievance",
        "Disclaimers & Risks"
    ])

    with legal_tab1:
        st.markdown(legal.PRIVACY_POLICY_MD)

    with legal_tab2:
        st.markdown(legal.TERMS_OF_SERVICE_MD)

    with legal_tab3:
        st.markdown(legal.COOKIE_POLICY_MD)

    with legal_tab4:
        st.markdown(legal.REFUND_POLICY_MD)

    with legal_tab5:
        b = legal.BUSINESS_DETAILS
        g = b["grievance_officer"]
        st.markdown(f"""
        ### Corporate Information & Grievance Redressal Mechanism

        **Entity Details:**
        - **Legal Entity Name:** {b['legal_name']}
        - **Corporate Identification Number (CIN):** {b['cin']}
        - **Registered Office:** {b['registered_office']}
        - **Corporate Office:** {b['corporate_office']}
        - **Support Email:** {b['contact_email']}
        - **Compliance Email:** {b['compliance_email']}
        - **Helpline Phone:** {b['contact_phone']}
        - **Working Hours:** {b['working_hours']}

        ---

        ### Statutory Grievance Redressal Officer (DPDP Act 2023 / IT Rules)
        In accordance with the Digital Personal Data Protection Act, 2023 and the Information Technology (Intermediary Guidelines) Rules:
        - **Officer Name:** {g['name']}
        - **Designation:** {g['designation']}
        - **Email:** {g['email']}
        - **Direct Phone:** {g['phone']}
        - **Office Address:** {g['address']}
        - **Redressal Timeline:** {g['response_time']}
        """)

    with legal_tab6:
        st.markdown(legal.LEGAL_RISKS_AND_DISCLAIMERS_MD)


# ================================================================
# CUSTOM 404 HANDLER FOR UNRECOGNIZED ROUTES
# ================================================================
else:
    st.markdown("""
    <div style="text-align:center; padding:60px 20px;">
        <h1 style="font-size:42px; font-weight:800; color:#e50914; margin-bottom:8px;">404 - Section Not Found</h1>
        <p style="font-size:15px; color:#cccccc; max-width:480px; margin:0 auto 24px auto; line-height:1.5;">
            The requested section or record identifier does not exist in the platform routing index.
        </p>
    </div>
    """, unsafe_allow_html=True)
    col_404_l, col_404_btn, col_404_r = st.columns([2, 1.2, 2])
    with col_404_btn:
        if st.button("Return to Catalog Home", type="primary", use_container_width=True):
            st.session_state["nav_page"] = "Home"
            st.rerun()
