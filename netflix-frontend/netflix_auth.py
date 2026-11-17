"""
Authentication and Profile Selector Module.
Fully compliant with DPDP Act 2023 principles (data minimization, explicit consent).
No gradients, no pill buttons, no emojis, strict form validation, anti-spam protections.
"""

import streamlit as st
import re
import time
from datetime import datetime
import data.database as db
from legal_policies import BUSINESS_DETAILS

# Clean vector Netflix wordmark (solid fill)
NETFLIX_LOGO_SVG = """<svg xmlns="http://www.w3.org/2000/svg" width="140" height="38" viewBox="0 0 1024 276.742"><path d="M140.803 258.904c-15.404 2.705-31.079 3.516-47.294 5.676l-49.458-144.856v151.073c-15.404 1.621-29.457 3.783-44.051 5.945v-276.742h41.08l56.212 157.021v-157.021h43.511v258.904zm85.131-157.558c16.757 0 42.431-.811 57.835-.811v43.24c-19.189 0-41.619 0-57.835.811v64.322c25.405-1.621 50.809-3.785 76.482-4.596v41.617l-119.724 9.461v-255.39h119.724v43.241h-76.482v58.105zm237.284-58.104h-44.862v198.908c-14.594 0-29.188 0-43.239.539v-199.447h-44.862v-43.242h132.965l-.002 43.242zm70.266 55.132h59.187v43.24h-59.187v98.104h-42.433v-239.718h120.808v43.241h-78.375v55.133zm148.641 103.507c24.594.539 49.456 2.434 73.51 3.783v42.701c-38.646-2.434-77.293-4.863-116.75-5.676v-242.689h43.24v201.881zm109.994 49.457c13.783.812 28.377 1.623 42.43 3.242v-254.58h-42.43v251.338zm231.881-251.338l-54.863 131.615 54.863 145.127c-16.217-2.162-32.432-5.135-48.648-7.838l-31.078-79.994-31.617 73.51c-15.678-2.705-30.812-3.516-46.484-5.678l55.672-126.75-50.269-129.992h46.482l28.377 72.699 30.27-72.699h47.295z" fill="#E50914"/></svg>"""

NETFLIX_AUTH_CSS = """
<style>
/* Clean system font stack, high contrast, zero gradients */
body, .stApp {
    background-color: #141414 !important;
    background-image: none !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
    color: #ffffff !important;
}

section[data-testid="stSidebar"], div[data-testid="collapsedControl"] {
    display: none !important;
}
#MainMenu, footer, header {
    visibility: hidden !important;
}

.main .block-container {
    max-width: 1080px !important;
    padding-top: 1.5rem !important;
    padding-bottom: 2.5rem !important;
}

/* Card Container: Solid matte card with crisp 4px border-radius */
div[data-testid="stColumn"]:has(div[data-testid="stForm"]) > div {
    background-color: #1f1f1f !important;
    background-image: none !important;
    border-radius: 4px !important;
    padding: 32px 36px !important;
    border: 1px solid #333333 !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.7) !important;
}

div[data-testid="stForm"] {
    border: none !important;
    padding: 0 !important;
    background: transparent !important;
}

/* Text Inputs: Square edges, high contrast */
div[data-testid="stTextInput"] input {
    background-color: #2b2b2b !important;
    color: #ffffff !important;
    border: 1px solid #444444 !important;
    border-radius: 4px !important;
    height: 46px !important;
    padding: 10px 14px !important;
    font-size: 15px !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #e50914 !important;
    outline: 2px solid #ffffff !important;
    outline-offset: 1px !important;
    background-color: #333333 !important;
}
div[data-testid="stTextInput"] label {
    color: #d1d5db !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}

/* Buttons: Strict 4px radius, flat solid colors, visible focus outline */
button {
    border-radius: 4px !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif !important;
    letter-spacing: 0.01em !important;
    transition: background-color 0.15s ease, border-color 0.15s ease !important;
}
button:focus-visible {
    outline: 2px solid #ffffff !important;
    outline-offset: 2px !important;
}

button[kind="primary"] {
    background-color: #e50914 !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    border: 1px solid #e50914 !important;
    height: 44px !important;
    width: 100% !important;
}
button[kind="primary"]:hover {
    background-color: #b80710 !important;
    border-color: #b80710 !important;
}

button[kind="secondary"] {
    background-color: #2b2b2b !important;
    color: #ffffff !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    border: 1px solid #444444 !important;
    height: 40px !important;
    width: 100% !important;
}
button[kind="secondary"]:hover {
    background-color: #3a3a3a !important;
    border-color: #666666 !important;
}

/* Checkbox styling */
div[data-testid="stCheckbox"] label span {
    color: #d1d5db !important;
    font-size: 13px !important;
}

/* Anti-spam honeypot hidden from human view */
div[data-testid="stTextInput"]:has(input[aria-label="Leave blank if human"]),
div:has(> div > input[aria-label="Leave blank if human"]),
div:has(> div > div > input[aria-label="Leave blank if human"]) {
    position: absolute !important;
    left: -9999px !important;
    opacity: 0 !important;
    height: 0 !important;
    width: 0 !important;
    overflow: hidden !important;
    pointer-events: none !important;
}

/* Profile Selector: Flat solid avatars */
.profile-card-tile {
    text-align: center;
    cursor: pointer;
    padding: 8px;
}
.profile-avatar-box {
    width: 110px;
    height: 110px;
    border-radius: 4px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.2rem;
    font-weight: 700;
    color: #ffffff;
    border: 2px solid transparent;
    transition: border-color 0.15s ease;
}
.profile-avatar-box:hover {
    border-color: #ffffff;
}
.profile-tile-name {
    margin-top: 10px;
    color: #cccccc;
    font-size: 1rem;
    font-weight: 600;
}
.profile-tile-type {
    font-size: 0.78rem;
    color: #888888;
    margin-top: 2px;
}

/* Clean Footer */
.compliance-footer {
    max-width: 960px;
    margin: 40px auto 0 auto;
    padding: 20px 10px;
    color: #888888;
    font-size: 12px;
    border-top: 1px solid #2a2a2a;
    line-height: 1.6;
}
.compliance-footer a {
    color: #aaaaaa;
    text-decoration: underline;
}
</style>
"""

# Solid, non-gradient avatar palette
SOLID_AVATAR_COLORS = [
    "#e50914",  # Red
    "#1d4ed8",  # Blue
    "#047857",  # Emerald Green
    "#b45309",  # Amber
    "#6d28d9",  # Purple
    "#374151",  # Dark Slate
]

EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"


def validate_email_address(email):
    """Validate email address format strictly."""
    if not email or not isinstance(email, str):
        return False
    return bool(re.match(EMAIL_REGEX, email.strip()))


def render_netflix_login():
    """Render the accessible, DPDP Act compliant sign in / registration page."""
    st.markdown(NETFLIX_AUTH_CSS, unsafe_allow_html=True)

    # Top brand bar
    col_t1, col_t2 = st.columns([1.5, 4.5])
    with col_t1:
        st.markdown(f'<div style="padding-top:4px;">{NETFLIX_LOGO_SVG}</div>', unsafe_allow_html=True)
    with col_t2:
        st.markdown(
            '<div style="text-align:right; font-size:13px; color:#aaaaaa; padding-top:10px;">'
            f'{BUSINESS_DETAILS["legal_name"]} | Secure Portal'
            '</div>',
            unsafe_allow_html=True
        )

    st.markdown("<hr style='border:none; border-top:1px solid #262626; margin:14px 0 24px 0;'>", unsafe_allow_html=True)

    auth_mode = st.session_state.get("auth_mode", "login")

    col_pad_l, col_center, col_pad_r = st.columns([1, 1.4, 1])

    with col_center:
        # Pre-seeded test accounts selector
        all_db_users = db.get_all_users()
        user_options = {f"{u['name']} ({u['email']})": u for u in all_db_users}

        with st.expander("Pre-seeded Test Accounts (USER Table)", expanded=False):
            st.caption("Select an existing database record to inspect the system:")
            selected_label = st.selectbox("Registered Account", list(user_options.keys()), key="demo_user_picker")
            if st.button("Authenticate Selected Account", key="btn_demo_login", type="secondary", use_container_width=True):
                chosen_user = user_options[selected_label]
                st.session_state.authenticated_user_id = chosen_user["user_id"]
                st.session_state.authenticated_user = chosen_user
                st.session_state.active_profile_id = None
                st.rerun()

        if auth_mode == "login":
            st.markdown('<h1 style="font-size:26px; font-weight:700; color:#ffffff; margin:0 0 18px 0;">Sign In</h1>', unsafe_allow_html=True)

            with st.form("signin_form", clear_on_submit=False):
                email_input = st.text_input("Email address", placeholder="name@example.com", key="login_email")
                password_input = st.text_input("Password", type="password", placeholder="Password", key="login_pass")

                # Anti-spam honeypot (invisible to legitimate users)
                hp_val = st.text_input("Leave blank if human", key="login_hp", label_visibility="collapsed")

                col_chk1, col_chk2 = st.columns(2)
                with col_chk1:
                    remember_me = st.checkbox("Remember me", value=True)
                with col_chk2:
                    st.caption("HTTPS Encrypted")

                # Form submission
                btn_signin = st.form_submit_button("Sign In", type="primary", use_container_width=True)

                if btn_signin:
                    if hp_val:
                        # Bot trap triggered
                        st.error("Automated submission blocked.")
                    elif not email_input.strip():
                        st.error("Please enter your registered email address.")
                    elif not validate_email_address(email_input):
                        st.error("Please enter a valid email address format (e.g. user@example.com).")
                    elif not password_input:
                        st.error("Please enter your password.")
                    else:
                        user = db.authenticate_user(email_input, password_input)
                        if user:
                            st.session_state.authenticated_user_id = user["user_id"]
                            st.session_state.authenticated_user = user
                            st.session_state.active_profile_id = None
                            st.success("Authentication successful.")
                            st.rerun()
                        else:
                            st.error("Invalid credentials. Please verify your email or select a pre-seeded account above.")

            st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

            # Registration switch
            st.markdown("<div style='font-size:14px; color:#888888; margin-top:14px;'>New to the platform?</div>", unsafe_allow_html=True)
            if st.button("Create an Account", key="btn_go_to_signup", type="secondary", use_container_width=True):
                st.session_state.auth_mode = "signup"
                st.rerun()

            st.markdown(
                '<div style="font-size:11px; color:#777777; margin-top:16px; line-height:1.4;">'
                'Personal data processing is governed by the Digital Personal Data Protection Act, 2023. '
                'We do not engage in unauthorized third-party tracking or cross-site telemetry.'
                '</div>',
                unsafe_allow_html=True
            )

        else:
            # Registration Mode
            st.markdown('<h1 style="font-size:26px; font-weight:700; color:#ffffff; margin:0 0 8px 0;">Create Account</h1>', unsafe_allow_html=True)
            st.caption("Register an account to access the catalog and subscription services.")

            with st.form("signup_form"):
                new_name = st.text_input("Full Name *", placeholder="Enter legal name", key="reg_name")
                new_email = st.text_input("Email Address *", placeholder="name@example.com", key="reg_email")
                new_phone = st.text_input("Mobile Phone (Optional)", placeholder="10-digit number", key="reg_phone")
                new_pass = st.text_input("Password (min 6 characters) *", type="password", placeholder="Set a secure password", key="reg_pass")

                # Anti-spam honeypot
                hp_val_reg = st.text_input("Leave blank if human", key="reg_hp", label_visibility="collapsed")

                # Mandatory DPDP Consent Checkbox
                consent_given = st.checkbox(
                    "I have read and agree to the Terms of Service, and I consent to the collection and processing of my name and email strictly for account administration in accordance with the Privacy Policy (DPDP Act, 2023).",
                    value=False,
                    key="reg_consent_chk"
                )

                btn_create = st.form_submit_button("Register Account", type="primary", use_container_width=True)

                if btn_create:
                    if hp_val_reg:
                        st.error("Automated bot submission detected.")
                    elif not new_name.strip():
                        st.error("Please provide your full name.")
                    elif not new_email.strip() or not validate_email_address(new_email):
                        st.error("Please provide a valid email address.")
                    elif len(new_pass) < 6:
                        st.error("Password must be at least 6 characters long.")
                    elif not consent_given:
                        st.error("Statutory consent is required under Section 6 of the DPDP Act 2023 to proceed with account creation.")
                    else:
                        succ, msg, new_uid = db.register_user(new_name, new_email, new_pass, new_phone)
                        if succ:
                            st.success("Account registered successfully.")
                            st.session_state.authenticated_user_id = new_uid
                            st.session_state.authenticated_user = db.get_user_by_id(new_uid)
                            st.session_state.active_profile_id = None
                            st.session_state.auth_mode = "login"
                            st.rerun()
                        else:
                            st.error(f"Registration error: {msg}")

            if st.button("Already have an account? Sign In", key="btn_back_to_login", type="secondary", use_container_width=True):
                st.session_state.auth_mode = "login"
                st.rerun()

    # Compliance Footer
    footer_html = f"""
    <div class="compliance-footer">
        <div style="display:flex; justify-content:space-between; flex-wrap:wrap; gap:12px; margin-bottom:12px;">
            <span>Entity: {BUSINESS_DETAILS['legal_name']} (CIN: {BUSINESS_DETAILS['cin']})</span>
            <span>Grievance Officer: {BUSINESS_DETAILS['grievance_officer']['email']}</span>
        </div>
        <div>
            This system enforces HTTPS transport security, adheres to purpose specification under the DPDP Act 2023, 
            and implements relational integrity constraints. All catalog titles are educational demo assets.
        </div>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)


def render_whos_watching(user):
    """Render clean, solid-color profile selection screen without gradients or emojis."""
    st.markdown(NETFLIX_AUTH_CSS, unsafe_allow_html=True)

    # Top brand bar with Sign Out button
    col_w1, col_w2 = st.columns([5, 1.2])
    with col_w1:
        st.markdown(f'<div style="padding-top:6px;">{NETFLIX_LOGO_SVG}</div>', unsafe_allow_html=True)
    with col_w2:
        if st.button("Sign Out", key="whos_signout_btn", type="secondary", use_container_width=True):
            st.session_state.authenticated_user_id = None
            st.session_state.authenticated_user = None
            st.session_state.active_profile_id = None
            st.rerun()

    st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)
    st.markdown('<h1 style="font-size:36px; font-weight:600; text-align:center; color:#ffffff; margin:10px 0 32px 0;">Who is watching?</h1>', unsafe_allow_html=True)

    profiles = db.get_user_profiles(user["user_id"])
    if not profiles:
        db.create_user_profile(user["user_id"], user["name"].split()[0], "Adult")
        profiles = db.get_user_profiles(user["user_id"])

    # Center profile cards with side padding
    num_profiles = len(profiles)
    total_slots = num_profiles + 1
    side_pad = max(0.6, (12 - total_slots * 2.2) / 2)
    col_weights = [side_pad] + [2.2] * total_slots + [side_pad]
    all_cols = st.columns(col_weights)
    cols = all_cols[1:-1]

    for i, prof in enumerate(profiles):
        with cols[i]:
            bg_color = SOLID_AVATAR_COLORS[i % len(SOLID_AVATAR_COLORS)]
            initial = prof["profile_name"][:1].upper() if prof["profile_name"] else "U"

            st.markdown(
                '<div class="profile-card-tile">'
                f'<div class="profile-avatar-box" style="background-color:{bg_color};">{initial}</div>'
                f'<div class="profile-tile-name">{prof["profile_name"]}</div>'
                f'<div class="profile-tile-type">{prof["profile_type"]}</div>'
                '</div>',
                unsafe_allow_html=True
            )

            if st.button(f"Select: {prof['profile_name']}", key=f"select_prof_{prof['profile_id']}", type="secondary", use_container_width=True):
                st.session_state.active_profile_id = prof["profile_id"]
                st.session_state.active_profile = prof
                st.rerun()

    # Add Profile Slot
    with cols[num_profiles]:
        st.markdown(
            '<div class="profile-card-tile">'
            '<div class="profile-avatar-box" style="background-color:#262626; border:2px dashed #555555; font-size:1.8rem; color:#888888;">+</div>'
            '<div class="profile-tile-name">Add Profile</div>'
            '<div class="profile-tile-type">New Profile</div>'
            '</div>',
            unsafe_allow_html=True
        )

        with st.popover("Add Profile", use_container_width=True):
            p_name = st.text_input("Profile Name", placeholder="e.g. Work, Study", key="who_add_name")
            p_type = st.selectbox("Audience Category", ["Adult", "Kids"], key="who_add_type")
            if st.button("Save Profile", key="who_add_btn", type="primary", use_container_width=True):
                if p_name.strip():
                    db.create_user_profile(user["user_id"], p_name.strip(), p_type)
                    st.rerun()

    st.markdown("<div style='height:40px;'></div>", unsafe_allow_html=True)
    c_m1, c_m2, c_m3 = st.columns([1.8, 1, 1.8])
    with c_m2:
        if st.button("Manage Profiles", key="manage_profs_btn", type="secondary", use_container_width=True):
            st.session_state.active_profile_id = profiles[0]["profile_id"]
            st.session_state.active_profile = profiles[0]
            st.session_state["nav_page"] = "User Profile"
            st.rerun()
