# Simple Cloud-Based Automated Backup System

## Overview
A Python-based backup system that monitors a source directory, detects new and modified files, creates local backups, uploads files to Google Drive, and verifies local backup integrity using SHA-256 hashing. It also records backup events and errors and provides a script to restore backed-up files.

## Features
- Automatic file monitoring and scheduled backups
- Detection of new, modified, and deleted files
- Local file backup with metadata preservation
- Google Drive cloud uploads
- SHA-256 integrity verification
- Backup history and error logging
- Local file restoration

## Technologies Used
- Python
- Google Drive API
- SHA-256 hashing
- Git and GitHub

## Project Structure
- `main.py` — Main application and scheduler integration
- `config.py` and `config.json` — Configuration management
- `modules/file_monitor.py` — File change detection
- `modules/backup_manager.py` — Local backup, verification, and upload handling
- `modules/cloud_storage.py` — Google Drive integration
- `modules/scheduler.py` — Periodic execution
- `modules/integrity_checker.py` — SHA-256 integrity verification
- `restore_backup.py` — Local backup restoration

## Setup
1. Install Python 3.
2. Install dependencies:
   `pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib`
3. Configure the source and backup directories in `config.json`.
4. Set up Google Drive API OAuth credentials and save `credentials.json` locally.
5. Run the application:
   `python main.py`

## Security Notes
Do not commit OAuth credentials, access tokens, or other secrets. Test the system with non-critical files before relying on it for important data.

## Limitations
- The application must remain running for its scheduler to operate.
- Deleted source files are logged, while existing backups are retained.
- Restoration currently uses local backups.
- Cloud upload success does not by itself verify the integrity of the uploaded cloud copy.
