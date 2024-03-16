from pyrogram import Client, filters
from info import API_ID, API_HASH, BOT_TOKEN, ADMINS
OWNER_ID = ADMINS 

client = Client("royal", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@client.on_message(filters.command("request"))
async def request_movie(bot, message):
    if len(message.command) <= 1:
        await bot.send_message(message.chat.id, "Please provide the name of the movie with the /request command.")
    else:
        movie_name = ' '.join(message.command[1:])
        owner_message = f"New movie request: {movie_name}"
        await bot.send_message(OWNER_ID, owner_message)
        await bot.send_message(message.chat.id, "Movie request sent successfully.")

client.start()
