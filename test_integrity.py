
from modules.integrity_checker import verify_backup

source = r"C:\BackupSource\test.txt"
backup = r"C:\CloudBackup\BackupFiles\test.txt"

success, message = verify_backup(source, backup)
print(message)
