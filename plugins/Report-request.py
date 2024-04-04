from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from info import LOG_CHANNEL

app = Client("movie_bot")

@app.on_message(filters.command("request", prefixes="/") & ~filters.edited)
async def request_movie(client, message: Message):
    if len(message.command) == 1:
        await message.reply("Wrong format! Use correct format: /request {movie_name}")
    else:
        await message.reply("movie request send successfully")
        movie_name = " ".join(message.command[1:])
        content = f"Movie name: {movie_name}\nRequested by: {message.from_user.mention}"
        buttons = [
            InlineKeyboardButton("Available", callback_data="movie_available"),
            InlineKeyboardButton("Not Available", callback_data="movie_not_available"),
            InlineKeyboardButton("Not Released Yet", callback_data="movie_not_released"),
            InlineKeyboardButton("Mark as Done", callback_data="close_data")
        ]
        keyboard = InlineKeyboardMarkup([buttons])
        await client.send_message("LOG_CHANNEL", text=content, reply_markup=keyboard)


@app.on_callback_query()
async def handle_button_click(client, callback_query):
    action, movie_name = callback_query.data.split()
    
    if data == "movie_available":
        await callback_query.answer()
        await client.send_message(callback_query.from_user.id, f"{movie_name} is now available.")
    elif data == "movie_not_available":
        await callback_query.answer()
        await client.send_message(callback_query.from_user.id, f"{movie_name} is not available.")
    elif data == "movie_not_released":
        await callback_query.answer()
        await client.send_message(callback_query.from_user.id, f"{movie_name} has not been released yet.")
