import asyncio

from telethon.events import ChatAction
from telethon.tl.functions.contacts import BlockRequest, UnblockRequest
from telethon.tl.types import MessageEntityMentionName

from userbot import CMD_HELP
from userbot.plugins.sql_helper.mute_sql import is_muted, mute, unmute
from userbot.utils import admin_cmd

from userbot.events import register

async def get_full_user(event):
    args = event.pattern_match.group(1).split(":", 1)
    extra = None
    if event.reply_to_msg_id and len(args) != 2:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.from_id)
        extra = event.pattern_match.group(1)
    elif len(args[0]) > 0:
        user = args[0]
        if len(args) == 2:
            extra = args[1]
        if user.isnumeric():
            user = int(user)
        if not user:
            await event.edit("`User ID Is Required")
            return
        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except Exception as err:
            return await event.edit("Something Went Wrong", str(err))
    return user_obj, extra


async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)
    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        await event.edit(str(err))
        return None
    return user_obj


@borg.on(admin_cmd(pattern="ggban ?(.*)"))
async def gspider(userbot):
    lol = userbot
    sender = await lol.get_sender()
    me = await lol.client.get_me()
    if sender.id != me.id:
        event = await lol.reply("Gbanning This User !")
    else:
        event = await lol.edit("Wait Processing.....")
    me = await userbot.client.get_me()
    await event.edit('Global Ban Is Coming ! Wait And Watch You Nigga')
    my_mention = "[{}](tg://user?id={})".format(me.first_name, me.id)
    f"@{me.username}" if me.username else my_mention
    await userbot.get_chat()
    a = b = 0
    if userbot.is_private:
        user = userbot.chat
        reason = userbot.pattern_match.group(1)
    else:
        userbot.chat.title
    try:
        user, reason = await get_full_user(userbot)
    except:
        pass
    try:
        if not reason:
            reason = "Private"
    except:
        return await event.edit('**Something W3NT Wrong 🤔**')
    if user:
        if user.id in [1169076058, 1492186775]:
            return await event.edit(
                "**Didn't , Your Father Teach You ? That You Cant Gban Dev**"
            )

        try:
            from userbot.modules.sql_helper.gmute_sql import gmute
        except:
            pass
        try:
            await userbot.client(BlockRequest(user))
        except:
            pass
        testuserbot = [
            d.entity.id
            for d in await userbot.client.get_dialogs()
            if (d.is_group or d.is_channel)
        ]
        for i in testuserbot:
            try:
                await userbot.client.edit_permissions(i, user, view_messages=False)
                a += 1
                await event.edit(f"**GBANNED⚠️ \n🚫Total Affected Chats **: `{a}`")
            except:
                b += 1
    else:
        await event.edit('**Reply to a user !!**')
    try:
        if gmute(user.id) is False:
            return await event.edit('**Error! User probably already gbanned.**')
    except:
        pass
    return await event.edit(
        f"**⚠️Gbanned\nUSER👤[{user.first_name}](tg://user?id={user.id}) \n🚫Affected Chats : {a} **"
    )


@borg.on(admin_cmd(pattern="unggban ?(.*)"))
async def gspider(userbot):
    lol = userbot
    sender = await lol.get_sender()
    me = await lol.client.get_me()
    if sender.id != me.id:
        event = await lol.reply("`Wait Let Me Process`")
    else:
        event = await lol.edit("One Min ! ")
    me = await userbot.client.get_me()
    await event.edit('Trying To Ungban User !')
    my_mention = "[{}](tg://user?id={})".format(me.first_name, me.id)
    f"@{me.username}" if me.username else my_mention
    await userbot.get_chat()
    a = b = 0
    if userbot.is_private:
        user = userbot.chat
        reason = userbot.pattern_match.group(1)
    else:
        userbot.chat.title
    try:
        user, reason = await get_full_user(userbot)
    except:
        pass
    try:
        if not reason:
            reason = "Private"
    except:
        return await event.edit("Someting Went Wrong 🤔")
    if user:
        if user.id in [1169076058, 1492186775]:
            return await event.edit("**You Cant Ungban A Dev !**")
        try:
            from userbot.modules.sql_helper.gmute_sql import ungmute
        except:
            pass
        try:
            await userbot.client(UnblockRequest(user))
        except:
            pass
        testuserbot = [
            d.entity.id
            for d in await userbot.client.get_dialogs()
            if (d.is_group or d.is_channel)
        ]
        for i in testuserbot:
            try:
                await userbot.client.edit_permissions(i, user, send_messages=True)
                a += 1
                await event.edit(f"**UNGBANNING // AFFECTED CHATS - {a} **")
            except:
                b += 1
    else:
        await event.edit("**Reply to a user !!**")
    try:
        if ungmute(user.id) is False:
            return await event.edit("**Error! User probably already ungbanned.**")
    except:
        pass
    return await event.edit(
        f"**🔹UNGBANNED\n🔹USER - [{user.first_name}](tg://user?id={user.id}) \n🔹CHATS : {a} **"
    )


@borg.on(ChatAction)
async def handler(rkG):
    if not rkG.user_joined and not rkG.user_added:
        return
    try:
        from userbot.modules.sql_helper.gmute_sql import is_gmuted

        guser = await rkG.get_user()
        gmuted = is_gmuted(guser.id)
    except:
        return
    if gmuted:
        for i in gmuted:
            if i.sender == str(guser.id):
                chat = await rkG.get_chat()
                admin = chat.admin_rights
                creator = chat.creator
                if admin or creator:
                    try:
                        await client.edit_permissions(
                            rkG.chat_id, guser.id, view_messages=False
                        )
                        await rkG.reply(
                            f"**Gbanned User Joined!!** \n"
                            f"**Victim Id**: [{guser.id}](tg://user?id={guser.id})\n"
                            f"**Action **  : `Banned`"
                        )
                    except:
                        rkG.reply("`No Permission To Ban`")
                        return


@borg.on(admin_cmd(pattern=r"gmute ?(\d+)?"))
async def startgmute(event):
    private = False
    if event.fwd_from:
        return
    elif event.is_private:
        await event.edit("Unexpected issues or ugly errors may occur!")
        await asyncio.sleep(3)
        private = True
    reply = await event.get_reply_message()
    if event.pattern_match.group(1) is not None:
        userid = event.pattern_match.group(1)
    elif reply is not None:
        userid = reply.sender_id
    elif private:
        userid = event.chat_id
    else:
        return await event.edit(
            "Please reply to a user or add their into the command to gmute them."
        )
    event.chat_id
    await event.get_chat()
    if is_muted(userid, "gmute"):
        return await event.edit("`He has Tap Already On His Mouth.`")
    try:
        mute(userid, "gmute")
    except Exception as e:
        await event.edit("Error occured!\nError is " + str(e))
    else:
        await event.edit("Here A Tape, Now Shutup \nGmuteD")


@borg.on(admin_cmd(pattern=r"ungmute ?(\d+)?"))
async def endgmute(event):
    private = False
    if event.fwd_from:
        return
    elif event.is_private:
        await event.edit("Unexpected issues or ugly errors may occur!")
        await asyncio.sleep(3)
        private = True
    reply = await event.get_reply_message()
    if event.pattern_match.group(1) is not None:
        userid = event.pattern_match.group(1)
    elif reply is not None:
        userid = reply.sender_id
    elif private:
        userid = event.chat_id
    else:
        return await event.edit(
            "Please reply to a user or add their into the command to ungmute them."
        )
    event.chat_id
    if not is_muted(userid, "gmute"):
        return await event.edit("This user is not gmuted")
    try:
        unmute(userid, "gmute")
    except Exception as e:
        await event.edit("Error occured!\nError is " + str(e))
    else:
        await event.edit("Successfully ungmuted that person")


@command(incoming=True)
async def watcher(event):
    if is_muted(event.sender_id, "gmute"):
        await event.delete()

@register(outgoing=True, pattern=r"^\.gcast(?: |$)(.*)")
async def gcast(event):
    xx = event.pattern_match.group(1)
    if not xx:
        return await event.edit("`Berikan aku teks`")
    tt = event.text
    msg = tt[6:]
    kk = await event.edit("`Proses Mengirim Pesan Broadcast...`")
    er = 0
    done = 0
    async for x in bot.iter_dialogs():
        if x.is_group:
            chat = x.id
            try:
                done += 1
                await bot.send_message(chat, msg)
            except BaseException:
                er += 1
    await kk.edit(f"Done in {done} chats, error in {er} chat(s)")


@register(outgoing=True, pattern=r"^\.gucast(?: |$)(.*)")
async def gucast(event):
    xx = event.pattern_match.group(1)
    if not xx:
        return await event.edit("`Berikan aku teks`")
    tt = event.text
    msg = tt[7:]
    kk = await event.edit("`Proses Mengirim Pesan Broadcast...`")
    er = 0
    done = 0
    async for x in bot.iter_dialogs():
        if x.is_user and not x.entity.bot:
            chat = x.id
            try:
                done += 1
                await bot.send_message(chat, msg)
            except BaseException:
                er += 1
    await kk.edit(f"Done in {done} chats, error in {er} chat(s)")

#XBot-Remix    

from telethon.errors.rpcerrorlist import (UserIdInvalidError,
                                            MessageTooLongError)
from telethon.tl.functions.channels import (EditAdminRequest,
                                              EditBannedRequest,
                                                EditPhotoRequest)
from telethon.tl.functions.messages import UpdatePinnedMessageRequest
from telethon.tl.types import (ChannelParticipantsAdmins,
                                 ChatAdminRights,
                                   ChatBannedRights,
                                     MessageEntityMentionName,
                                       MessageMediaPhoto)
from userbot.utils import register, errors_handler
from userbot.utils import admin_cmd

async def get_full_user(event):  
    args = event.pattern_match.group(1).split(':', 1)
    extra = None
    if event.reply_to_msg_id and len(args) != 2:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.sender_id)
        extra = event.pattern_match.group(1)
    elif len(args[0]) > 0:
        user = args[0]
        if len(args) == 2:
            extra = args[1]
        if user.isnumeric():
            user = int(user)
        if not user:
            await event.edit("`Itz not possible without an user ID`")
            return
        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except Exception as err:
            return await event.edit("Error... Please report at @TamilsuPPorT", str(err))
    return user_obj, extra

async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)
    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        await event.edit(str(err))
        return None
    return user_obj
@borg.on(admin_cmd(pattern="gpromote ?(.*)"))
async def gben(userbot):
    dc = dark = userbot
    i = 0
    sender = await dc.get_sender()
    me = await userbot.client.get_me()
    await dark.edit("`promoting...`")
    my_mention = "[{}](tg://user?id={})".format(me.first_name, me.id)
    f"@{me.username}" if me.username else my_mention
    await userbot.get_chat()
    if userbot.is_private:
        user = userbot.chat
        rank = userbot.pattern_match.group(1)
    else:
        userbot.chat.title
    try:
        user, rank = await get_full_user(userbot)
    except:
        pass
    if me == user:
       k = await dark.edit("U want to promote urself 😑😑 waao..")
       return
    try:
        if not rank:
            rank = "ㅤㅤ"
    except:
        return await dark.edit('**Something W3NT Wrong 🤔**')
    if user:
        telchanel = [d.entity.id
                     for d in await userbot.client.get_dialogs()
                     if (d.is_group or d.is_channel)
                     ]
        rgt = ChatAdminRights(add_admins=False,
                               invite_users=True,
                                change_info=False,
                                 ban_users=True,
                                  delete_messages=True,
                                   pin_messages=True)
        for x in telchanel:
          try:
             await userbot.client(EditAdminRequest(x, user, rgt, rank))
             i += 1
             await dark.edit(f"**Promoted in Chats **: `{i}`")
          except:
             pass
    else:
        await dark.edit('**Reply to a user you dumbo !!**')
    return await dark.edit(
        f"**Globally promoted [{user.first_name}](tg://user?id={user.id})\n On Chats😏 : {i} **"
    )
@borg.on(admin_cmd(pattern="gdemote ?(.*)"))
async def gben(userbot):
    dc = dark = userbot
    i = 0
    sender = await dc.get_sender()
    me = await userbot.client.get_me()
    await dark.edit("`demoting...`")
    my_mention = "[{}](tg://user?id={})".format(me.first_name, me.id)
    f"@{me.username}" if me.username else my_mention
    await userbot.get_chat()
    if userbot.is_private:
        user = userbot.chat
        rank = userbot.pattern_match.group(1)
    else:
        userbot.chat.title
    try:
        user, rank = await get_full_user(userbot)
    except:
        pass
    if me == user:
       k = await dark.edit("U want to demote urself 😑😑 waao..")
       return
    try:
        if not rank:
            rank = "ㅤㅤ"
    except:
        return await dark.edit('**Something W3NT Wrong 🤔**')
    if user:
        telchanel = [d.entity.id
                     for d in await userbot.client.get_dialogs()
                     if (d.is_group or d.is_channel)
                     ]
        rgt = ChatAdminRights(add_admins=None,
                               invite_users=None,
                                change_info=None,
                                 ban_users=None,
                                  delete_messages=None,
                                   pin_messages=None)
        for x in telchanel:
          try:
             await userbot.client(EditAdminRequest(x, user, rgt, rank))
             i += 1
             await dark.edit(f"**Demoted in Chats **: `{i}`")
          except:
             pass
    else:
        await dark.edit('**Reply to a user you dumbo !!**')
    return await dark.edit(
        f"**Globally Demoted [{user.first_name}](tg://user?id={user.id})\n On Chats😏 : {i} **"
    )

CMD_HELP.update(
    {
        "Globaltools":
        "╼•∘ 🅲🅼🅽🅳 ∘•╾  : `.gmute <replying to user message>`\
\n╼•∘ 🆄🆂🅰️🅶🅴 ∘•╾ Gmute User And Delete His Msg.\
\n\n╼•∘ 🅲🅼🅽🅳 ∘•╾  : `.ungmute <replying to user message>`\
\n╼•∘ 🆄🆂🅰️🅶🅴 ∘•╾ UnGmute User And Stops Deleting His Msgs.\
\n\n╼•∘ 🅲🅼🅽🅳 ∘•╾  : `.gban <replying to user message>`\
\n╼•∘ 🆄🆂🅰️🅶🅴 ∘•╾  Gban User And Blow Him From Your Groups\
\n\n╼•∘ 🅲🅼🅽🅳 ∘•╾  : `.ungban <replying to user message>`\
\n╼•∘ 🆄🆂🅰️🅶🅴 ∘•╾ Ugban User.\
\n\n╼•∘ 🅲🅼🅽🅳 ∘•╾  : `.gban <replying to user message>`\
\n╼•∘ 🆄🆂🅰️🅶🅴 ∘•╾  Gban User And Blow Him From Your Groups\
\n\n╼•∘ 🅲🅼🅽🅳 ∘•╾  : `.ungban <replying to user message>`\
\n╼•∘ 🆄🆂🅰️🅶🅴 ∘•╾ Ugban User."

    }
)
