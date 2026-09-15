Auto Download Organizer

A lightweight, real-time Python background automation script for Windows that monitors your Downloads directory and automatically organizes incoming files into categorized folders based on their file extensions.

Features:
Real-time monitoring of the Windows Downloads folder
Event-driven file organization using watchdog
Automatic categorization by file extension
Avoids interfering with incomplete downloads
Ignores hidden files and directories
Automatic duplicate filename handling
Short delay before moving files to avoid Windows file-lock issues
Can run automatically in the background when Windows starts

Installation
1. Clone the Repository
Open Command Prompt or PowerShell and run:

git clone https://github.com/roniikaa1/auto-download-organizer.git
cd auto-download-organizer

2. Install the Dependency

Install watchdog using pip:
pip install watchdog

3. Run the Script

Start the organizer manually:
python organizer.py


