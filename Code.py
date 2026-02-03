import os
import json
import requests
from tqdm import tqdm
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.colab import userdata

# ==========================================
# 1. Configuration & Setup
# ==========================================

# [ACTION REQUIRED]: Update this URL before every run (Bevy links expire quickly).
# Do not commit private/expired links to GitHub.
VIDEO_URL = "PUT_YOUR_BEVY_LINK_HERE"

# Local temporary filename
VIDEO_FILENAME = "bevy_session.mp4"

# YouTube Metadata
YOUTUBE_TITLE = 'Bevy Session - GDG'
YOUTUBE_DESC = 'Session uploaded automatically via Google Colab Automation Script.'
YOUTUBE_TAGS = ['GDG', 'Bevy', 'Tech Session', 'Google Developer Groups']
YOUTUBE_CATEGORY_ID = '22'  # 22 = People & Blogs, 28 = Science & Technology

# ==========================================
# 2. Secure Credentials Handling
# ==========================================
print("🔐 Fetching credentials from Colab Secrets...")

try:
    # Attempt to retrieve secrets from Google Colab environment
    CLIENT_ID = userdata.get('GOOGLE_CLIENT_ID')
    CLIENT_SECRET = userdata.get('GOOGLE_CLIENT_SECRET')
except ImportError:
    # Fallback if not running in Colab (e.g., local machine env vars)
    CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')

# Validation check
if not CLIENT_ID or not CLIENT_SECRET:
    raise ValueError(
        "❌ Credentials not found! \n"
        "Please go to the 'Secrets' tab (Key icon) in Colab and add:\n"
        "1. GOOGLE_CLIENT_ID\n"
        "2. GOOGLE_CLIENT_SECRET\n"
        "Make sure to enable 'Notebook access' for them."
    )

# Prepare client configuration dictionary
client_config = {
    "installed": {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "redirect_uris": ["http://localhost"]
    }
}

# [FIX]: Allow HTTP traffic for OAuth lib to accept the localhost redirect in Colab
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Generate the 'client_secret.json' file temporarily
with open('client_secret.json', 'w') as f:
    json.dump(client_config, f)


# ==========================================
# 3. Download Function
# ==========================================
def download_video():
    """Downloads the video file from the provided Bevy URL."""
    
    if os.path.exists(VIDEO_FILENAME):
        print(f"✅ File '{VIDEO_FILENAME}' already exists. Skipping download.")
        return True

    print(f"⬇️ Starting download from Bevy...")
    try:
        response = requests.get(VIDEO_URL, stream=True)
        
        if response.status_code == 200:
            total_size = int(response.headers.get('content-length', 0))
            
            with open(VIDEO_FILENAME, 'wb') as file, tqdm(
                desc="Downloading", 
                total=total_size, 
                unit='iB', 
                unit_scale=True, 
                unit_divisor=1024,
            ) as bar:
                for data in response.iter_content(1024):
                    bar.update(len(data))
                    file.write(data)
            
            print("\n✅ Download completed successfully!")
            return True
        else:
            print(f"\n❌ Download Failed! Status Code: {response.status_code}")
            print("⚠️ Hint: The Bevy URL might have expired. Please retrieve a fresh link.")
            return False
            
    except Exception as e:
        print(f"❌ Error during download: {e}")
        return False


# ==========================================
# 4. Upload Function
# ==========================================
def upload_to_youtube():
    """Authenticates and uploads the video to YouTube."""
    
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
    
    print("\n🔐 Initializing YouTube Authentication...")
    
    flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
    flow.redirect_uri = 'http://localhost'
    
    # Generate Authorization URL
    auth_url, _ = flow.authorization_url(prompt='consent')

    print("-" * 60)
    print("👇 MANUAL AUTHENTICATION REQUIRED:")
    print(f"1. Click the URL below: \n{auth_url}")
    print("2. Log in with your authorized email and 'Allow' access.")
    print("3. When redirected to the broken 'localhost' page, COPY the full URL.")
    print("-" * 60)
    
    auth_response = input("🔗 Paste the full localhost URL here and press Enter: ")
    
    try:
        flow.fetch_token(authorization_response=auth_response)
        creds = flow.credentials
    except Exception as e:
        print(f"\n❌ Authentication failed. Did you copy the full URL? Error: {e}")
        return

    print("\n🚀 Authentication successful! Uploading to YouTube...")
    
    youtube = build('youtube', 'v3', credentials=creds)

    body = {
        'snippet': {
            'title': YOUTUBE_TITLE,
            'description': YOUTUBE_DESC,
            'tags': YOUTUBE_TAGS,
            'categoryId': YOUTUBE_CATEGORY_ID
        },
        'status': {
            'privacyStatus': 'private', # Private by default for safety
            'selfDeclaredMadeForKids': False
        }
    }

    media = MediaFileUpload(VIDEO_FILENAME, chunksize=-1, resumable=True)
    
    request = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        media_body=media
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"📊 Upload Progress: {int(status.progress() * 100)}%")

    print(f"\n✅ Upload Complete!")
    print(f"📺 Watch Video: https://youtu.be/{response['id']}")


# ==========================================
# 5. Main Execution
# ==========================================
if __name__ == "__main__":
    # Ensure URL is set
    if "PUT_YOUR_BEVY_LINK_HERE" in VIDEO_URL:
        print("❌ Error: You forgot to update the 'VIDEO_URL' variable!")
    else:
        if download_video():
            upload_to_youtube()
