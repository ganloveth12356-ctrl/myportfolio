
import os
import shutil

# Configuration
DIST_DIR = 'out'
OLD_DIR = '_next'
NEW_DIR = 'assets'

def replace_in_file(filepath, old_str, new_str):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if old_str in content:
            new_content = content.replace(old_str, new_str)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
    return False

def main():
    print(f"Starting post-build fix: Renaming {OLD_DIR} to {NEW_DIR}...")
    
    # 1. Rename directory
    old_path = os.path.join(DIST_DIR, OLD_DIR)
    new_path = os.path.join(DIST_DIR, NEW_DIR)
    
    if os.path.exists(new_path):
        shutil.rmtree(new_path)
        
    if os.path.exists(old_path):
        os.rename(old_path, new_path)
        print(f"Renamed {old_path} to {new_path}")
    else:
        print(f"Warning: {old_path} not found!")

    # 2. Replace references in all files
    count = 0
    for root, dirs, files in os.walk(DIST_DIR):
        for file in files:
            if file.endswith(('.html', '.css', '.js', '.json')):
                filepath = os.path.join(root, file)
                # Replace /_next/ with /assets/
                if replace_in_file(filepath, f"/{OLD_DIR}/", f"/{NEW_DIR}/"):
                    count += 1
    
    print(f"Updated references in {count} files.")
    print("Post-build fix completed.")

if __name__ == "__main__":
    main()
