

import telegram
import asyncio

BOT_TOKEN = '7827627496:AAHx2vU2Top43OsizxQmy2ADT5nC2doaKgI'

async def send_message(message):
    try:
        print('sending message1')
        bot = telegram.Bot(token=BOT_TOKEN)
        await bot.send_message(chat_id=192398851, text=message)
        print('sending message2')
    except Exception as e:
        print(f"Error: {e}")

async def main():
    await send_message('test')

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())