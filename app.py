# ============================================================
# Suraksha Sakhi — Women's Online Safety Dashboard
# Protecting girls from cam phishing and online traps
# ============================================================
# HOW TO RUN:
#   1. Make sure Python is installed on your computer.
#   2. Open a terminal (Command Prompt or PowerShell).
#   3. Navigate to this folder:
#        cd "c:\IBM NEW PROJECT CYBERSECURITY CAM PHISHING"
#   4. Install the required libraries (only once):
#        pip install -r requirements.txt
#   5. Run the app:
#        streamlit run app.py
#   6. Your browser will open automatically at http://localhost:8501
# ============================================================

import streamlit as st          # Streamlit is the web dashboard library
import re                        # re = regular expressions, used to search inside URLs
import pandas as pd              # pandas lets us create and display tables of data
import io                        # io lets us work with files in memory (no disk needed)
from PIL import Image            # PIL / Pillow: open and process images
from PIL.ExifTags import TAGS    # TAGS maps raw EXIF tag numbers to human-readable names

# ── PAGE CONFIG ──────────────────────────────────────────────
# This must be the FIRST Streamlit command in the file.
# We set the page title, icon, and a wide layout.
st.set_page_config(
    page_title="Suraksha Sakhi",
    page_icon="🛡️",
    layout="wide",
)

# ── CUSTOM CSS (Dark Theme + Purple/Pink Accents) ─────────────
# st.markdown with unsafe_allow_html=True lets us inject CSS
# to give the app a custom dark look and feel.
st.markdown("""
<style>
/* ── Global background and text ── */
html, body, [class*="css"] {
    background-color: #0f0f1a;   /* very dark navy */
    color: #e8e8f0;               /* soft white text */
    font-family: 'Segoe UI', sans-serif;
}

/* ── Main content area ── */
.main .block-container {
    background-color: #0f0f1a;
    padding: 2rem 2.5rem;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: #16162a;   /* slightly lighter dark */
    border-right: 1px solid #2e2e4a;
}
[data-testid="stSidebar"] * {
    color: #c8c8e0 !important;
}

/* ── KPI card style ── */
.kpi-card {
    background-color: #1c1c30;
    border: 1px solid #2e2e4a;
    border-left: 4px solid #9b59b6;  /* purple accent */
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    text-align: center;
}
.kpi-card h3 {
    margin: 0 0 0.3rem 0;
    font-size: 0.85rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #a88fc8;               /* light purple label */
}
.kpi-card p {
    margin: 0;
    font-size: 2.4rem;
    font-weight: 700;
    color: #e91e8c;               /* pink number */
}
.kpi-card span {
    font-size: 0.78rem;
    color: #7878a0;               /* muted footnote */
}

/* ── Section headings ── */
h1, h2, h3 {
    color: #e0d0f5;
}

/* ── Horizontal rule ── */
hr {
    border-color: #2e2e4a;
}

/* ── Description box ── */
.desc-box {
    background-color: #1c1c30;
    border-left: 4px solid #e91e8c;  /* pink accent */
    border-radius: 8px;
    padding: 1rem 1.4rem;
    margin-bottom: 1.5rem;
    color: #c8c8e0;
    font-size: 0.97rem;
    line-height: 1.7;
}
/* ── Result verdict boxes ── */
.verdict-safe {
    background-color: #0d2b1a;
    border-left: 4px solid #27ae60;
    border-radius: 8px;
    padding: 1rem 1.4rem;
    margin-top: 1rem;
    color: #aef5c8;
}
.verdict-suspicious {
    background-color: #2b2200;
    border-left: 4px solid #f39c12;
    border-radius: 8px;
    padding: 1rem 1.4rem;
    margin-top: 1rem;
    color: #ffd98a;
}
.verdict-dangerous {
    background-color: #2b0d0d;
    border-left: 4px solid #e74c3c;
    border-radius: 8px;
    padding: 1rem 1.4rem;
    margin-top: 1rem;
    color: #ffaaaa;
}
.checker-box {
    background-color: #1c1c30;
    border: 1px solid #2e2e4a;
    border-radius: 10px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)


# ── SIDEBAR — navigation menu ─────────────────────────────────
# st.sidebar.radio() renders clickable radio buttons in the sidebar.
# The value chosen by the user is stored in the variable `page`.
# Every content block below checks `page` to decide whether to show itself.
with st.sidebar:
    st.markdown("## 🛡️ Suraksha Sakhi")
    st.markdown("*Women's Online Safety*")
    st.markdown("---")

    # Navigation radio — labels map directly to page names used in if-blocks below
    page = st.sidebar.radio(
        "Navigate to:",
        options=[
            "🏠 Dashboard",
            "🔍 Link Checker",
            "📋 Link History",
            "📷 Camera Alerts",
            "🖼️ Photo Safety",
            "📊 Charts",
            "❓ Help & Tips",
            "ℹ️ About",
        ],
    )

    st.markdown("---")
    st.markdown("🟢 &nbsp; **Status:** Active")
    st.markdown("📅 &nbsp; **Updated:** Oct 31, 2026")
    st.markdown("---")
    st.caption("Made with ❤️ for women's digital safety.")


# ── FICTIONAL LINK HISTORY DATA ──────────────────────────────
# This function builds a pandas DataFrame of 20 made-up link records.
# Each record has: Time, Source (where the link came from), Link, and Result.
# We include many Suspicious/Dangerous links from WhatsApp so we can
# show source patterns later in the dashboard.
# NOTE: every link here is fictional — none of these are real websites.

def make_history():
    """Return a fresh DataFrame of 20 fictional link-history records."""
    records = [
        # ── WhatsApp cluster: several Suspicious & Dangerous ──
        {"Time": "09:02", "Source": "WhatsApp", "Link": "http://free-camera-verify.example/activate",       "Result": "Dangerous"},
        {"Time": "09:15", "Source": "WhatsApp", "Link": "https://bit.ly/wa-prize-claim",                    "Result": "Suspicious"},
        {"Time": "09:31", "Source": "WhatsApp", "Link": "http://192.168.55.12/login-now",                   "Result": "Dangerous"},
        {"Time": "09:47", "Source": "WhatsApp", "Link": "https://win-free-webcam-access.example/verify",    "Result": "Dangerous"},
        {"Time": "10:05", "Source": "WhatsApp", "Link": "https://tinyurl.com/wacam2026",                    "Result": "Suspicious"},
        {"Time": "10:22", "Source": "WhatsApp", "Link": "https://safe-helpline.example/contact",            "Result": "Safe"},
        # ── Instagram: mix of safe and suspicious ──
        {"Time": "08:11", "Source": "Instagram", "Link": "http://insta-free-follower-prize.example/claim",  "Result": "Dangerous"},
        {"Time": "08:44", "Source": "Instagram", "Link": "https://bit.ly/ig-offer99",                       "Result": "Suspicious"},
        {"Time": "09:58", "Source": "Instagram", "Link": "https://official-helpdesk.example/support",       "Result": "Safe"},
        {"Time": "10:33", "Source": "Instagram", "Link": "https://photo-verify-login.example/account",      "Result": "Suspicious"},
        # ── SMS: a few dangerous and one safe ──
        {"Time": "07:30", "Source": "SMS",       "Link": "http://urgent-reward-claim.example/free-gift",    "Result": "Dangerous"},
        {"Time": "08:00", "Source": "SMS",       "Link": "https://tinyurl.com/sms-winner",                  "Result": "Suspicious"},
        {"Time": "08:55", "Source": "SMS",       "Link": "https://bank-verify-login.example/secure",        "Result": "Suspicious"},
        {"Time": "11:10", "Source": "SMS",       "Link": "https://gov-scholarship.example/apply",           "Result": "Safe"},
        # ── Email: mixture ──
        {"Time": "07:05", "Source": "Email",     "Link": "http://prize-winner-camera-access.example/open",  "Result": "Dangerous"},
        {"Time": "07:45", "Source": "Email",     "Link": "https://bit.ly/email-prize-2026",                 "Result": "Suspicious"},
        {"Time": "08:20", "Source": "Email",     "Link": "https://university-portal.example/login",         "Result": "Safe"},
        {"Time": "09:10", "Source": "Email",     "Link": "https://safe-newsletter.example/unsubscribe",     "Result": "Safe"},
        {"Time": "10:50", "Source": "Email",     "Link": "http://verify-your-webcam-now.example/enable",    "Result": "Dangerous"},
        {"Time": "11:30", "Source": "Email",     "Link": "https://job-portal.example/apply",                "Result": "Safe"},
    ]
    # pandas.DataFrame() turns our list of dicts into a table
    return pd.DataFrame(records)


# ── FICTIONAL CAMERA ALERT DATA ──────────────────────────────
# This function builds a DataFrame of 10 made-up camera/permission alert events.
# Each event has: Time, App/Site, Permission, Risk, and Reason.
# NOTE: all app/site names are fictional — none are real.
# A real app would detect these events via phone OS permission APIs,
# which we cannot do in a web prototype, so we simulate them here.

def make_cam_alerts():
    """Return a fresh DataFrame of 10 fictional camera-alert events."""
    events = [
        {
            "Time": "08:14",
            "App / Site": "free-gift-camera.example",
            "Permission": "Camera",
            "Risk": "High",
            "Reason": "Unknown website requested camera access without user action",
        },
        {
            "Time": "08:31",
            "App / Site": "video-verify-now.example",
            "Permission": "Camera",
            "Risk": "High",
            "Reason": "Fake video-call link from unverified sender opened camera silently",
        },
        {
            "Time": "09:02",
            "App / Site": "flashlight-free-app.example",
            "Permission": "Camera",
            "Risk": "High",
            "Reason": "Flashlight app tried to turn on the camera in the background",
        },
        {
            "Time": "09:20",
            "App / Site": "prize-scanner.example",
            "Permission": "Camera",
            "Risk": "High",
            "Reason": "QR-code scanner app requested camera while the screen was off",
        },
        {
            "Time": "09:45",
            "App / Site": "lucky-draw-wa.example",
            "Permission": "Microphone",
            "Risk": "High",
            "Reason": "WhatsApp forwarded link triggered microphone permission silently",
        },
        {
            "Time": "10:05",
            "App / Site": "photo-editor-free.example",
            "Permission": "Gallery",
            "Risk": "Medium",
            "Reason": "Free photo editor app requested full gallery access on first launch",
        },
        {
            "Time": "10:22",
            "App / Site": "discount-coupon.example",
            "Permission": "Microphone",
            "Risk": "Medium",
            "Reason": "Coupon website requested microphone — unusual for a shopping page",
        },
        {
            "Time": "10:50",
            "App / Site": "ringtone-maker.example",
            "Permission": "Gallery",
            "Risk": "Medium",
            "Reason": "Ringtone app scanned all photos in gallery during setup",
        },
        {
            "Time": "11:15",
            "App / Site": "weather-app.example",
            "Permission": "Camera",
            "Risk": "Low",
            "Reason": "Weather app asked for camera to scan a QR code for settings sync",
        },
        {
            "Time": "11:40",
            "App / Site": "fitness-tracker.example",
            "Permission": "Gallery",
            "Risk": "Low",
            "Reason": "Fitness app requested gallery access to set a profile photo",
        },
    ]
    return pd.DataFrame(events)


# ── SESSION STATE — counters, last result, link history ───────
# st.session_state persists values across Streamlit reruns.
# We initialise each key only once (on the very first load).

# "extra_checked" counts links scanned via the Link Checker widget.
# We add this to the history-derived counts for the KPI cards.
if "extra_checked" not in st.session_state:
    st.session_state.extra_checked = 0      # starts at zero
if "extra_safe" not in st.session_state:
    st.session_state.extra_safe = 0
if "extra_suspicious" not in st.session_state:
    st.session_state.extra_suspicious = 0
# cam_alerts holds the 10-row camera alerts DataFrame.
# We auto-generate it on first load.
if "cam_alerts" not in st.session_state:
    st.session_state.cam_alerts = make_cam_alerts()

# last_result stores the most recent Link Checker result so it
# survives Streamlit's automatic rerun that happens after a button click.
if "last_result" not in st.session_state:
    st.session_state.last_result = None     # will hold a dict once a check runs

# link_history holds the 20-row DataFrame.
# We auto-generate it on first load so the table is visible immediately.
if "link_history" not in st.session_state:
    st.session_state.link_history = make_history()


# ── LINK CHECKER LOGIC ───────────────────────────────────────
# This function receives a URL string and returns:
#   score   — integer risk score (higher = more risky)
#   verdict — "Safe", "Suspicious", or "Dangerous"
#   reasons — list of strings explaining what was flagged

def check_link(url: str):
    url = url.strip()           # remove accidental spaces
    reasons = []                # collect all reasons found
    score = 0                   # start with zero risk

    # ── Rule 1: URL shorteners ────────────────────────────────
    # Services like bit.ly hide the real destination.
    # Attackers use them so victims cannot see the true URL.
    SHORTENERS = ["bit.ly", "tinyurl.com", "t.co", "goo.gl",
                  "ow.ly", "buff.ly", "is.gd", "rb.gy", "cutt.ly"]
    for shortener in SHORTENERS:
        if shortener in url.lower():
            score += 30
            reasons.append(f"Uses a URL shortener ({shortener}) — hides the real destination")
            break  # no need to check all shorteners once one matches

    # ── Rule 2: HTTP instead of HTTPS ─────────────────────────
    # HTTPS encrypts data between you and the website.
    # HTTP sends everything in plain text — easy to intercept.
    if url.lower().startswith("http://"):
        score += 25
        reasons.append("Uses HTTP (not HTTPS) — your data is NOT encrypted")

    # ── Rule 3: IP address instead of a domain name ───────────
    # Legitimate websites use domain names (e.g., google.com).
    # An IP address like http://192.168.1.1/login is a red flag.
    # We use a regular expression to detect patterns like digits.digits.digits.digits
    ip_pattern = re.compile(r"https?://(\d{1,3}\.){3}\d{1,3}")
    if ip_pattern.search(url):
        score += 35
        reasons.append("Contains a raw IP address instead of a domain name")

    # ── Rule 4: Dangerous keywords in the URL ─────────────────
    # Phishing pages often contain words that lure victims.
    DANGER_WORDS = ["free", "verify", "login", "prize",
                    "camera", "webcam", "winner", "claim", "reward", "urgent"]
    found_words = [w for w in DANGER_WORDS if w in url.lower()]
    if found_words:
        score += 20 * len(found_words)   # each bad word adds more risk
        reasons.append(f"Contains suspicious keyword(s): {', '.join(found_words)}")

    # ── Rule 5a: URL is very long ─────────────────────────────
    # Attackers pad URLs with junk to confuse users and filters.
    # A normal URL is rarely longer than 75 characters.
    if len(url) > 75:
        score += 15
        reasons.append(f"URL is very long ({len(url)} characters) — could be obfuscated")

    # ── Rule 5b: Too many hyphens ─────────────────────────────
    # Phishing domains often look like: free-prize-claim-now.com
    # More than 3 hyphens in a URL is unusual and suspicious.
    hyphen_count = url.count("-")
    if hyphen_count > 3:
        score += 10 * (hyphen_count - 3)   # penalise each extra hyphen
        reasons.append(f"Contains {hyphen_count} hyphens — looks like a fake domain")

    # ── Decide the final verdict ──────────────────────────────
    # Score 0–19  → Safe
    # Score 20–49 → Suspicious
    # Score 50+   → Dangerous
    if score >= 50:
        verdict = "Dangerous"
    elif score >= 20:
        verdict = "Suspicious"
    else:
        verdict = "Safe"

    # If no problems were found, add a positive message
    if not reasons:
        reasons.append("No known risk signals detected")

    return score, verdict, reasons


# ══════════════════════════════════════════════════════════════
# PAGE CONTENT — each block only renders when `page` matches
# ══════════════════════════════════════════════════════════════

# ── Shared page header helper ─────────────────────────────────
# We call this at the top of every page so the title and subtitle
# are consistent across all sections.
def page_header(title: str, subtitle: str = ""):
    st.markdown(f"# {title}")
    if subtitle:
        st.markdown(f"<p style='color:#a88fc8; margin-top:-0.6rem;'>{subtitle}</p>",
                    unsafe_allow_html=True)
    st.markdown("---")


# ══════════════════════════════════════════════════════════════
# 🏠 DASHBOARD
# ══════════════════════════════════════════════════════════════
if page == "🏠 Dashboard":
    page_header("🛡️ Suraksha Sakhi", "Women's Online Safety Dashboard — Cam Phishing Protection")

    # Description box explaining the purpose of the dashboard
    st.markdown("""
    <div class="desc-box">
        <strong>What is cam phishing?</strong> Cam phishing is an online trap where attackers
        trick people — especially young women and girls — into turning on their webcam or
        sharing private photos/videos, and then use that footage to blackmail or harass them.
        <br><br>
        <strong>Suraksha Sakhi</strong> monitors suspicious links, fake video-call invitations,
        and camera-access requests to keep you safe. All numbers below are simulated for
        demonstration purposes.
    </div>
    """, unsafe_allow_html=True)

    # ── KPI METRIC CARDS ─────────────────────────────────────
    # These four cards show the key safety numbers at a glance.
    # Counts = history table totals  +  anything checked via the Link Checker.
    st.markdown("### 📊 Today's Safety Overview")
    st.markdown(" ")

    # Count verdicts from the history DataFrame
    df_hist = st.session_state.link_history
    hist_total      = len(df_hist)
    hist_safe       = int((df_hist["Result"] == "Safe").sum())
    hist_suspicious = int((df_hist["Result"] != "Safe").sum())

    # Add the Link Checker widget counts on top
    total_checked    = hist_total      + st.session_state.extra_checked
    total_safe       = hist_safe       + st.session_state.extra_safe
    total_suspicious = hist_suspicious + st.session_state.extra_suspicious

    col1, col2, col3, col4 = st.columns(4)
    cards = [
        ("🔗", "Links Checked",   f"{total_checked:,}",    "URLs scanned today"),
        ("✅", "Safe Links",       f"{total_safe:,}",       "No threats found"),
        ("⚠️", "Suspicious Links", f"{total_suspicious:,}", "Flagged for review"),
        ("📷", "Camera Alerts",
         f"{int((st.session_state.cam_alerts['Risk']=='High').sum()):,}",
         "High-risk cam events today"),
    ]
    for col, (icon, label, value, footnote) in zip([col1, col2, col3, col4], cards):
        with col:
            st.markdown(f"""
            <div class="kpi-card">
                <h3>{icon} {label}</h3>
                <p>{value}</p>
                <span>{footnote}</span>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# 🔍 LINK CHECKER
# ══════════════════════════════════════════════════════════════
elif page == "🔍 Link Checker":
    page_header("🔍 Link Checker", "Instantly analyse a URL for cam phishing signals")

    st.markdown(
        "Paste any suspicious link below and click **Check Link** to analyse it "
        "using five simple rules. No internet connection is needed — "
        "everything runs on your device."
    )

    st.markdown('<div class="checker-box">', unsafe_allow_html=True)
    user_url = st.text_input(
        label="Paste a link here:",
        placeholder="e.g. http://192.168.1.1/free-prize-claim",
        help="Include the full URL starting with http:// or https://"
    )
    check_clicked = st.button("🔍 Check Link", type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

    # When button is clicked: run analysis and SAVE result to session_state.
    # We cannot display output inside the if-block because Streamlit reruns the
    # entire script after a button click — that would wipe the output.
    # Solution: save the result, then always render it from session_state below.
    if check_clicked:
        if not user_url.strip():
            st.session_state.last_result = {"error": True}
        else:
            score, verdict, reasons = check_link(user_url)
            st.session_state.extra_checked += 1
            if verdict == "Safe":
                st.session_state.extra_safe += 1
            else:
                st.session_state.extra_suspicious += 1
            st.session_state.last_result = {
                "error": False, "url": user_url.strip(),
                "score": score, "verdict": verdict, "reasons": reasons,
            }

    # Always render the saved result on every page load
    if st.session_state.last_result is not None:
        result = st.session_state.last_result
        if result.get("error"):
            st.warning("Please paste a link in the box above before clicking Check Link.")
        else:
            verdict = result["verdict"]
            score   = result["score"]
            reasons = result["reasons"]
            url     = result["url"]
            css_class = {
                "Safe": "verdict-safe", "Suspicious": "verdict-suspicious",
                "Dangerous": "verdict-dangerous",
            }[verdict]
            emoji = {"Safe": "✅", "Suspicious": "⚠️", "Dangerous": "🚨"}[verdict]
            reason_html = "".join(f"<li>{r}</li>" for r in reasons)
            st.markdown(f"""
            <div class="{css_class}">
                <strong>{emoji} Verdict: {verdict}</strong>
                &nbsp;&nbsp;|&nbsp;&nbsp;
                <strong>Risk Score: {score} / 100+</strong><br>
                <small style="opacity:0.75;">Checked: {url}</small>
                <ul style="margin:0.6rem 0 0 0; padding-left:1.4rem;">{reason_html}</ul>
            </div>
            """, unsafe_allow_html=True)
            if verdict == "Dangerous":
                st.error("🚨 **Do NOT open this link.** Block the sender and report it immediately.")
            elif verdict == "Suspicious":
                st.warning("⚠️ **Be very careful.** Avoid entering any personal information on this page.")
            else:
                st.success("✅ No major red flags found, but always stay alert online.")


# ══════════════════════════════════════════════════════════════
# 📋 LINK HISTORY
# ══════════════════════════════════════════════════════════════
elif page == "📋 Link History":
    page_header("📋 Link History", "20 most-recent links received across all platforms")

    st.markdown(
        "Click **Generate Sample Data** to load or refresh the fictional link records."
    )

    if st.button("🔄 Generate Sample Data"):
        st.session_state.link_history = make_history()

    # Filter dropdown
    result_filter = st.selectbox(
        "Filter by Result:",
        options=["All", "Safe", "Suspicious", "Dangerous"],
        key="result_filter",
    )
    if result_filter == "All":
        filtered_history = st.session_state.link_history
    else:
        filtered_history = st.session_state.link_history[
            st.session_state.link_history["Result"] == result_filter
        ]

    # Colour-code the Result column
    def colour_result(val):
        if val == "Dangerous":
            return "background-color: #3b0a0a; color: #ffaaaa;"
        elif val == "Suspicious":
            return "background-color: #2b2200; color: #ffd98a;"
        else:
            return "background-color: #0d2b1a; color: #aef5c8;"

    styled_df = (
        filtered_history.style
        .map(colour_result, subset=["Result"])
        .set_properties(**{"background-color": "#1c1c30", "color": "#e8e8f0", "border-color": "#2e2e4a"})
        .set_table_styles([{"selector": "th", "props": [
            ("background-color", "#16162a"), ("color", "#a88fc8"),
            ("font-size", "0.82rem"), ("text-transform", "uppercase"),
        ]}])
    )
    st.dataframe(styled_df, use_container_width=True, hide_index=True)

    # Summary metrics (always from full unfiltered data)
    lh = st.session_state.link_history
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Records", len(lh))
    m2.metric("🚨 Dangerous",  int((lh["Result"] == "Dangerous").sum()))
    m3.metric("⚠️ Suspicious", int((lh["Result"] == "Suspicious").sum()))
    m4.metric("✅ Safe",        int((lh["Result"] == "Safe").sum()))


# ══════════════════════════════════════════════════════════════
# 📷 CAMERA ALERTS
# ══════════════════════════════════════════════════════════════
elif page == "📷 Camera Alerts":
    page_header("📷 Camera Safety Alerts", "Simulated camera, microphone & gallery permission events")

    st.markdown(
        "High-risk events are the most urgent — review them first. "
        "Click **Generate Camera Alerts** to refresh the data."
    )

    if st.button("🔄 Generate Camera Alerts"):
        st.session_state.cam_alerts = make_cam_alerts()

    # Filter dropdown
    risk_filter = st.selectbox(
        "Filter by Risk Level:",
        options=["All", "High", "Medium", "Low"],
        key="risk_filter",
    )
    if risk_filter == "All":
        filtered_cam = st.session_state.cam_alerts
    else:
        filtered_cam = st.session_state.cam_alerts[
            st.session_state.cam_alerts["Risk"] == risk_filter
        ]

    # Colour-code the Risk column
    def colour_risk(val):
        if val == "High":
            return "background-color: #3b0a0a; color: #ffaaaa;"
        elif val == "Medium":
            return "background-color: #2b1800; color: #ffcc88;"
        else:
            return "background-color: #0d2b1a; color: #aef5c8;"

    styled_cam = (
        filtered_cam.style
        .map(colour_risk, subset=["Risk"])
        .set_properties(**{"background-color": "#1c1c30", "color": "#e8e8f0", "border-color": "#2e2e4a"})
        .set_table_styles([{"selector": "th", "props": [
            ("background-color", "#16162a"), ("color", "#a88fc8"),
            ("font-size", "0.82rem"), ("text-transform", "uppercase"),
        ]}])
    )
    st.dataframe(styled_cam, use_container_width=True, hide_index=True)

    ca_df = st.session_state.cam_alerts
    ca1, ca2, ca3, ca4 = st.columns(4)
    ca1.metric("Total Events",   len(ca_df))
    ca2.metric("🔴 High Risk",   int((ca_df["Risk"] == "High").sum()))
    ca3.metric("🟠 Medium Risk", int((ca_df["Risk"] == "Medium").sum()))
    ca4.metric("🟢 Low Risk",    int((ca_df["Risk"] == "Low").sum()))

    st.markdown("""
    <div class="desc-box" style="margin-top:1rem; border-left-color:#9b59b6;">
        <strong>⚠️ Simulation Notice</strong><br>
        All events are <strong>entirely fictional</strong>. A real implementation would use
        phone OS permission APIs (Android Accessibility Service / iOS Privacy Report).
        A suspicious pattern does <em>not</em> automatically prove an attack — always verify
        through official channels before taking action.
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# 🖼️ PHOTO SAFETY
# ══════════════════════════════════════════════════════════════
elif page == "🖼️ Photo Safety":
    page_header("🖼️ Photo Safety", "Check & remove hidden metadata from your photos")

    st.markdown("""
    <div class="desc-box">
        <strong>Why is hidden photo data risky?</strong><br>
        Every photo taken with a phone or camera can contain invisible data called
        <strong>EXIF metadata</strong>, which often includes:<br>
        <ul style="margin:0.4rem 0 0 0; padding-left:1.4rem;">
            <li><strong>GPS location</strong> — exact street or home address where the photo was taken.</li>
            <li><strong>Device model</strong> — brand and model of your phone or camera.</li>
            <li><strong>Date and time</strong> — when the photo was taken.</li>
        </ul><br>
        Attackers can extract this data in seconds using free online tools.
        Use <strong>Make Safe to Share</strong> below to strip all hidden data.
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload a photo to check its hidden metadata:",
        type=["jpg", "jpeg", "png"],
        help="Your photo is processed in memory only — it is never uploaded to any server.",
    )

    if uploaded_file is not None:
        original_image = Image.open(uploaded_file)
        img_col, info_col = st.columns([1, 2])
        with img_col:
            st.image(original_image, caption="Uploaded photo", use_container_width=True)

        # Extract EXIF — _getexif() may not exist on PNGs, so check first
        raw_exif = {}
        if hasattr(original_image, "_getexif") and original_image._getexif():
            raw_exif = original_image._getexif()
        named_exif = {TAGS.get(k, str(k)): v for k, v in raw_exif.items()}

        with info_col:
            st.markdown("#### 🔍 Metadata Found")
            if not named_exif:
                st.success("✅ No hidden EXIF metadata found. Safe to share!")
            else:
                if "GPSInfo" in named_exif:
                    st.error("🚨 **GPS location data detected!** Do NOT share without removing metadata.")
                else:
                    st.success("✅ No GPS location found.")
                device_make  = named_exif.get("Make", "")
                device_model = named_exif.get("Model", "")
                if device_make or device_model:
                    st.warning(f"📱 **Device info:** {device_make} {device_model}".strip()
                               + "  \nThis tells others what phone or camera you use.")
                else:
                    st.info("📱 No device model information found.")
                date_taken = named_exif.get("DateTimeOriginal", named_exif.get("DateTime", ""))
                if date_taken:
                    st.warning(f"📅 **Date & time:** {date_taken}  \nThis reveals when the photo was taken.")
                else:
                    st.info("📅 No date/time information found.")
                with st.expander("📋 See all hidden EXIF fields"):
                    exif_rows = [
                        {"Field": k,
                         "Value": "(location data — see warning above)" if k == "GPSInfo" else str(v)[:120]}
                        for k, v in named_exif.items()
                    ]
                    st.dataframe(pd.DataFrame(exif_rows), use_container_width=True, hide_index=True)

        st.markdown("#### 🧹 Make Safe to Share")
        st.markdown("Creates a clean copy with **all metadata removed**. Your original file is never changed.")

        if st.button("🧹 Make Safe to Share"):
            clean_buffer = io.BytesIO()
            original_image.convert("RGB").save(clean_buffer, format="JPEG", quality=95)
            clean_buffer.seek(0)
            st.image(clean_buffer, caption="✅ Clean photo (no metadata)", use_container_width=True)
            clean_buffer.seek(0)
            st.download_button(
                label="⬇️ Download Clean Photo",
                data=clean_buffer,
                file_name="safe_" + uploaded_file.name.rsplit(".", 1)[0] + ".jpg",
                mime="image/jpeg",
            )
            st.success("✅ Metadata removed. This copy has no GPS, device info, or date embedded.")


# ══════════════════════════════════════════════════════════════
# 📊 CHARTS
# ══════════════════════════════════════════════════════════════
elif page == "📊 Charts":
    page_header("📊 Charts & Filters", "Spot patterns in the safety data at a glance")

    if len(st.session_state.link_history) == 0:
        st.info("📂 No data yet. Go to Link History and click Generate Sample Data first.")
    else:
        lh = st.session_state.link_history
        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            st.markdown("**Link Results Breakdown**")
            result_counts = (
                lh["Result"].value_counts()
                .reindex(["Safe", "Suspicious", "Dangerous"], fill_value=0)
            )
            st.bar_chart(result_counts)
            st.caption(
                "How many of the 20 recent links were safe vs risky. "
                "A healthy pattern has mostly Safe bars."
            )

        with chart_col2:
            st.markdown("**Risky Links by Source**")
            risky = lh[lh["Result"] != "Safe"]
            if len(risky) == 0:
                st.success("No risky links in the current data.")
            else:
                st.bar_chart(risky["Source"].value_counts())
                st.caption(
                    "Which platform sent the most suspicious or dangerous links. "
                    "A tall bar means that platform is being actively targeted."
                )


# ══════════════════════════════════════════════════════════════
# ❓ HELP & TIPS
# ══════════════════════════════════════════════════════════════
elif page == "❓ Help & Tips":
    page_header("❓ Help & Tips", "What to do if you're targeted, and how to stay safe")

    # ── What To Do If You're Targeted ────────────────────────
    st.markdown("### 🆘 What To Do If You're Targeted")
    st.markdown("""
    <div class="desc-box" style="border-left-color:#e91e8c;">
        If someone is threatening you with photos or videos, or pressuring you online,
        please know: <strong>you are not alone, and it is not your fault.</strong>
        Follow the steps below and reach out for help.
    </div>
    """, unsafe_allow_html=True)

    STEPS = [
        ("1️⃣  Stay Calm — It Is Not Your Fault",
         "Take a deep breath. What happened to you is a crime committed by someone else. "
         "You do not need to feel ashamed. Help is available. Act carefully and do not panic."),
        ("2️⃣  Do Not Pay Money or Send More Photos",
         "If someone demands money, gift cards, or more photos or videos, **do not comply**. "
         "Paying does not make them stop — it usually makes things worse."),
        ("3️⃣  Take Screenshots — Do Not Delete the Chat",
         "Before blocking anyone, screenshot the threatening messages, the links they sent, "
         "and their profile page. Save these to a safe place. "
         "**Do not delete the conversation** — it may be needed for a police report."),
        ("4️⃣  Block and Report on the Platform",
         "Block the person, then use the platform's built-in Report feature:\n"
         "- **WhatsApp** → long-press the chat → Report\n"
         "- **Instagram** → profile → ⋯ → Report\n"
         "- **Telegram** → profile → Report\n"
         "- **Email** → Mark as spam / Report phishing"),
        ("5️⃣  Tell a Trusted Person",
         "Tell a parent, older sibling, close friend, or teacher. "
         "You do not have to go through this alone. Talking about it is brave."),
        ("6️⃣  Report to the Police or Cybercrime Helpline",
         "- 🌐 **Online:** [cybercrime.gov.in](https://cybercrime.gov.in)\n"
         "- 📞 **Helpline:** Call **1930** (National Cybercrime, 24×7)\n"
         "- 🚨 **Emergency:** Call **112**\n\nYou can report anonymously."),
    ]
    for title, body in STEPS:
        with st.expander(title):
            st.markdown(body)

    st.markdown("""
    <div class="desc-box" style="margin-top:1rem; border-left-color:#7878a0; font-size:0.85rem;">
        <strong>Note:</strong> General awareness guidance only — not legal advice.
        For formal legal help, contact a qualified lawyer or your local police station.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Safety Tips ───────────────────────────────────────────
    st.markdown("### 💡 Safety Tips")
    st.markdown("Small habits that make a big difference in keeping you safe online.")

    TIPS = [
        ("📷", "Cover your camera when not in use",
         "Use a sticker or slider over your webcam/phone camera when not on a call."),
        ("🔗", "Don't open unknown video-call links",
         "Verify who sent a video-call link before clicking — especially from WhatsApp, SMS, or email."),
        ("🔒", "Check app permissions regularly",
         "Settings → Privacy → Camera/Microphone. Remove access for any app that doesn't need it."),
        ("🙅", "Don't share personal photos with strangers",
         "Never send photos or videos to someone you've only met online — relationships can be faked."),
        ("📍", "Turn off location tagging in your camera",
         "Camera settings → turn off 'Save location' / 'Geo-tagging' to hide your address from photos."),
        ("🔑", "Use strong passwords and two-step verification",
         "12+ characters with letters, numbers & symbols. Enable 2FA on every important account."),
    ]
    tip_col1, tip_col2 = st.columns(2)
    for i, (emoji, title, detail) in enumerate(TIPS):
        col = tip_col1 if i < 3 else tip_col2
        with col:
            st.markdown(f"""
            <div style="background-color:#1c1c30;border:1px solid #2e2e4a;
                border-left:4px solid #9b59b6;border-radius:10px;
                padding:1rem 1.2rem;margin-bottom:0.9rem;">
                <p style="margin:0 0 0.3rem 0;font-size:1.05rem;">
                    {emoji} <strong style="color:#e0d0f5;">{title}</strong>
                </p>
                <p style="margin:0;font-size:0.88rem;color:#a8a8c8;line-height:1.6;">{detail}</p>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# ℹ️ ABOUT
# ══════════════════════════════════════════════════════════════
elif page == "ℹ️ About":
    page_header("ℹ️ About Suraksha Sakhi", "Project overview, features, and future scope")

    # ── Problem statement ─────────────────────────────────────
    st.markdown("### 🔴 The Problem")
    st.markdown("""
    <div class="desc-box" style="border-left-color:#e74c3c;">
        Young women and girls are increasingly targeted by <strong>cam phishing</strong> —
        a form of online blackmail where attackers:<br>
        <ul style="margin:0.4rem 0 0 0; padding-left:1.4rem;">
            <li>Send fake video-call links or friend requests to gain trust</li>
            <li>Trick victims into turning on their camera or sharing private photos</li>
            <li>Use that footage to demand money, more photos, or sexual favours</li>
            <li>Threaten to share the footage with family, friends, or publicly</li>
        </ul><br>
        This is a growing crime across India and globally. Most victims do not report it
        out of shame or fear — even though it is entirely the attacker's fault.
    </div>
    """, unsafe_allow_html=True)

    # ── What Suraksha Sakhi does ──────────────────────────────
    st.markdown("### 🛡️ What Suraksha Sakhi Does")
    st.markdown("""
    <div class="desc-box" style="border-left-color:#9b59b6;">
        Suraksha Sakhi is a <strong>women's online safety dashboard</strong> that demonstrates
        how technology can help detect, visualise, and respond to cam phishing threats.<br><br>
        <strong>Current features (prototype):</strong>
        <ul style="margin:0.4rem 0 0 0; padding-left:1.4rem;">
            <li>🔍 <strong>Link Checker</strong> — analyses URLs using 5 rule-based checks</li>
            <li>📋 <strong>Link History</strong> — table of 20 fictional recent links with filters</li>
            <li>📷 <strong>Camera Alerts</strong> — simulated camera/mic permission events</li>
            <li>🖼️ <strong>Photo Safety</strong> — reads and strips EXIF metadata from photos</li>
            <li>📊 <strong>Charts</strong> — bar charts showing threat patterns by result and source</li>
            <li>❓ <strong>Help & Tips</strong> — step-by-step guidance and 6 safety habits</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # ── Prototype note ────────────────────────────────────────
    st.markdown("### 📝 Prototype Note")
    st.markdown("""
    <div class="desc-box" style="border-left-color:#f39c12;">
        This is a <strong>working prototype built for demonstration purposes</strong>.<br>
        <ul style="margin:0.4rem 0 0 0; padding-left:1.4rem;">
            <li>All link history and camera alert data is <strong>entirely fictional</strong></li>
            <li>The link checker uses simple Python rules — not machine learning or real APIs</li>
            <li>No real network requests are made; no data is stored or sent anywhere</li>
            <li>Photo metadata is processed in browser memory only — files are never uploaded</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # ── Future scope ──────────────────────────────────────────
    st.markdown("### 🚀 Future Scope")

    future_items = [
        ("📱", "Always-active Android app",
         "A background Android service that monitors incoming links in real time, "
         "without the user needing to open a dashboard manually."),
        ("🎥", "Real camera & microphone permission monitoring",
         "Integration with Android Accessibility Service or iOS Privacy Report APIs "
         "to detect when any app accesses the camera or microphone without the user's knowledge."),
        ("🖼️", "Gallery protection",
         "Automatic scanning of the photo gallery for images with GPS metadata, "
         "and a one-tap option to strip location data from all photos before sharing."),
        ("🔗", "Link scanner inside messaging apps",
         "A keyboard extension or share-sheet plugin that automatically scans links "
         "received in WhatsApp, Instagram, Telegram, and SMS before the user taps them."),
    ]
    for emoji, title, detail in future_items:
        with st.expander(f"{emoji}  {title}"):
            st.markdown(detail)

    st.markdown("---")
    st.markdown("""
    <div class="desc-box" style="border-left-color:#7878a0; font-size:0.85rem;">
        Built with Python · Streamlit · Pandas · Pillow &nbsp;|&nbsp;
        Prototype with fictional data &nbsp;|&nbsp;
        Made with ❤️ for women's digital safety
    </div>
    """, unsafe_allow_html=True)


# ── SHARED FOOTER ─────────────────────────────────────────────
# Shown on every page below the content
st.markdown(" ")
st.markdown(" ")
st.caption("⚠️ All data shown is fictional and for demonstration only. "
           "Suraksha Sakhi does not connect to any real network or database.")
