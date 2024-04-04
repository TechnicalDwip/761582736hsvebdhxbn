from info import *
from pyrogram import Client, filters
from pyrogram.types import ChatPermissions

@Client.on_message(filters.group & filters.command("fsub"))
async def f_sub_cmd(bot, message):
    m = await message.reply("Please wait..")
    try:
       group = await get_group(message.chat.id)
    except:
       return await m.edit("❌ Error: Failed to get group information.")
    
    try:
       f_sub = int(message.command[-1])
    except:
       return await m.edit("❌ Incorrect format!\nUse `/forcesub ChannelID`")       
    try:
       chat = await bot.get_chat(f_sub)
       group_info = await bot.get_chat(message.chat.id)
       c_link = chat.invite_link
       g_link = group_info.invite_link       
    except Exception as e:
       text = f"❌ Error: `{str(e)}`\n\nMake sure I'm admin in that channel & this group with all permissions"
       return await m.edit(text)
    
    try:
        await update_group(message.chat.id, {"f_sub": f_sub})
    except Exception as e:
        await m.edit(f"❌ Error: Failed to attach ForceSub channel. {str(e)}")
        return
    
    await m.edit(f"✅ Successfully Attached ForceSub to [{chat.title}]({c_link})!", disable_web_page_preview=True)
    text = f"#NewFsub\n\nUser: {message.from_user.mention}\nGroup: [{group_info.title}]({g_link})\nChannel: [{chat.title}]({c_link})"
    await bot.send_message(chat_id=LOG_CHANNEL, text=text)

@Client.on_message(filters.group & filters.command("nofsub"))
async def nf_sub_cmd(bot, message):
    m = await message.reply("Disattaching..")
    try:
       group = await get_group(message.chat.id)
       f_sub = group["f_sub"]
    except:
       return await m.edit("❌ Error: Failed to get group information.")  
    
    if not f_sub:
       return await m.edit("This chat is currently not subscribed to any ForceSub channel.\nUse /fsub to attach one.")        
    try:
       chat = await bot.get_chat(f_sub)
       group_info = await bot.get_chat(message.chat.id)
       c_link = chat.invite_link
       g_link = group_info.invite_link       
    except Exception as e:
       text = f"❌ Error: `{str(e)}`\n\nMake sure I'm admin in that channel & this group with all permissions"
       return await m.edit(text)
    try:
        await update_group(message.chat.id, {"f_sub": False})
    except Exception as e:
        await m.edit(f"❌ Error: Failed to remove ForceSub. {str(e)}")
        return
    
    await m.edit(f"✅ Successfully removed ForceSub from [{chat.title}]({c_link})!", disable_web_page_preview=True)
    text = f"#RemoveFsub\n\nUser: {message.from_user.mention}\nGroup: [{group_info.title}]({g_link})\nChannel: [{chat.title}]({c_link})"
    await bot.send_message(chat_id=LOG_CHANNEL, text=text)

@Client.on_callback_query(filters.regex(r"^checksub"))
async def f_sub_callback(bot, update):
    user_id = int(update.data.split("_")[-1])
    group = await get_group(update.message.chat.id)
    f_sub = group["f_sub"]

    try:
       await bot.get_chat_member(f_sub, user_id)          
    except UserNotParticipant:
       await update.answer("You need to subscribe to the channel first.", show_alert=True)
    except:       
       await bot.restrict_chat_member(chat_id=update.message.chat.id, 
                                      user_id=user_id,
                                      permissions=ChatPermissions(can_send_messages=True,
                                                                  can_send_media_messages=True,
                                                                  can_send_other_messages=True))
       await update.message.delete()
    else:
       await bot.restrict_chat_member(chat_id=update.message.chat.id, 
                                      user_id=user_id,
                                      permissions=ChatPermissions(can_send_messages=True,
                                                                  can_send_media_messages=True,
                                                                  can_send_other_messages=True))
       await update.message.delete()
       
@Client.on_message(filters.group & filters.command("checksub"))
async def rev_f_sub_cmd(bot, message):
    m = await message.reply("Checking ForceSub channel...")
    try:
        group = await get_group(message.chat.id)
        f_sub = group["f_sub"]
    except:
        return await m.edit("This chat is not subscribed to any ForceSub channel.")
    
    try:
        chat = await bot.get_chat(f_sub)
        c_link = chat.invite_link
    except Exception as e:
        text = f"❌ Error: `{str(e)}`\n\nFailed to retrieve ForceSub channel information."
        return await m.edit(text)
    
    await m.edit(f"🔗 Connected ForceSub Channel: [{chat.title}]({c_link})", disable_web_page_preview=True)
        
