
import os
from modules.cloud_storage import upload_file

source = r"C:\BackupSource\cloud_test.txt"

if os.path.isfile(source):
    upload_file(source, "cloud_test.txt")
    print("Upload test completed.")
else:
    print("Test file not found:", source)
