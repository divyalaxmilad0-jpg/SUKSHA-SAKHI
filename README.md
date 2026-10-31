# 🛡️ Suraksha Sakhi — Women's Online Safety Dashboard

A beginner-friendly Streamlit prototype that demonstrates how technology can
help detect, visualise, and respond to **cam phishing** and online threats
targeting women and girls.

> **All data in this app is fictional and for demonstration purposes only.**
> No real network requests are made. No data is stored or sent anywhere.

---

## 📋 What Is Cam Phishing?

Cam phishing is an online trap where attackers trick people — especially young
women and girls — into turning on their webcam or sharing private photos/videos,
and then use that footage to blackmail or harass them.

---

## ✨ Features

| Page | What it does |
|---|---|
| 🏠 **Dashboard** | Four live KPI cards: Links Checked, Safe Links, Suspicious Links, Camera Alerts |
| 🔍 **Link Checker** | Paste any URL; five rule-based checks flag shorteners, HTTP, IP addresses, bad keywords, long URLs, and hyphens |
| 📋 **Link History** | 20 fictional link records with a Result filter and colour-coded table |
| 📷 **Camera Alerts** | 10 simulated camera/mic/gallery permission events with a Risk filter |
| 🖼️ **Photo Safety** | Upload a JPG/PNG, read EXIF metadata, detect GPS location, and download a clean metadata-free copy |
| 📊 **Charts** | Bar chart of link results breakdown + risky links by source platform |
| ❓ **Help & Tips** | 6-step guide for targeted victims (helpline 1930, cybercrime.gov.in) + 6 safety tips |
| ℹ️ **About** | Problem statement, prototype note, and future scope |

---

## 🚀 How to Run

### 1. Install Python
Make sure Python 3.8 or newer is installed.
Download from: https://www.python.org/downloads/

### 2. Install the required libraries
Open a terminal (Command Prompt or PowerShell) and navigate to this folder:

```
cd "c:\IBM NEW PROJECT CYBERSECURITY CAM PHISHING"
```

Install dependencies (only needed once):

```
pip install -r requirements.txt
```

### 3. Run the app

```
python -m streamlit run app.py
```

Your browser will open automatically at **http://localhost:8501**

---

## 📦 Requirements

```
streamlit
pandas
pillow
```

Listed in [`requirements.txt`](requirements.txt).

---

## 🗂️ Project Structure

```
app.py              — Single-file Streamlit app (all code and comments)
requirements.txt    — Python package dependencies
README.md           — This file
```

---

## 🔭 Future Scope

- 📱 **Always-active Android app** — background service that monitors links in real time
- 🎥 **Real camera & microphone monitoring** — Android Accessibility Service / iOS Privacy Report
- 🖼️ **Gallery protection** — auto-scan and strip GPS metadata from all photos
- 🔗 **Link scanner inside messaging apps** — keyboard extension for WhatsApp, Telegram, SMS

---

## ⚠️ Disclaimer

This is a **working prototype built for demonstration purposes**.
All link history and camera alert data is entirely fictional.
The link checker uses simple Python rules — not machine learning or real APIs.
Photo metadata is processed in browser memory only — files are never uploaded.

---

*Made with ❤️ for women's digital safety*
