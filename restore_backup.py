
import os
import shutil


def restore_file(backup_path, restore_path):
    if not os.path.isfile(backup_path):
        print("Error: Backup file not found.")
        return

    try:
        os.makedirs(os.path.dirname(restore_path), exist_ok=True)
        shutil.copy2(backup_path, restore_path)
        print("File restored successfully:", restore_path)

    except OSError as error:
        print("Restore failed:", error)


if __name__ == "__main__":
    backup = r"C:\CloudBackup\BackupFiles\test.txt"
    restored = r"C:\RestoredFiles\test.txt"

    restore_file(backup, restored)
