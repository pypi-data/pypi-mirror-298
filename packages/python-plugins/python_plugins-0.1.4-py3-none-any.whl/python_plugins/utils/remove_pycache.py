import os
import shutil

def remove_pycache(dir_path):
    for root, dirs, files in os.walk(dir_path):
        if "venv" in root or "git" in root:
            continue
        for dir in dirs:
            if dir == "__pycache__":
                pycache_path = os.path.join(root, dir)
                print(f"Removing {pycache_path}")
                shutil.rmtree(pycache_path)

