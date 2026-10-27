
import os
import shutil
from datetime import datetime

from modules.cloud_storage import upload_file
from modules.integrity_checker import verify_backup


def write_log(backup_folder, message):
    log_file = os.path.join(
        os.path.dirname(backup_folder),
        "backup_history.log"
    )

    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(log_file, "a", encoding="utf-8") as file:
        file.write(f"[{timestamp}] {message}\n")


def process_changes(source_folder, backup_folder, changes):
    for change_type, relative_path in changes:
        source_path = os.path.join(source_folder, relative_path)
        destination_path = os.path.join(backup_folder, relative_path)

        if change_type in ("NEW", "MODIFIED"):
            if not os.path.isfile(source_path):
                continue

            try:
                os.makedirs(
                    os.path.dirname(destination_path),
                    exist_ok=True
                )

                shutil.copy2(source_path, destination_path)

                success, message = verify_backup(
                    source_path,
                    destination_path
                )

                if not success:
                    result = (
                        f"INTEGRITY ERROR: {relative_path} - {message}"
                    )
                    print(result)
                    write_log(backup_folder, result)
                    continue

                result = (
                    f"{change_type}: {relative_path} -> "
                    "Backup successful; integrity verified."
                )
                print(result)
                write_log(backup_folder, result)

                try:
                    upload_file(destination_path, relative_path)
                    result = f"CLOUD UPLOAD SUCCESS: {relative_path}"
                    print(result)
                    write_log(backup_folder, result)

                except Exception as error:
                    result = (
                        f"CLOUD UPLOAD ERROR: {relative_path} - {error}"
                    )
                    print(result)
                    write_log(backup_folder, result)

            except Exception as error:
                result = f"BACKUP ERROR: {relative_path} - {error}"
                print(result)
                write_log(backup_folder, result)

        elif change_type == "DELETED":
            result = (
                f"DELETED: {relative_path} - "
                "Original removed; backup retained."
            )
            print(result)
            write_log(backup_folder, result)
