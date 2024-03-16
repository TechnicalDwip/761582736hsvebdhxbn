from pyrogram import Client, filters
from info import API_ID, API_HASH, BOT_TOKEN, OWNER_ID

client = Client("movie_request_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@client.on_message(filters.command("request") & filters.private)
async def request_movie(bot, update):
    if len(update.command) <= 1:
        await bot.send_message(update.chat.id, "Please provide the name of the movie with the /request command.")
    else:
        movie_name = ' '.join(update.command[1:])
        owner_message = f"New movie request: {movie_name}"
        await bot.send_message(OWNER_ID, owner_message)
