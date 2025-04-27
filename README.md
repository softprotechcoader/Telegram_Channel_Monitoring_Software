# Telegram Automation Tool

This project is a Windows-based software for automating Telegram account management and channel monitoring. It allows users to log in to multiple Telegram accounts and monitor the content of subscribed channels.

## Features
- Generate an empty Excel file with a `Phone Number` header.
- Load an Excel file containing phone numbers for multiple accounts.
- Log in to Telegram accounts using OTP (One-Time Password).
- Monitor all channels the accounts are subscribed to.

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
1. Open the `telegram_handler.py` file in the project directory.
2. Locate the following lines:
   ```python
   API_ID = 'your_api_id'  # Replace with your Telegram API ID
   API_HASH = 'your_api_hash'  # Replace with your Telegram API Hash
   ```
3. Replace `'your_api_id'` and `'your_api_hash'` with the values obtained from the Telegram API Development Tools.
4. Save the file.

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
   - Generate an empty Excel file for phone numbers.
   - Load an existing Excel file with phone numbers.
   - Start the automation process.

3. During the login process, the application will prompt you to enter the OTP for each phone number.

## File Structure
- `main.py`: The main entry point for the application.
- `excel_handler.py`: Handles Excel file operations.
- `telegram_handler.py`: Manages Telegram API interactions.
- `.gitignore`: Excludes session files and sensitive data from version control.

## Notes
- Ensure that the phone numbers in the Excel file include the country code (e.g., `+91` for India).
- Session files are saved locally to avoid repeated logins.

## License
This project is licensed under the MIT License.