import time
import shutil
import logging
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------

# Configure the logging system to output messages like: "2023-10-25 14:30:00 - INFO - Moved file..."
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Set the folder we want to monitor. Path.home() gets the current user's home directory automatically.
WATCH_DIR = Path.home() / "Downloads"

# Map file extensions to their target folder names.
# We use sets (the {} brackets) instead of lists ([]) because checking if an item exists 
# in a set is mathematically faster (O(1)) for Python than scanning through a list.
EXTENSION_MAP = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp", ".bmp"},
    "Documents": {".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".csv"},
    "Archives": {".zip", ".tar", ".gz", ".7z", ".rar"},
    "Installers": {".dmg", ".pkg", ".exe", ".msi", ".deb"},
    "Code": {".py", ".cs", ".js", ".html", ".css", ".json", ".xml"},
    "Media": {".mp3", ".wav", ".mp4", ".mkv", ".avi", ".mov"},
}

# ---------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------

def get_destination_folder(extension: str) -> str:
    """Matches a file's extension to the correct category folder."""
    # Loop through each category and its associated extensions
    for category, extensions in EXTENSION_MAP.items():
        if extension in extensions:
            return category
    # If the extension isn't in our map, put it in a generic folder
    return "Other"

def wait_for_file_ready(file_path: Path, timeout: int = 60) -> bool:
    """
    Prevents the script from moving a file while the browser is still downloading it.
    It does this by tracking the file's size and trying to 'touch' it.
    """
    historical_size = -1
    start_time = time.time()
    
    # Keep checking the file for up to 'timeout' seconds (default 60s)
    while time.time() - start_time < timeout:
        try:
            # If the file disappeared (deleted or moved by the user), abort
            if not file_path.exists():
                return False
            
            # Get the current file size in bytes
            current_size = file_path.stat().st_size
            
            # If the file has data AND its size hasn't changed since the last check
            if current_size == historical_size and current_size > 0:
                # Try to open the file in 'append' ('a') mode.
                # If the browser is still writing to it, the OS will block this and throw a PermissionError.
                with open(file_path, 'a'): 
                    pass
                # If it successfully opens, the file is completely free and ready to move.
                return True
            
            # Update our historical size for the next loop iteration
            historical_size = current_size
        except (PermissionError, OSError):
            # File is still locked by the browser writing to it. We ignore the error and wait.
            pass
            
        # Pause for 1 second before checking the file size again
        time.sleep(1) 
        
    # If we waited for 60 seconds and it's still locked, give up
    return False

def process_file(file_path: Path):
    """Handles the logic of determining where a single file goes and moving it."""
    # Ignore missing files, directories, and hidden system files (which start with a dot)
    if not file_path.exists() or file_path.is_dir() or file_path.name.startswith("."):
        return

    # Extract the extension (e.g., ".pdf") and make it lowercase
    # Ignore temporary files created by Chrome (.crdownload), Safari (.download), or incomplete parts
    if file_path.suffix.lower() in {".crdownload", ".tmp", ".part", ".download"}:
        return

    # Figure out which folder this belongs in based on its extension
    destination_folder = get_destination_folder(file_path.suffix.lower())
    
    # Create the full path to the target folder (e.g., C:/Users/Name/Downloads/Images)
    target_dir = WATCH_DIR / destination_folder
    
    # Create the target directory if it doesn't already exist (exist_ok=True prevents errors)
    target_dir.mkdir(exist_ok=True)
    
    # Determine the final file path
    target_path = target_dir / file_path.name
    
    # COLLISION HANDLING: What if a file with this name already exists in the target folder?
    counter = 1
    # While the target path is already taken...
    while target_path.exists():
        # Append a number to the end of the filename (e.g., "report_1.pdf", "report_2.pdf")
        # .stem is the filename without the extension, .suffix is the extension
        target_path = target_dir / f"{file_path.stem}_{counter}{file_path.suffix}"
        counter += 1

    # Wait until the file is fully downloaded and unlocked by the OS
    if not wait_for_file_ready(file_path):
        logging.warning(f"Skipped {file_path.name} (locked or downloading too slowly).")
        return

    # Attempt to move the file
    try:
        shutil.move(str(file_path), str(target_path))
        logging.info(f"Moved: {file_path.name} -> {destination_folder}/")
    except Exception as e:
        # If something unexpectedly goes wrong, log the error without crashing the script
        logging.error(f"Failed to move {file_path.name}: {e}")

# ---------------------------------------------------------
# WATCHDOG EVENT HANDLER
# ---------------------------------------------------------

class DownloadOrganizerHandler(FileSystemEventHandler):
    """This class defines what happens when Watchdog detects a file system event."""
    
    def on_created(self, event):
        # Triggered when a brand new file is created in the folder
        if not event.is_directory:
            process_file(Path(event.src_path))

    def on_moved(self, event):
        # Triggered when a file is renamed (e.g., Chrome renaming 'file.crdownload' to 'file.pdf')
        if not event.is_directory:
            process_file(Path(event.dest_path))
            
    def on_modified(self, event):
        # Triggered when a file's contents are updated
        if not event.is_directory:
            process_file(Path(event.src_path))

def organize_existing_files():
    """Scans the directory on startup to clean up files that are already there."""
    logging.info("Scanning existing files...")
    # .iterdir() loops through everything currently inside the WATCH_DIR
    for item in WATCH_DIR.iterdir():
        if item.is_file():
            process_file(item)

# ---------------------------------------------------------
# MAIN EXECUTION
# ---------------------------------------------------------

# This block only runs if the script is executed directly (not imported into another script)
if __name__ == "__main__":
    logging.info(f"Monitoring started for directory: {WATCH_DIR}")
    
    # 1. Clean up anything already sitting in the Downloads folder before we start monitoring
    organize_existing_files()

    # 2. Set up the Watchdog observer
    event_handler = DownloadOrganizerHandler()
    observer = Observer()
    
    # Tell the observer to watch our specified directory. 
    # recursive=False means it won't look inside subfolders (like "Images" or "Documents")
    observer.schedule(event_handler, str(WATCH_DIR), recursive=False)
    
    # Start a background thread that monitors the folder
    observer.start()

    try:
        # Keep the main thread alive infinitely so the background observer can do its job
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # If the user presses Ctrl+C, gracefully stop the observer
        observer.stop()
        logging.info("Monitoring stopped by user.")
    
    # Wait for the observer thread to cleanly finish before closing the program completely
    observer.join()