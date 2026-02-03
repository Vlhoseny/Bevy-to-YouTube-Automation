# Bevy-to-YouTube-Automation
# 🎥 Bevy to YouTube Automation (Colab Edition)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/)

A powerful Python automation tool optimized for **Google Colab**. It seamlessly downloads session recordings from **Bevy** (virtual event platform) and uploads them directly to a **YouTube** channel via the YouTube Data API v3.

> **Why use this on Colab?**
> * **Zero Bandwidth:** No need to download 2GB+ files to your local machine.
> * **High Speed:** leverages Google's cloud infrastructure for lightning-fast transfers.
> * **No Environment Setup:** Runs instantly in the browser without installing Python locally.

---

## 🚀 Features

* **Cloud-Native:** Designed specifically to run on Google Colab free tier.
* **Smart Downloading:** Handles large file downloads from AWS S3 (Bevy) with a progress bar.
* **Auto-Authentication:** Automatically generates the required `client_secret.json` for OAuth 2.0.
* **Direct Upload:** Uploads video files to YouTube with full metadata (Title, Description, Tags, Privacy Status).
* **Fixes Colab Constraints:** Includes built-in workarounds for OAuth redirects (`localhost` issues) and HTTPS requirements unique to the Colab environment.

---

## 🛠️ Prerequisites

Before running the notebook, you need to set up a project on Google Cloud Platform:

1.  **Create a Project** on [Google Cloud Console](https://console.cloud.google.com/).
2.  **Enable API:** Search for and enable **YouTube Data API v3**.
3.  **Configure OAuth Consent Screen:**
    * User Type: `External`
    * **Test Users:** Add the email address that manages the YouTube channel (Crucial to avoid "Access Blocked" errors).
4.  **Create Credentials:**
    * Create **OAuth 2.0 Client ID**.
    * Application Type: `Desktop App`.
    * Copy your `Client ID` and `Client Secret`.

---

## ⚙️ Configuration

Open the script in Google Colab and update the **Configuration Section** at the top:

```python
# 1. Update the Bevy video URL (Links expire quickly!)
VIDEO_URL = "https://prod-us-east-1... (Your Bevy Link)"

# 2. Update YouTube Metadata
YOUTUBE_TITLE = 'Your Session Title'
YOUTUBE_DESC = 'Uploaded via Automation Tool'
YOUTUBE_TAGS = ['GDG', 'Tech', 'Event']

# 3. Update OAuth Credentials
client_config = {
    "installed": {
        "client_id": "YOUR_CLIENT_ID_HERE",
        "client_secret": "YOUR_CLIENT_SECRET_HERE",
        # ... keep the rest as is
    }
}
