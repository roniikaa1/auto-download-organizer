# Auto Download Organizer

A lightweight, robust, and real-time Python background automation script that monitors your Downloads directory and automatically organizes incoming files into categorized folders based on their extensions.

## Features

- **Real-Time Monitoring:** Uses `watchdog` to catch file creations, modifications, and renames (such as Chrome finalizing `.crdownload` files or Safari's `.download` files).
- **Smart File-Lock Protection:** Instead of arbitrary timers, it actively monitors file size stability and verifies OS access permissions to ensure downloads are fully completed before moving them.
- **Startup Cleanup:** Automatically scans and organizes any existing unorganized files sitting in your Downloads folder when the script first launches.
- **Automatic Categorization:** Neatly sorts files into designated folders: *Images, Documents, Archives, Installers, Code, Media, and Other*.
- **Duplicate Prevention:** Safely handles filename collisions by automatically appending counters (e.g., `report_1.pdf`) instead of overwriting existing files.
- **Advanced Filtering:** Automatically ignores hidden files, directories, and temporary download parts (`.tmp`, `.part`, etc.).
- **Professional Logging:** Uses Python's built-in `logging` module to output clean, timestamped activity logs.

---

## Installation & Usage

### 1. Clone the Repository
Open Command Prompt, PowerShell, or Terminal and run:

```bash
git clone [https://github.com/roniikaa1/auto-download-organizer.git](https://github.com/roniikaa1/auto-download-organizer.git)
cd auto-download-organizer
