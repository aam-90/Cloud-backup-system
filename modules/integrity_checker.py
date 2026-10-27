
import hashlib
import os


def calculate_sha256(file_path):
    """Calculate the SHA-256 hash of a file."""
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def verify_backup(source_path, backup_path):
    """Compare the source file with its backup."""
    if not os.path.isfile(source_path):
        return False, "Source file does not exist."

    if not os.path.isfile(backup_path):
        return False, "Backup file does not exist."

    source_hash = calculate_sha256(source_path)
    backup_hash = calculate_sha256(backup_path)

    if source_hash == backup_hash:
        return True, "Backup integrity verified. Files match."

    return False, "Integrity check failed. Files differ."
