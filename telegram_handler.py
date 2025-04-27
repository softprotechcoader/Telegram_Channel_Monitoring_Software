from telethon import TelegramClient
import asyncio

# Define constants for the Telegram API
API_ID = '29844383'  # Replace with your Telegram API ID
API_HASH = 'de3cc48c49de957cbc533bc22d9004b7'  # Replace with your Telegram API Hash

async def login_account(phone_number, get_login_code):
    """Log in to a Telegram account using the provided phone number and a callback for the login code."""
    client = TelegramClient(f'session_{phone_number}', API_ID, API_HASH)
    await client.connect()

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
    """Monitor all channels the user is subscribed to."""
    async for dialog in client.iter_dialogs():
        if dialog.is_channel:
            print(f"Monitoring channel: {dialog.name}")
            # Add logic to handle new messages or content here

async def main(accounts, get_login_code):
    """Log in to multiple accounts and monitor their channels."""
    clients = []
    for account in accounts:
        phone_number = account['Phone Number']
        client = await login_account(phone_number, get_login_code)
        if client:
            clients.append(client)

    # Monitor channels for all clients
    await asyncio.gather(*(monitor_channels(client) for client in clients))

# Example usage (replace with actual data from Excel file)
# accounts = [{'Phone Number': '+123456789'}, {'Phone Number': '+987654321'}]
# async def get_login_code(phone_number):
#     return input(f"Enter the code for {phone_number}: ")
# asyncio.run(main(accounts, get_login_code))