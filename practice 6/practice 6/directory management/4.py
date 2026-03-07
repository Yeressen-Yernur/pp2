import shutil
import os
os.makedirs("backup", exist_ok=True)
shutil.copy("sample.txt", "backup/sample.txt")