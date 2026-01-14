
import ftplib
import os
import sys

# Configuration
FTP_HOST = "ftpupload.net"
FTP_USER = "if0_40626556"
FTP_PASS = "tE7iRH3rAG"
LOCAL_FRONTEND = "out"
LOCAL_BACKEND = "php-backend"
REMOTE_ROOT = "htdocs"

def upload_directory(ftp, local_path, remote_path):
    print(f"Uploading directory {local_path} to {remote_path}...")
    
    # Create remote directory if it doesn't exist
    try:
        ftp.mkd(remote_path)
    except ftplib.error_perm:
        pass # Directory probably exists

    # Walk through local directory
    items = os.listdir(local_path)
    for item in items:
        local_item = os.path.join(local_path, item)
        remote_item = f"{remote_path}/{item}"
        
        if os.path.isdir(local_item):
            # Recursively upload subdirectory
            upload_directory(ftp, local_item, remote_item)
        else:
            # Upload file
            print(f"  Uploading {item}...")
            with open(local_item, "rb") as fp:
                try:
                    ftp.storbinary(f"STOR {remote_item}", fp)
                except Exception as e:
                    print(f"Failed to upload {item}: {e}")

def main():
    print(f"Connecting to {FTP_HOST} as {FTP_USER}...")
    try:
        ftp = ftplib.FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        print("Connected successfully.")
        
        # Determine strict mode: checking if htdocs exists
        files = ftp.nlst()
        if "htdocs" not in files:
            print("Warning: 'htdocs' folder not found in root. Creating it.")
            ftp.mkd("htdocs")
        
        # Upload Frontend (Contents of 'out' go directly into 'htdocs')
        # We need to list 'out' contents and upload them to 'htdocs'
        print("Starting Frontend Upload...")
        for item in os.listdir(LOCAL_FRONTEND):
            local_item = os.path.join(LOCAL_FRONTEND, item)
            remote_item = f"{REMOTE_ROOT}/{item}"
            
            if os.path.isdir(local_item):
                upload_directory(ftp, local_item, remote_item)
            else:
                print(f"  Uploading {item}...")
                with open(local_item, "rb") as fp:
                    ftp.storbinary(f"STOR {remote_item}", fp)

        # Upload Backend (Goes into 'htdocs/php-backend')
        print("Starting Backend Upload...")
        upload_directory(ftp, LOCAL_BACKEND, f"{REMOTE_ROOT}/php-backend")
        
        print("Deployment completed successfully!")
        ftp.quit()
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
