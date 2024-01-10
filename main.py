import asyncio
import logging
from warnings import filterwarnings
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Bot, Message, ChatMember, error, warnings
from telegram.constants import ParseMode, MessageLimit
from telegram.ext import Application, CommandHandler, ContextTypes, filters, MessageHandler, PicklePersistence, \
    ConversationHandler, CallbackQueryHandler
import pytz
import datetime

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=warnings.PTBUserWarning)

PRIVATE_CHAT_ID = -1002068070497

sub_chat = -1001546627098
faddmsg = "faddmsg"
fshowmsg = "fshowmsg"
fdelmsg = "fdelmsg"
faddmsgs = "faddmsgs"
fclearids = "fclearids"
feditmsg = "feditmsg"
feditmsgtext = "feditmsgtext"

(SB_Users_CB, Users_CB, Msgs_CB, Msg_CB, Del_Msg_CB, Edit_Msg_CB, Edit_MsgText_Button_CB, Edit_Msg_Button_CB, Add_Msg_CB, Add_Msgs_CB, Post_CB,
 Clear_IDs_CB,
 Close_CB, Back_CB,
 ConvBack_CB, NextPage_CB, BackPage_CB, ConfClearIDs_CB, NotConfClearIDs_CB, apply_edit_button_CB) = (
    "SB_Users_CB", "Users_CB", "Msgs_CB", "Msg_CB", "Del_Msg_CB", "Edit_Msg_CB","Edit_MsgText_Button_CB", "Edit_Msg_Button_CB", "Add_Msg_CB", "Add_Msgs_CB", "Post_CB",
    "Clear_IDs_CB", "Close_CB", "Back_CB", "ConvBack_CB", "NextPage", "BackPage", "ConfClearIDs_CB",
    "NotConfClearIDs_CB", "apply_edit_button_CB")

BOT_TOKEN = "6919559774:AAFnSF34gZgkIJt7Lb0d92vle34r87PpSmo"

PagesButtons = InlineKeyboardMarkup([[InlineKeyboardButton(text="Next", callback_data=NextPage_CB),
                                      InlineKeyboardButton(text="Back", callback_data=BackPage_CB)],
                                     [InlineKeyboardButton(text="عودة 🔙", callback_data=Back_CB)]])

menu_button = InlineKeyboardMarkup(
    [[InlineKeyboardButton(text="🙎‍♂️🙍‍♀️ SB Users", callback_data=SB_Users_CB),
      InlineKeyboardButton(text="🙎‍♂️️ Users", callback_data=Users_CB)],
     [InlineKeyboardButton(text="📑 Msgs", callback_data=Msgs_CB),
      InlineKeyboardButton(text="📄 Msg", callback_data=Msg_CB)],
     [InlineKeyboardButton(text="🧨 Del Msg", callback_data=Del_Msg_CB),
      InlineKeyboardButton(text="🔧 Edit Msg", callback_data=Edit_Msg_CB)],
     [InlineKeyboardButton(text="➕➕ Add Msgs", callback_data=Add_Msgs_CB),
      InlineKeyboardButton(text="➕ Add Msg", callback_data=Add_Msg_CB)],
     [InlineKeyboardButton(text="🗑 Clear IDs", callback_data=Clear_IDs_CB),
      InlineKeyboardButton(text="📝 Post", callback_data=Post_CB)],
     [InlineKeyboardButton(text="❌ Close", callback_data=Close_CB)]]
)
back_button = InlineKeyboardMarkup([[InlineKeyboardButton(text="عودة 🔙", callback_data=Back_CB)]])
apply_edit_buttons = InlineKeyboardMarkup([[InlineKeyboardButton(text="نشر", callback_data=apply_edit_button_CB)]
                                              ,[InlineKeyboardButton(text="عودة 🔙", callback_data=Back_CB)]])
edit_msg_buttons = InlineKeyboardMarkup([[InlineKeyboardButton(text="تعديل النص", callback_data=Edit_MsgText_Button_CB)],
                                         [InlineKeyboardButton(text="عودة 🔙", callback_data=Back_CB)]])
ConvBack_button = InlineKeyboardMarkup([[InlineKeyboardButton(text="عودة 🔙", callback_data=ConvBack_CB)]])
ConfClearIDs_button = InlineKeyboardMarkup([[InlineKeyboardButton(text="تاكيد", callback_data=ConfClearIDs_CB),
                                             InlineKeyboardButton(text="الغاء", callback_data=NotConfClearIDs_CB)]])

CHOOSING, ConAns, link, photo, text, post, button, review, review0, link1, photo1, text1, button1 = range(13)
post1, post2 = range(2)

Anser, Anser1, Anser2, Anser3 = range(4)

PEA, EM, EditLink, EditText, EditMsgId, EditPhoto, EditButton = range(7)


async def check_for_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    bot = (await Bot(BOT_TOKEN).get_me())
    bot_name = bot.username
    if update.effective_chat.id == PRIVATE_CHAT_ID:
        bot_data = context.bot_data
        if "msgs_data" not in bot_data:
            context.bot_data.setdefault("msgs_data", {})

        msg_id = update.effective_message.message_id
        app_name = update.effective_message.document.file_name
        app_size = update.effective_message.document.file_size
        mydict2 = {msg_id: {1: app_name, 2: app_size}}
        AppLink0 = f"https://t.me/{bot_name}?start={update.effective_message.id}"
        AppLink = f'<a href="{AppLink0}">AppLink</a>'
        bot_data.get("msgs_data").update(mydict2)
        text = (f"<code>###App Name###</code>\n"
                f"<code>{app_name}</code>\n\n"
                f"###{AppLink}###")
        await context.bot.send_message(text=text, chat_id=PRIVATE_CHAT_ID, parse_mode=ParseMode.HTML,
                                       disable_web_page_preview=True)
        await asyncio.sleep(1)


async def ForwardMsg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user_id = update.effective_user.id
    bot_data = context.bot_data
    user_name = update.effective_user.full_name
    chat_id = sub_chat
    if "Url" not in bot_data:
        bot_data.setdefault("Url", "https://short-jambo.com/Zm8GgeL")
    if "KeyUrl" not in bot_data:
        bot_data.setdefault("KeyUrl", "SAO")
    chat_member = await Bot(BOT_TOKEN).getChatMember(chat_id, user_id)
    chat_member_list = [ChatMember.MEMBER, ChatMember.OWNER, ChatMember.ADMINISTRATOR]
    if "subs" not in bot_data:
        bot_data.setdefault("subs", {})
    if "user_ids" not in bot_data:
        bot_data.setdefault("user_ids", {})
    if chat_member.status in chat_member_list and user_id not in bot_data.get("subs"):
        if user_id not in bot_data.get("subs"):
            mydict2 = {user_id: user_name}
            bot_data.get("subs").update(mydict2)
    elif chat_member.status not in chat_member_list:
        if user_id in bot_data.get("subs", {}):
            del bot_data["subs"][user_id]

        url = f"https://t.me/{context.bot.username}"
        text = "انت لست مشتركا بالقناة قم بالشتراك ثم اعد المحاولة"
        keyboard = InlineKeyboardMarkup.from_button(
            InlineKeyboardButton(text="اشتراك", url=url)
        )
        await update.message.reply_text(text, reply_markup=keyboard)
        await asyncio.sleep(5)
    try:
        if str(context.args[0]) == bot_data["KeyUrl"] and chat.id not in bot_data.get("user_ids",
                                                                                      {}) and chat.id in bot_data.get(
            "subs",
            {}):
            mydict2 = {user_id: user_name}
            bot_data.get("user_ids").update(mydict2)
            await update.effective_message.reply_text(f"شكرا {user_name}. على دعمك. \n يمكنك الان تحميل التطبيقات")
            return
    except (IndexError, ValueError):
        pass
    try:

        if chat.id not in bot_data.get("user_ids", {}) and chat.id in bot_data.get("subs", {}):
            url = bot_data["Url"]
            videolink = f'<a href="https://t.me/test12e8/827">شاهد هذا الفيديو</a>'
            text = (f"""⚙️ البوت غير مفعل!

لتفعيل البوت بشكل مجاني، عليك الضغط على الزر في الأسفل، اذا كنت لاتعرف كيفية تفعيل البوت {videolink}.
            """)
            keyboard = InlineKeyboardMarkup.from_button(
                InlineKeyboardButton(text="⚡ تفعيل البوت ⚡", url=url)
            )
            await update.message.reply_text(text, reply_markup=keyboard, parse_mode=ParseMode.HTML,
                                            disable_web_page_preview=True)
            await asyncio.sleep(3)
    except (IndexError, ValueError):
        pass
    try:
        if chat.id in bot_data.get("user_ids", {}) and chat.id in bot_data.get("subs", {}):

            if (context.args[0]).isdigit() and int(context.args[0]) in bot_data["msgs_data"]:
                if int(context.args[0]) > 1 and chat.id in bot_data.get("user_ids", {}) and chat.id in bot_data.get(
                        "subs",
                        {}):
                    await context.bot.forward_message(chat_id=update.effective_chat.id, from_chat_id=PRIVATE_CHAT_ID,
                                                      message_id=int(context.args[0]), protect_content=True)
                    await asyncio.sleep(2)
    except (IndexError, ValueError):
        await update.effective_message.reply_text("لتحميل تطبيق استخدم رابطه الموجود في القناة")


async def back_to_menu0(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.callback_query.edit_message_text("⚙️ قائمة الادوات:", reply_markup=menu_button)
    except (error.BadRequest):
        await update.callback_query.edit_message_caption("⚙️ قائمة الادوات:", reply_markup=menu_button)


async def ConvBackToMenu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.callback_query.edit_message_text("⚙️ قائمة الادوات:", reply_markup=menu_button)
        return ConversationHandler.END
    except ():
        await update.callback_query.edit_message_caption("⚙️ قائمة الادوات:", reply_markup=menu_button)
        return ConversationHandler.END


async def NextPage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    if user_data["PagesConter"] < user_data["PagesNumber"] and user_data["PagesConter"] > -user_data["PagesNumber"]:
        context.user_data["PagesConter"] += 1
        await update.callback_query.edit_message_text(user_data["Pages"][user_data["PagesConter"]],
                                                      reply_markup=PagesButtons, parse_mode=ParseMode.HTML)
    else:
        context.user_data["PagesConter"] = 0
        await update.callback_query.edit_message_text(user_data["Pages"][0], reply_markup=PagesButtons,
                                                      parse_mode=ParseMode.HTML)


async def BackPage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    if user_data["PagesConter"] < user_data["PagesNumber"] and user_data["PagesConter"] > -user_data["PagesNumber"]:
        context.user_data["PagesConter"] -= 1
        await update.callback_query.edit_message_text(user_data["Pages"][user_data["PagesConter"]],
                                                      reply_markup=PagesButtons, parse_mode=ParseMode.HTML)
    else:
        context.user_data["PagesConter"] = 0
        await update.callback_query.edit_message_text(user_data["Pages"][0], reply_markup=PagesButtons,
                                                      parse_mode=ParseMode.HTML)


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("⚙️ قائمة الادوات:", reply_markup=menu_button)
    except (error.BadRequest):
        print("ERR3")


async def msg_cuter(update, context, text, lists):
    if len(text) <= MessageLimit.MAX_TEXT_LENGTH:
        return await update.callback_query.edit_message_text(text="\n".join(lists), parse_mode=ParseMode.HTML,
                                                             disable_web_page_preview=True, reply_markup=back_button)
    else:
        parts = []
        while len(text) > 0:
            if len(text) > MessageLimit.MAX_TEXT_LENGTH:
                part = text[:MessageLimit.MAX_TEXT_LENGTH]
                first_lnbr = part.rfind('\n')
                if first_lnbr != -1:
                    parts.append(part[:first_lnbr])
                    text = text[(first_lnbr + 1):]
                else:
                    parts.append(part)
                    text = text[MessageLimit.MAX_TEXT_LENGTH:]
            else:
                parts.append(text)
                break
        else:
            print("Out Of Index")

        context.user_data["Pages"] = parts
        context.user_data["PagesConter"] = 0
        context.user_data["PagesNumber"] = len(parts)
        if context.user_data["PagesNumber"] == 1:
            await update.callback_query.edit_message_text(parts[0],
                                                          parse_mode=ParseMode.HTML)
        else:
            await update.callback_query.edit_message_text(parts[0], reply_markup=PagesButtons,
                                                          parse_mode=ParseMode.HTML)

        await asyncio.sleep(2)


async def show_bot_start_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot_data_subs = context.bot_data.get("subs", {})
    lists = ["قائمة تشغيل البوت:"]
    if bot_data_subs:
        for i, (user_id, user_name) in enumerate(bot_data_subs.items(), start=1):
            lists.append(f"{i}. {user_id} | {user_name}")

        text = "\n".join(lists)

        await msg_cuter(update, context, text, lists)

    else:
        await update.callback_query.edit_message_text('قائمة تشغيل البوت فارغة', reply_markup=back_button,
                                                      parse_mode=ParseMode.HTML)


async def show_users_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot_data_ids = context.bot_data.get("user_ids", {})
    lists = [":قائمة المستخدمين"]
    if bot_data_ids:
        for i, (user_id, user_name) in enumerate(bot_data_ids.items(), start=1):
            user_list = f"{i}. {user_id} | {user_name}"
            lists.append(user_list)

        text = "\n".join(lists)

        await msg_cuter(update, context, text, lists)

    else:
        await update.callback_query.edit_message_text('قائمة المستخدمين فارغة', reply_markup=back_button,
                                                      parse_mode=ParseMode.HTML)


async def show_msgs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    channel_id = str(PRIVATE_CHAT_ID)
    bot = (await Bot(BOT_TOKEN).get_me())
    bot_name = bot.username
    channel_id = channel_id[3:]
    bot_data = context.bot_data.get("msgs_data", {})
    if bot_data:
        lists = ["قائمة الرسائل المحفوظة:"]
        for i, (msg_id, msg_info) in enumerate(bot_data.items(), start=1):
            app_size = msg_info.get(2, "None")
            app_name = msg_info.get(1, "None")
            app_size_mb = app_size / 1_024_000 if app_size != "None" else "None"
            deepurl0 = f"https://t.me/{bot_name}?start={msg_id}"
            deepurl = f'<a href="{deepurl0}">Link</a>'
            url = f"https://t.me/c/{channel_id}/{msg_id}"
            msg_id1 = f'<a href="{url}">{msg_id}</a>'
            app_size_mb_f = f"{app_size_mb:.2f}" if app_size_mb != "None" else "None"
            msg_list = (f"{i}. ID: {msg_id1} - {deepurl}\n"
                        f"App Name: <code>{(app_name)}</code> \n"
                        f"App Size: {app_size_mb_f} MB \n")
            lists.append(msg_list)
        text = "\n".join(lists)

        await msg_cuter(update, context, text, lists)


    else:
        await update.message.reply_text('قائمة الرسائل المحفوظة فارغة')


async def FShowMsg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.edit_message_text(text="قم بتحويل الرسالة المراد اظهارها من قناة السحابه",
                                                  reply_markup=back_button)
    context.user_data["callback_query.id"] = update.callback_query.message.id
    return fshowmsg


async def ShowMsg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = update.message.forward_from_message_id
        await update.message.delete()
        channel_id = str(PRIVATE_CHAT_ID)
        bot = (await Bot(BOT_TOKEN).get_me())
        bot_name = bot.username
        channel_id = channel_id[3:]
        if "msgs_data" not in context.bot_data:
            context.bot_data.setdefault("msgs_data", {})
        bot_data = context.bot_data.get("msgs_data", {})

        if args in bot_data:

            value = bot_data[int(args)]
            app_size = value[2]
            app_name = value[1]
            if app_size != 'None':
                app_size_mb = f"{app_size / 1_049_890:.2f} MB"
            else:
                app_size_mb = 'NoSize'
            deepurl0 = f"https://t.me/{bot_name}?start={args}"
            deepurl = f'<a href="{deepurl0}">Link</a>'
            url = f"https://t.me/c/{channel_id}/{args}"
            msg_id1 = f'<a href="{url}">{args}</a>'
            msg_list = (f"ID: {msg_id1} - {deepurl}\n"
                        f"App Name: <code>{(app_name)}</code> \n"
                        f"App Size: {app_size_mb} \n")
            await Bot(BOT_TOKEN).edit_message_text(text=msg_list, chat_id=update.effective_chat.id,
                                                   message_id=context.user_data["callback_query.id"],
                                                   reply_markup=back_button, parse_mode=ParseMode.HTML)
            return ConversationHandler.END


        else:
            await Bot(BOT_TOKEN).edit_message_text(text="الرسالة غير مضافة.", chat_id=update.effective_chat.id,
                                                   message_id=context.user_data["callback_query.id"],
                                                   reply_markup=back_button)
            return ConversationHandler.END

    except (IndexError, ValueError):
        await update.message.reply_text("انت لم تقم بتحديد الرسالة.")
        return ConversationHandler.END


async def FDelMsg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.edit_message_text(text="قم بتحويل الرسالة المراد حذفها من قناة السحابه",
                                                  reply_markup=ConvBack_button)
    context.user_data["callback_query.id"] = update.callback_query.message.id
    return fdelmsg


async def DelMsg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "msgs_data" not in context.bot_data:
        context.bot_data.setdefault("msgs_data", {})
    bot_data = context.bot_data.get("msgs_data", {})
    args = update.message.forward_from_message_id
    await update.message.delete()
    if bot_data:
        if args in bot_data:
            bot_data.pop(args)
            print(args)
            await Bot(BOT_TOKEN).edit_message_text(text="تم حذف الرسالة بنجاح.", chat_id=update.effective_chat.id,
                                                   message_id=context.user_data["callback_query.id"],
                                                   reply_markup=back_button)
            return ConversationHandler.END
        else:
            await Bot(BOT_TOKEN).edit_message_text(text="الرسالة غير موجودة.",
                                                   chat_id=update.effective_chat.id,
                                                   message_id=context.user_data["callback_query.id"],
                                                   reply_markup=back_button)
            return ConversationHandler.END
    else:
        await Bot(BOT_TOKEN).edit_message_text(text="لا يوجد رسائل لحذفها.",
                                               chat_id=update.effective_chat.id,
                                               message_id=context.user_data["callback_query.id"],
                                               reply_markup=back_button)
        return ConversationHandler.END


async def FEditMsg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.edit_message_text("قم بتحويل الرسالة المراد تعديلها من القناة الرئيسيه",
                                                  reply_markup=ConvBack_button)
    context.user_data["callback_query.id"] = update.callback_query.message.id
    return feditmsg


async def EditMsg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["forward_msg_id"] = update.message.forward_from_message_id
    context.user_data["forward_msg_text"] = update.message.text
    context.user_data["forward_from_chat"] = update.message.forward_from_chat.id
    print(update.message.document, update.message.photo, update.message.caption, update.message, sep='\n')
    await update.message.delete()
    await Bot(BOT_TOKEN).edit_message_text(text=context.user_data["forward_msg_text"],
                                           chat_id=update.effective_chat.id,
                                           message_id=context.user_data["callback_query.id"],
                                           reply_markup=edit_msg_buttons)
    return ConversationHandler.END


async def fedit_msg_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.edit_message_text("قم بارسال النص الجديد", reply_markup=ConvBack_button)
    return feditmsgtext


async def edit_msg_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["forward_msg_text"] = update.effective_message.text
    await Bot(BOT_TOKEN).edit_message_text(text=f'النص الجديد: \n'
                                                f'{context.user_data["forward_msg_text"]}',
                                           chat_id=update.effective_chat.id,
                                           message_id=context.user_data["callback_query.id"],
                                           reply_markup=apply_edit_buttons)
    return ConversationHandler.END
async def fapply_edit_msg_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg_id = context.user_data["forward_msg_id"]
    forward_from_chat_id = context.user_data["forward_from_chat"]
    await context.bot.edit_message_text(text=f'تم تحديث نص الرسالة: \n'
                                                f'{context.user_data["forward_msg_text"]}',
                                           chat_id=update.effective_chat.id,
                                           message_id=context.user_data["callback_query.id"],
                                           reply_markup=back_button)
    await context.bot.edit_message_text(text=context.user_data["forward_msg_text"],
                                           chat_id=forward_from_chat_id,
                                           message_id=msg_id)


async def POST(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.edit_message_text("قم بارسال المنشور مع صورة وبهذا الشكل\n"
                                                  "نص المنشور-نص الزر-رابط الزر", reply_markup=ConvBack_button)
    print(1)
    return post1


async def POST_2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['photo'] = update.effective_message.photo[-1].file_id
    context.user_data['caption'] = update.effective_message.caption
    splited_caption = context.user_data['caption'].split(sep="-")
    if len(splited_caption) == 3:
        context.user_data['text'] = splited_caption[0]
        context.user_data['button'] = splited_caption[1]

        print(2)
        if splited_caption[2].startswith('http') or splited_caption[2].startswith('https'):
            context.user_data['link'] = splited_caption[2]
            inlineKeyboardButton = InlineKeyboardButton(text=context.user_data['button'], url=context.user_data['link'])
            await update.message.reply_text("المنشور الحالي:")
            button = InlineKeyboardMarkup(
                [[inlineKeyboardButton],
                 [InlineKeyboardButton(text="عودة 🔙", callback_data=ConvBack_CB)]])
            await update.message.reply_photo(photo=context.user_data['photo'], caption=context.user_data['text'],
                                             reply_markup=button)
    elif len(splited_caption) > 3:
        context.user_data['text'] = splited_caption.pop(0)
        buttons_link = [i for i in splited_caption if splited_caption.index(i) % 2 != 0]
        buttons_name = [i for i in splited_caption if splited_caption.index(i) % 2 == 0]
        Buttons_step1 = []
        Buttons_step2 = []
        Buttons_step3 = []
        for i, ii in enumerate(buttons_link):
            inlineKeyboardButton = InlineKeyboardButton(text=buttons_name[i], url=buttons_link[i])
            Buttons_step1.append(inlineKeyboardButton)
            if len(Buttons_step1) == 2:
                Buttons_step2.append(Buttons_step1.copy())
                Buttons_step3.append(Buttons_step1.copy())
                Buttons_step1.clear()
        if Buttons_step1:
            Buttons_step3.append(Buttons_step1.copy())
            context.user_data['user buttons'] = Buttons_step3
            Buttons_step2.append(Buttons_step1.copy())
            Buttons_step1.clear()
            Buttons_step2.append([InlineKeyboardButton(text="عودة 🔙", callback_data=ConvBack_CB)])
        await update.message.reply_text("المنشور الحالي:")
        button = InlineKeyboardMarkup(Buttons_step2)
        await update.message.reply_photo(photo=context.user_data['photo'], caption=context.user_data['text'],
                                         reply_markup=button)
        print(buttons_name, buttons_link, Buttons_step1, Buttons_step2, context.user_data['user buttons'], sep='\n')
    return post2


async def create_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    button = InlineKeyboardMarkup(context.user_data['user buttons'])
    await context.bot.send_photo(photo=context.user_data['photo'], caption=context.user_data['text'], chat_id=sub_chat,
                                 reply_markup=button)
    return ConversationHandler.END


async def close_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.delete_message()


async def FClearIDs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.edit_message_text("هل انت متاكد من حذف قائمة المستخدمين؟",
                                                  reply_markup=ConfClearIDs_button)
    context.user_data["callback_query.id"] = update.callback_query.message.id


async def NotConfClearIDs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.edit_message_text("⚙️ قائمة الادوات:", reply_markup=menu_button)


async def ClearIDs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text1 = "تم الغاء صلاحيات وصلول جميع المستخدمين"
    if context.bot_data.get("subs") and context.bot_data.get("user_ids"):
        context.bot_data.get("subs").clear()
        context.bot_data.get("user_ids").clear()
        await Bot(BOT_TOKEN).edit_message_text(f"{text1}\nقائمة تشغيل البوت فارغة\nقائمة المشتركين فارغة",
                                               chat_id=update.effective_chat.id,
                                               message_id=context.user_data["callback_query.id"],
                                               reply_markup=back_button)
    elif not context.bot_data.get("subs") and not context.bot_data.get("user_ids"):
        await Bot(BOT_TOKEN).edit_message_text("قائمة تشغيل البوت فارغة\nقائمة المشتركين فارغة",
                                               chat_id=update.effective_chat.id,
                                               message_id=context.user_data["callback_query.id"],
                                               reply_markup=back_button)
    elif not context.bot_data.get("subs"):
        await Bot(BOT_TOKEN).edit_message_text(f"{text1}\nقائمة تشغيل البوت فارغة",
                                               chat_id=update.effective_chat.id,
                                               message_id=context.user_data["callback_query.id"],
                                               reply_markup=back_button)

    elif not context.bot_data.get("user_ids"):
        await Bot(BOT_TOKEN).edit_message_text(f"{text1}\nقائمة المشتركين فارغة", chat_id=update.effective_chat.id,
                                               message_id=context.user_data["callback_query.id"],
                                               reply_markup=back_button)


async def AutoClearids(context: ContextTypes.DEFAULT_TYPE):
    text1 = "تم الغاء صلاحيات وصلول جميع المستخدمين"
    if context.bot_data.get("subs"):
        context.bot_data.get("subs").clear()
    elif not context.bot_data.get("subs"):
        await context.bot.sendMessage(chat_id=789221262, text="قائمة تشغيل البوت فارغة")
    if context.bot_data.get("user_ids"):
        context.bot_data.get("user_ids").clear()
    elif not context.bot_data.get("user_ids"):
        await context.bot.sendMessage(chat_id=789221262, text="قائمة المشتركين فارغة")
    await context.bot.sendMessage(chat_id=789221262, text=text1)
    await context.bot.sendMessage(chat_id=5475147476, text=text1)


async def FAddMsgs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    await update.callback_query.edit_message_text("قم بتحويل الرسائل المراد اضافتها", reply_markup=ConvBack_button)
    context.user_data["callback_query.id"] = update.callback_query.message.id
    return faddmsgs


async def AddMsgs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    bot = (await Bot(BOT_TOKEN).get_me())
    bot_name = bot.username
    bot_data = context.bot_data
    if "msgs_data" not in bot_data:
        context.bot_data.setdefault("msgs_data", {})

    msg_id = update.effective_message.forward_from_message_id
    app_name = update.effective_message.document.file_name
    app_size = update.effective_message.document.file_size
    mydict2 = {msg_id: {1: app_name, 2: app_size}}
    AppLink0 = f"https://t.me/{bot_name}?start={update.effective_message.id}"
    AppLink = f'<a href="{AppLink0}">AppLink</a>'
    bot_data.get("msgs_data").update(mydict2)
    text = (f"<code>###App Name###</code>\n"
            f"<code>{app_name}</code>\n\n"
            f"###{AppLink}###")
    await Bot(BOT_TOKEN).edit_message_text(text, chat_id=update.effective_chat.id,
                                           message_id=context.user_data["callback_query.id"],
                                           reply_markup=ConvBack_button, parse_mode=ParseMode.HTML, )
    await asyncio.sleep(1)


async def FAddMsg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.edit_message_text("قم بتحويل الرسالة المراد حفظها من قناة السحابه",
                                                  reply_markup=ConvBack_button)
    context.user_data["callback_query.id"] = update.callback_query.message.id
    return faddmsg


async def AddMsg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg_id = update.message.forward_from_message_id
    bot_data = context.bot_data
    if "msgs_data" not in bot_data:
        context.bot_data.setdefault("msgs_data", {})
    if Message.forward_from_chat:
        if msg_id in context.bot_data.setdefault("msgs_data", {}):
            await Bot(BOT_TOKEN).edit_message_text("الوثيقة موجودة مسبقا.", chat_id=update.effective_chat.id,
                                                   message_id=context.user_data["callback_query.id"],
                                                   reply_markup=back_button)
            await update.message.delete()
            return ConversationHandler.END

        elif update.effective_message.document is not None and update.effective_message.document.file_name is not None and update.effective_message.document.file_size is not None:
            app_name = update.effective_message.document.file_name
            app_size = update.effective_message.document.file_size
            mydict2 = {msg_id: {1: app_name, 2: app_size}}
            bot_data.get("msgs_data").update(mydict2)
            await Bot(BOT_TOKEN).edit_message_text("تم اضافة الوثيقة بنجاح.", chat_id=update.effective_chat.id,
                                                   message_id=context.user_data["callback_query.id"],
                                                   reply_markup=back_button)
            await update.message.delete()
            return ConversationHandler.END

        else:
            msg_id = update.message.forward_from_message_id
            app_name = "None"
            app_size = "None"
            bot_data = context.bot_data
            if "msgs_data" not in bot_data:
                context.bot_data.setdefault("msgs_data", {})
            mydict2 = {msg_id: {1: app_name, 2: app_size}}
            bot_data.get("msgs_data").update(mydict2)
            await Bot(BOT_TOKEN).edit_message_text("تم اضافة الرسالة بنجاح.", chat_id=update.effective_chat.id,
                                                   message_id=context.user_data["callback_query.id"],
                                                   reply_markup=back_button)
            await update.message.delete()
            return ConversationHandler.END
    else:
        await Bot(BOT_TOKEN).edit_message_text("ليست رسالة محولة من قناة.", chat_id=update.effective_chat.id,
                                               message_id=context.user_data["callback_query.id"],
                                               reply_markup=back_button)
        return ConversationHandler.END


async def StartChangekeyUrl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text="هل انت متاكد من تغيير المفتاح و الرابط؟")
    return Anser


async def StartChangeKeyUrl_step2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_message.text == "تاكيد":
        await update.message.reply_text(text="قم بارسال الرابط")
        return Anser2
    elif update.effective_message.text == "الغاء":
        return ConversationHandler.END


async def ChangeKeyUrl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot_data = context.bot_data
    if update.effective_message.text.startswith('http') or update.effective_message.text.startswith('https'):
        bot_data["Url"] = update.effective_message.text
        await update.message.reply_text(text="قم بارسال المفتاح")
        return Anser3
    else:
        await update.message.reply_text(text="هذا ليس رابط -> اعد ارسال الرابط")
        return Anser2


async def StartChangeKeyUrl_step3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot_data = context.bot_data
    bot_data["KeyUrl"] = update.effective_message.text
    await update.message.reply_text(text=f"{bot_data['KeyUrl']}تم تغيير المفتاح و الرابط -> المفتاح الحالي: ")
    return ConversationHandler.END


# async def admin_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     help_msg = (f"<code>/CreatePost</code> -> امر يقوم بعمل منشور مع زر\n"
#                 f"<code>/ShowMsgs</code> -> امر اظهار الرسائل المحفوظه\n"
#                 f"<code>/ShowMsg</code> -> امر اظهار رساله محفوظه\n"
#                 f"<code>/DelMsg</code> -> (امر حذف الرسائل المحفوظه عن طريق (رقم الرسالة\n"
#                 f"<code>/AddMsg</code> -> امر يقوم باضافة رسالة الى القائمة المحفوظة\n"
#                 f"<code>/ShowUL</code> -> امر يقوم باظهار قائمة تخطي الاعلان\n"
#                 f"<code>/ShowBSL</code> -> امر يقوم باظهار قائمة تشغيل البوت \n"
#                 f"<code>/ClearIDs</code> -> امر يقوم بحذف مباشر للمستخدمين\n"
#                 f"<code>/UpdateUrl</code> -> امر يقوم بتغيير المفتاح و الرابط\n")
#     await update.message.reply_text(help_msg, parse_mode=ParseMode.HTML, disable_web_page_preview=True)


def main() -> None:
    today = datetime.time(hour=10, minute=0, second=0, tzinfo=pytz.timezone('Asia/Damascus'))
    persistence = PicklePersistence(filepath="bot_data", update_interval=600)
    # defaults = Defaults(tzinfo=pytz.timezone('Asia/Damascus'))
    application = Application.builder().token(BOT_TOKEN).persistence(persistence).build()

    application.add_handler(CommandHandler("start", ForwardMsg))
    PostH = ConversationHandler(
        entry_points=[CallbackQueryHandler(POST, pattern=Post_CB)],
        states={
            post1: [MessageHandler(filters.PHOTO, POST_2)],
            post2: [MessageHandler(filters.Regex("نشر"), create_post)]
        },
        fallbacks=[CallbackQueryHandler(ConvBackToMenu, pattern=ConvBack_CB)]
    )

    DelMsgH = ConversationHandler(
        entry_points=[CallbackQueryHandler(FDelMsg, pattern=Del_Msg_CB)],
        states={
            fdelmsg: [MessageHandler(filters.FORWARDED, DelMsg)],
        },
        fallbacks=[CallbackQueryHandler(ConvBackToMenu, pattern=ConvBack_CB)]
    )

    EditMsgH = ConversationHandler(
        entry_points=[CallbackQueryHandler(FEditMsg, pattern=Edit_Msg_CB)],
        states={
            feditmsg: [MessageHandler(filters.FORWARDED, EditMsg)],
        },
        fallbacks=[MessageHandler(filters.FORWARDED, EditMsg)]
    )

    EditMsgTextH = ConversationHandler(
        entry_points=[CallbackQueryHandler(fedit_msg_text, pattern=Edit_MsgText_Button_CB)],
        states={
            feditmsgtext: [MessageHandler(filters.TEXT, edit_msg_text)],
        },
        fallbacks=[MessageHandler(filters.TEXT, edit_msg_text)]
    )

    ShowMsgH = ConversationHandler(
        entry_points=[CallbackQueryHandler(FShowMsg, pattern=Msg_CB)],
        states={
            fshowmsg: [MessageHandler(filters.FORWARDED, ShowMsg)],
        },
        fallbacks=[CallbackQueryHandler(ConvBackToMenu, pattern=ConvBack_CB)]
    )

    AddMsgsH = ConversationHandler(
        entry_points=[CallbackQueryHandler(FAddMsgs, pattern=Add_Msgs_CB)],
        states={
            faddmsgs: [MessageHandler(filters.FORWARDED, AddMsgs)],
        },
        fallbacks=[CallbackQueryHandler(ConvBackToMenu, pattern=ConvBack_CB)]
    )

    AddMsgH = ConversationHandler(
        entry_points=[CallbackQueryHandler(FAddMsg, pattern=Add_Msg_CB)],
        states={
            faddmsg: [MessageHandler(filters.FORWARDED, AddMsg)],
        },
        fallbacks=[CallbackQueryHandler(ConvBackToMenu, pattern=ConvBack_CB)]
    )

    conv_handler2 = ConversationHandler(
        entry_points=[CommandHandler("UpdateUrl", StartChangekeyUrl, filters.User(user_id=[5475147476, 789221262]))],
        states={
            Anser: [MessageHandler(filters.TEXT, StartChangeKeyUrl_step2)],
            Anser2: [MessageHandler(filters.TEXT, ChangeKeyUrl)],
            Anser3: [MessageHandler(filters.TEXT, StartChangeKeyUrl_step3)]
        },
        fallbacks=[MessageHandler(filters.TEXT, StartChangeKeyUrl_step3)]
    )

    application.add_handler(PostH)
    application.add_handler(AddMsgH)
    application.add_handler(AddMsgsH)
    application.add_handler(ShowMsgH)
    application.add_handler(DelMsgH)
    application.add_handler(EditMsgH)
    application.add_handler(conv_handler2)
    application.add_handler(EditMsgTextH)
    application.add_handler(CallbackQueryHandler(fapply_edit_msg_text, pattern=apply_edit_button_CB))
    application.add_handler(CallbackQueryHandler(FClearIDs, pattern=Clear_IDs_CB))
    application.add_handler(CallbackQueryHandler(NotConfClearIDs, pattern=NotConfClearIDs_CB))
    application.add_handler(CallbackQueryHandler(ClearIDs, pattern=ConfClearIDs_CB))
    application.add_handler(CallbackQueryHandler(close_menu, pattern=Close_CB))
    application.add_handler(CallbackQueryHandler(back_to_menu0, pattern=Back_CB))
    application.add_handler(CallbackQueryHandler(BackPage, pattern=BackPage_CB))
    application.add_handler(CallbackQueryHandler(NextPage, pattern=NextPage_CB))
    application.add_handler(CallbackQueryHandler(show_bot_start_list, pattern=SB_Users_CB))
    application.add_handler(CallbackQueryHandler(show_users_list, pattern=Users_CB))
    application.add_handler(CallbackQueryHandler(show_msgs, pattern=Msgs_CB))

    application.add_handler(
        CommandHandler("menu", menu, filters.ChatType.PRIVATE & filters.User(user_id=[5475147476, 789221262])))

    application.job_queue.run_daily(callback=AutoClearids, time=today)

    application.add_handler(MessageHandler(filters.ChatType.CHANNEL & filters.Document.APK, check_for_file))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
