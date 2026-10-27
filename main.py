
from config import load_config
from modules.file_monitor import scan_folder, detect_changes
from modules.backup_manager import process_changes
from modules.scheduler import start_scheduler


def main():
    try:
        config = load_config()

        source_folder = config["source_folder"]
        backup_folder = config["backup_folder"]
        interval = config["backup_interval_minutes"]

        source = source_folder.replace("\\", "/").rstrip("/").lower()
        backup = backup_folder.replace("\\", "/").rstrip("/").lower()

        if backup == source or backup.startswith(source + "/"):
            raise ValueError(
                "Backup folder must be outside the source folder."
            )

        print("Simple Cloud-Based Automated Backup System")
        print("Source:", source_folder)
        print("Local backup:", backup_folder)

        previous = scan_folder(source_folder)

        # Back up files already present at startup
        initial_changes = detect_changes({}, previous)
        process_changes(
            source_folder, backup_folder, initial_changes
        )

        def backup_task():
            nonlocal previous

            current = scan_folder(source_folder)
            changes = detect_changes(previous, current)

            if changes:
                for change_type, path in changes:
                    print(f"{change_type}: {path}")

                process_changes(
                    source_folder, backup_folder, changes
                )
            else:
                print("No file changes detected.")

            previous = current

        start_scheduler(backup_task, interval)

    except (OSError, ValueError, KeyError) as error:
        print("Error:", error)


if __name__ == "__main__":
    main()
