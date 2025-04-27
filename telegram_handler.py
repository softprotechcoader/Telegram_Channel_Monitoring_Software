from telethon import TelegramClient
import asyncio
import sqlite3

async def login_account(phone_number, api_id, api_hash, get_login_code):
    """Log in to a Telegram account using the provided phone number, API_ID, API_HASH, and a callback for the login code."""
    client = TelegramClient(f'session_{phone_number}', api_id, api_hash)

    for attempt in range(5):  # Retry up to 5 times
        try:
            await client.connect()
            break
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e):
                print(f"Database is locked. Retrying... (Attempt {attempt + 1}/5)")
                await asyncio.sleep(1)  # Wait for 1 second before retrying
            else:
                raise
    else:
        raise sqlite3.OperationalError("Failed to connect after 5 attempts due to database lock.")

    if not await client.is_user_authorized():
        try:
            await client.send_code_request(phone_number)
            code = await get_login_code(phone_number)
            if code:
                await client.sign_in(phone_number, code)
            else:
                print(f"No code provided for {phone_number}")
                return None
        except Exception as e:
            print(f"Failed to log in for {phone_number}: {e}")
            return None

    print(f"Logged in as {phone_number}")
    return client

async def monitor_channels(client):
    """Monitor all channels the user is subscribed to and read their content."""
    async for dialog in client.iter_dialogs():
        if dialog.is_channel:
            print(f"Monitoring channel: {dialog.name}")
            async for message in client.iter_messages(dialog.id):
                print(f"[{dialog.name}] {message.date}: {message.text}")

async def main(accounts, get_login_code, monitor_channels_with_ui):
    """Log in to multiple accounts and monitor their channels using a custom monitoring function."""
    clients = []
    for account in accounts:
        phone_number = account['Phone Number']
        api_id = account['API_ID']
        api_hash = account['API_HASH']
        client = await login_account(phone_number, api_id, api_hash, get_login_code)
        if client:
            clients.append(client)

    # Monitor channels for all clients using the custom monitoring function
    await asyncio.gather(*(monitor_channels_with_ui(client) for client in clients))

# Example usage (replace with actual data from Excel file)
# accounts = [{'Phone Number': '+123456789', 'API_ID': '12345', 'API_HASH': 'abcde'}, {'Phone Number': '+987654321', 'API_ID': '67890', 'API_HASH': 'fghij'}]
# async def get_login_code(phone_number):
#     return input(f"Enter the code for {phone_number}: ")
# asyncio.run(main(accounts, get_login_code))