
import os


def scan_folder(folder):
    files = {}

    for root, _, filenames in os.walk(folder):
        for filename in filenames:
            path = os.path.join(root, filename)
            relative_path = os.path.relpath(path, folder)

            try:
                stat = os.stat(path)
                files[relative_path] = (
                    stat.st_size,
                    stat.st_mtime_ns
                )
            except OSError:
                continue

    return files


def detect_changes(previous, current):
    changes = []

    for path in current.keys() - previous.keys():
        changes.append(("NEW", path))

    for path in previous.keys() - current.keys():
        changes.append(("DELETED", path))

    for path in current.keys() & previous.keys():
        if current[path] != previous[path]:
            changes.append(("MODIFIED", path))

    return sorted(changes)
