Auto Download Organizer

A lightweight, real-time Python background automation script for Windows that monitors your Downloads directory and automatically organizes incoming files into categorized folders based on their file extensions.

Features

📁 Real-time monitoring of the Windows Downloads folder

⚡ Event-driven file organization using watchdog

🗂️ Automatic categorization by file extension

🔒 Avoids interfering with incomplete downloads

👻 Ignores hidden files and directories

🔄 Automatic duplicate filename handling

⏱️ Short delay before moving files to avoid Windows file-lock issues

🚀 Can run automatically in the background when Windows starts

How It Works

The script uses watchdog and pathlib to monitor the Downloads directory in real time.

1. Folder Watching

watchdog.observers.Observer monitors the following directory:

C:\Users\<Username>\Downloads


When a filesystem event occurs, the script checks whether the event involves a file that should be organized.

2. Event Trigger

The file system event handler detects changes in the Downloads folder and triggers the organization routine.

3. Filtering & Safety Checks

Before moving a file, the script checks:

Temporary download files are ignored:

.crdownload

.part

.tmp

Directories are ignored

Hidden/system files are ignored

This helps prevent files from being moved while they are still being downloaded or written.

4. Category Mapping

The file extension is converted to lowercase and compared against the predefined categories.

If an extension is not recognized, the file is automatically moved to the Other folder.

5. Duplicate Handling

If a file with the same name already exists in the destination folder, the script automatically creates a new filename instead of overwriting the existing file.

For example:

document.pdf
document_1.pdf
document_2.pdf

6. Safe File Movement

Before moving a file, the script waits approximately 0.5 seconds.

This provides a small safety buffer for Windows applications to release file locks before shutil.move() is executed.

Folder Categorization
Category	File Extensions
Images	.jpg, .jpeg, .png, .gif, .svg, .webp, .bmp
Documents	.pdf, .docx, .doc, .txt, .xlsx, .pptx, .csv
Archives	.zip, .tar, .gz, .7z, .rar
Installers	.exe, .msi
Code	.py, .cs, .js, .html, .css, .json, .xml
Media	.mp3, .wav, .mp4, .mkv, .avi, .mov
Other	Any unlisted extension

After organization, your Downloads folder may look like this:

Downloads/
├── Images/
├── Documents/
├── Archives/
├── Installers/
├── Code/
├── Media/
└── Other/

Requirements

Windows 10 or Windows 11

Python 3.x

watchdog

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


The script will begin monitoring your Downloads folder.

To stop the script, press:

Ctrl + C

Run Automatically on Windows Startup

There are two recommended ways to start the organizer automatically when you log into Windows.

Method 1: Windows Startup Folder

This is the easiest method.

Step 1 — Open the Startup Folder

Press:

Win + R


Enter:

shell:startup


and press Enter.

Windows will open your personal Startup folder, typically located at:

C:\Users\<Username>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup

Step 2 — Create a Batch File

Create a new file called:

run_organizer.bat


Right-click the file and select Edit.

Add the following:

@echo off
start /B pythonw.exe "C:\Users\YOUR_USERNAME\auto-download-organizer\organizer.py"


Replace:

YOUR_USERNAME


with your actual Windows username.

For example:

@echo off
start /B pythonw.exe "C:\Users\John\auto-download-organizer\organizer.py"


Note: pythonw.exe runs Python without opening a Command Prompt window, allowing the organizer to run silently in the background.

Method 2: Windows Task Scheduler

You can also use Windows Task Scheduler for more control over how the script starts.

Step 1 — Open Task Scheduler

Press:

Win + R


Enter:

taskschd.msc


and press Enter.

Step 2 — Create a Task

Click:

Create Task...

on the right-hand side.

General

Set:

Name: Auto Download Organizer


Select:

Run only when user is logged on

Triggers

Click:

New...

Set:

Begin the task: At log on


Then click OK.

Actions

Click:

New...

Set:

Action: Start a program


For Program/script, enter:

pythonw.exe


For Add arguments, enter:

"C:\Users\YOUR_USERNAME\auto-download-organizer\organizer.py"


Replace YOUR_USERNAME with your Windows username.

Click OK and save the task.

Usage

Once the script is running, simply download or copy files into your Downloads folder.

For example:

Downloads/
├── photo.jpg
├── report.pdf
├── archive.zip
├── installer.exe
└── music.mp3


The organizer will automatically sort them into:

Downloads/
├── Images/
│   └── photo.jpg
├── Documents/
│   └── report.pdf
├── Archives/
│   └── archive.zip
├── Installers/
│   └── installer.exe
├── Media/
│   └── music.mp3
├── Code/
└── Other/


No manual organization is required.

Duplicate Files

The organizer never overwrites an existing file.

If report.pdf already exists in the Documents folder, a new download will be renamed automatically:

report.pdf
report_1.pdf
report_2.pdf
report_3.pdf


This ensures that existing files are preserved.

Temporary Downloads

Modern browsers often use temporary file extensions while downloading.

The organizer ignores:

.crdownload
.part
.tmp


This prevents incomplete downloads from being moved prematurely.

Once the download is complete and the browser creates the final file, the organizer can process it normally.

Project Structure
auto-download-organizer/
│
├── organizer.py
└── README.md

Technologies Used

Python — Main programming language

watchdog — Real-time filesystem monitoring

pathlib — Cross-platform filesystem path handling

shutil — File movement

Windows Task Scheduler / Startup Folder — Automatic startup

Repository

The source code is available on GitHub:

{"fallbackMarkdown":"github.com/roniikaa1/auto-download-organizer","reference":{"matched_text":"","prefix":null,"start_idx":7180,"end_idx":7283,"safe_urls":[],"refs":[],"alt":"github.com/roniikaa1/auto-download-organizer","prompt_text":"github.com/roniikaa1/auto-download-organizer","type":"url","item":{"title":"github.com/roniikaa1/auto-download-organizer","url":"https://github.com/roniikaa1/auto-download-organizer?utm_source=chatgpt.com","attribution":"github.com","pub_date":null,"snippet":null,"attribution_segments":null,"supporting_websites":null,"refs":[],"hue":null,"attributions":null},"layout":null,"title":"github.com/roniikaa1/auto-download-organizer","logo":null},"showLoginRequiredCard":false}
