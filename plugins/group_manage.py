from pyrogram import Client, filters
from pyrogram.types import ChatPermissions
import re
from datetime import datetime, timedelta

# Function to parse time duration
def parse_duration(duration):
    match = re.match(r"^(\d+)([mhdwMy])$", duration)
    if not match:
        return None
    value = int(match.group(1))
    unit = match.group(2)
    if unit == "m":
        return timedelta(minutes=value)
    elif unit == "h":
        return timedelta(hours=value)
    elif unit == "d":
        return timedelta(days=value)
    elif unit == "w":
        return timedelta(weeks=value)
    elif unit == "M":
        return timedelta(days=value*30)
    elif unit == "y":
        return timedelta(days=value*365)

# Function to check if user is admin
async def is_admin(bot, message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    member = await bot.get_chat_member(chat_id, user_id)
    return member.status in ["administrator", "creator"]

# Command to ban a user (accessible only by admins)
@Client.on_message(filters.group & filters.command("ban"))
async def ban_user(bot, message):
    if not await is_admin(bot, message):
        return await message.reply("❌ You must be an admin to use this command.")
    if len(message.command) != 2:
        return await message.reply("❌ Incorrect format!\nUse `/ban user_id`")
    try:
        user_id = int(message.command[1])
    except ValueError:
        return await message.reply("❌ Please provide a valid user ID.")
    await bot.kick_chat_member(message.chat.id, user_id)
    await message.reply("✅ User has been banned from the group.")

# Command to kick a user (accessible only by admins)
@Client.on_message(filters.group & filters.command("kick"))
async def kick_user(bot, message):
    if not await is_admin(bot, message):
        return await message.reply("❌ You must be an admin to use this command.")
    if len(message.command) != 2:
        return await message.reply("❌ Incorrect format!\nUse `/kick user_id`")
    try:
        user_id = int(message.command[1])
    except ValueError:
        return await message.reply("❌ Please provide a valid user ID.")
    await bot.kick_chat_member(message.chat.id, user_id)
    await message.reply("✅ User has been kicked from the group.")

# Command to pin a message (accessible only by admins)
@Client.on_message(filters.group & filters.command("pin"))
async def pin_message(bot, message):
    if not await is_admin(bot, message):
        return await message.reply("❌ You must be an admin to use this command.")
    if not message.reply_to_message:
        return await message.reply("❌ Please reply to the message you want to pin.")
    await bot.pin_chat_message(message.chat.id, message.reply_to_message.message_id)
    await message.reply("✅ Message has been pinned.")

# Command to mute a user (accessible only by admins)
@Client.on_message(filters.group & filters.command("mute"))
async def mute_user(bot, message):
    if not await is_admin(bot, message):
        return await message.reply("❌ You must be an admin to use this command.")
    if len(message.command) != 3:
        return await message.reply("❌ Incorrect format!\nUse `/mute user_id duration`")
    try:
        user_id = int(message.command[1])
    except ValueError:
        return await message.reply("❌ Please provide a valid user ID.")
    
    duration = message.command[2]
    mute_duration = parse_duration(duration)
    if not mute_duration:
        return await message.reply("❌ Please provide a valid duration (e.g., 1m for 1 minute, 1h for 1 hour).")
    
    until_date = datetime.now() + mute_duration
    permissions = ChatPermissions()
    await bot.restrict_chat_member(message.chat.id, user_id, permissions, until_date=until_date)
    await message.reply(f"✅ User has been muted for {duration}.")

# Command to unmute a user (accessible only by admins)
@Client.on_message(filters.group & filters.command("unmute"))
async def unmute_user(bot, message):
    if not await is_admin(bot, message):
        return await message.reply("❌ You must be an admin to use this command.")
    if len(message.command) != 2:
        return await message.reply("❌ Incorrect format!\nUse `/unmute user_id`")
    try:
        user_id = int(message.command[1])
    except ValueError:
        return await message.reply("❌ Please provide a valid user ID.")
    await bot.restrict_chat_member(message.chat.id, user_id, ChatPermissions(can_send_messages=True))
    await message.reply("✅ User has been unmuted.")

# Command to unban a user (accessible only by admins)
@Client.on_message(filters.group & filters.command("unban"))
async def unban_user(bot, message):
    if not await is_admin(bot, message):
        return await message.reply("❌ You must be an admin to use this command.")
    if len(message.command) != 2:
        return await message.reply("❌ Incorrect format!\nUse `/unban user_id`")
    try:
        user_id = int(message.command[1])
    except ValueError:
        return await message.reply("❌ Please provide a valid user ID.")
    await bot.unban_chat_member(message.chat.id, user_id)
    await message.reply("✅ User has been unbanned.")

# Command to promote a user (accessible only by admins)
@Client.on_message(filters.group & filters.command("promote"))
async def promote_user(bot, message):
    if not await is_admin(bot, message):
        return await message.reply("❌ You must be an admin to use this command.")
    if len(message.command) != 2:
        return await message.reply("❌ Incorrect format!\nUse `/promote user_id`")
    try:
        user_id = int(message.command[1])
    except ValueError:
        return await message.reply("❌ Please provide a valid user ID.")
    await bot.promote_chat_member(message.chat.id, user_id)

# Command to demote a user (accessible only by admins)
@Client.on_message(filters.group & filters.command("demote"))
async def demote_user(bot, message):
    if not await is_admin(bot, message):
        return await message.reply("❌ You must be an admin to use this command.")
    if len(message.command) != 2:
        return await message.reply("❌ Incorrect format!\nUse `/demote user_id`")
    try:
        user_id = int(message.command[1])
    except ValueError:
        return await message.reply("❌ Please provide a valid user ID.")
    await bot.promote_chat_member(message.chat.id, user_id, can_change_info=False, can_invite_users=False, can_pin_messages=False, can_manage_chat=False, can_manage_voice_chats=False, can_restrict_members=False, can_promote_members=False)

# Command for member to request ban
@Client.on_message(filters.group & filters.command("banme"))
async def ban_me(bot, message):
    if await is_admin(bot, message):
        return await message.reply("❌ This command is not for admins.")
    await bot.kick_chat_member(message.chat.id, message.from_user.id)
    await message.reply("❌ You have been banned from the group.")
