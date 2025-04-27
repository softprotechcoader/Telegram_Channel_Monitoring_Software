# Telegram Automation Tool

This project is a Windows-based software for automating Telegram account management and channel monitoring. It allows users to log in to multiple Telegram accounts, monitor the content of subscribed channels, and export data to Word documents.

## Features
- Generate an empty Excel file with a `Phone Number`, `API_ID`, and `API_HASH` header.
- Load an Excel file containing phone numbers and API credentials for multiple accounts.
- Log in to Telegram accounts using OTP (One-Time Password).
- Monitor all channels the accounts are subscribed to.
- Read the latest N messages from all channels.
- Abort ongoing processes and reset the tool while keeping the loaded file.
- Export channel content to a Word document, organized by date and channel.

## Prerequisites
1. Python 3.10 or higher installed on your system.
2. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```
3. Obtain your Telegram API credentials:
   - Go to [Telegram API Development Tools](https://my.telegram.org/auth).
   - Log in with your Telegram account.
   - Create a new application to get your `API_ID` and `API_HASH`.

## Configuring API_ID and API_HASH
1. Open the Excel file you are using for the application.
2. Ensure the file contains the following columns:
   - `Phone Number`: The phone number of the Telegram account (including country code, e.g., +91).
   - `API_ID`: The API ID obtained from Telegram API Development Tools.
   - `API_HASH`: The API Hash obtained from Telegram API Development Tools.
3. Populate the `API_ID` and `API_HASH` columns with the credentials for each account.
4. Save the Excel file and load it into the application using the "Load Excel File" button in the GUI.

## Installation
1. Clone this repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd Telegram_Automation
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Run the application:
   ```bash
   python main.py
   ```
2. Use the GUI to:
   - Generate an empty Excel file for phone numbers and API credentials.
   - Load an existing Excel file with phone numbers and API credentials.
   - Start the automation process.
   - Read the latest N messages from all channels.
   - Abort ongoing processes and reset the tool.
   - Export channel content to a Word document.

3. During the login process, the application will prompt you to enter the OTP for each phone number.

## Creating a Standalone Installer
To create a standalone installer for this application:

### Step 1: Bundle the Application
1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```
2. Create a standalone executable:
   ```bash
   pyinstaller --onefile --windowed main.py
   ```
   - `--onefile`: Bundles everything into a single executable.
   - `--windowed`: Ensures no console window appears when running the application.

3. The executable will be located in the `dist` folder.

### Step 2: Create the Installer
1. Install Inno Setup from [https://jrsoftware.org/isinfo.php](https://jrsoftware.org/isinfo.php).
2. Create an Inno Setup script (`setup.iss`) with the following content:
   ```iss
   ; Inno Setup Script for Telegram Automation Tool
   [Setup]
   AppName=Telegram Automation Tool
   AppVersion=1.0
   DefaultDirName={pf}\TelegramAutomation
   DefaultGroupName=Telegram Automation Tool
   OutputBaseFilename=TelegramAutomationInstaller
   Compression=lzma
   SolidCompression=yes

   [Files]
   Source: "dist\main.exe"; DestDir: "{app}"; Flags: ignoreversion
   Source: "telegram_icon.png"; DestDir: "{app}"; Flags: ignoreversion

   [Icons]
   Name: "{group}\Telegram Automation Tool"; Filename: "{app}\main.exe"
   Name: "{group}\Uninstall Telegram Automation Tool"; Filename: "{uninstallexe}"

   [Run]
   Filename: "{app}\main.exe"; Description: "Launch Telegram Automation Tool"; Flags: nowait postinstall skipifsilent
   ```
3. Open the script in Inno Setup and click "Compile" to generate the installer.

### Step 3: Test the Installer
1. Run the generated installer to test the installation process.
2. Verify that the application works without requiring Python.

## File Structure
- `main.py`: The main entry point for the application.
- `excel_handler.py`: Handles Excel file operations.
- `telegram_handler.py`: Manages Telegram API interactions.
- `.gitignore`: Excludes session files and sensitive data from version control.
- `README.md`: Documentation for the project.

## Notes
- Ensure that the phone numbers in the Excel file include the country code (e.g., `+91` for India).
- Session files are saved locally to avoid repeated logins.
- The application is designed to handle multiple accounts and channels efficiently.

## License
This project is licensed under the MIT License.