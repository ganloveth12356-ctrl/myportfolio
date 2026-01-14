
import ftplib
import time
import sys
import os
import urllib.request as request

# Configuration
FTP_HOST = "ftpupload.net"
FTP_USER = "if0_40626556"
FTP_PASS = "tE7iRH3rAG"
FILES_TO_UPLOAD = ["UPLOAD_THIS.zip", "unzip.php"]
REMOTE_DIR = "htdocs"

def connect_ftp():
    ftp = ftplib.FTP()
    ftp.set_debuglevel(1)
    print(f"Connecting to {FTP_HOST}...")
    ftp.connect(FTP_HOST, 21, timeout=30)
    print(f"Logging in as {FTP_USER}...")
    ftp.login(FTP_USER, FTP_PASS)
    return ftp

def upload_file(filename):
    max_retries = 5
    for attempt in range(max_retries):
        ftp = None
        try:
            ftp = connect_ftp()
            
            # Navigate to htdocs
            try:
                ftp.cwd(REMOTE_DIR)
            except:
                print(f"Could not change to {REMOTE_DIR}, assuming root.")

            print(f"Uploading {filename} (Attempt {attempt+1}/{max_retries})...")
            with open(filename, "rb") as fp:
                ftp.storbinary(f"STOR {filename}", fp)
            
            print(f"SUCCESS: {filename} uploaded.")
            ftp.quit()
            return True

        except ftplib.all_errors as e:
            print(f"Error on attempt {attempt+1}: {e}")
            if "530" in str(e):
                print("Access denied (likely too many connections). Waiting 15s...")
                time.sleep(15)
            else:
                print("Retrying in 5s...")
                time.sleep(5)
            
            try:
                if ftp: ftp.quit()
            except:
                pass
    
    return False

def trigger_unzipper():
    url = "http://eing.42web.io/unzip.php"
    print(f"Triggering unzipper at {url}...")
    try:
        response = request.urlopen(url)
        print(f"Response: {response.status}")
        content = response.read().decode('utf-8')
        if "Success" in content:
            print("DEPLOYMENT SUCCESSFUL! Files extracted.")
        else:
            print("Unzipper ran but check output.")
            print(content[:200])
    except Exception as e:
        print(f"Failed to trigger unzipper: {e}")

def main():
    print("Starting Smart Deployment...")
    
    for file in FILES_TO_UPLOAD:
        if not os.path.exists(file):
            print(f"Error: {file} missing locally!")
            return
        
        if not upload_file(file):
            print(f"CRITICAL: Failed to upload {file} after retries.")
            return

    print("All files uploaded. Triggering installation...")
    # Give it a second to settle
    time.sleep(2)
    trigger_unzipper()

if __name__ == "__main__":
    main()
