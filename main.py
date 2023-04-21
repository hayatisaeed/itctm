# in the name of Allah
############### GLOBAL ZONE ################
# Modules:

import telegram
import json
from telegram import *
from telegram.ext import *
import datetime
import random
# from admin import *

# VARIABLES

# TOKEN = "6231214497:AAHTFpTdBKklS9FQieCX3MtaMBak9StrbM8" # replace with your own
TOKEN = "6126767405:AAH4B-wx0ckT6NoMPp6pA3lGoGAU-DxEC9Q" # temp for test
# ADMIN_CHAT_ID = 5514445607 # get your chat id from @RawDataBot
ADMIN_CHAT_ID = 1767064220 # temp for test
CHANNEL_ID = -1001693014687
# Attention: ADMIN_CHAT_ID should be int.


# Load the user data from the JSON file
with open('data.json', 'r') as f:
    data = json.load(f)

# Create an instance of the Telegram bot using the API token provided by BotFather
bot = telegram.Bot(token=TOKEN)

# Create an instance of the Updater class to receive updates from the bot
updater = Updater(token=TOKEN, use_context=True)



# Some constants (used in conv_handlers)

ADMIN_SEND_MESSAGE = 0
FIRST = 0
SECOND = 1
FIRST1 = 0
SECOND1 = 1
FIRST2 = 0
SECOND2 = 1
SEND_BROD = 0
CREDIT = 0
SET_PACK = 0
EDIT_MESSAGE = 0
BUY = 0
CONFIRM_BUY = 1
GET_CONFIGS = 0
GET_TEST = 0
SET_INVITER = 0
GET_DESCRIPTION = 0
GET_NUMBER_OF_MESSAGES = 0
GET_MESSAGES = 1
GET_CARDS = 1
GET_USER_UNLIMITED_TEST = 1

# Fuction to make write operation easier
def write_to_db():
    with open('data.json', 'w') as f:
        json.dump(data, f)












# Define the function to handle the /start command
def start(update, context):
    user_id = update.effective_user.id
    # Add the user to the user data if not already exists

    """
        "credit": "80",
        "services": {},
        "is_blocked": 0,
        "is_invited": 0,
        "inviter_got_commission": 0,
        "commissions": {
            "id": {
                "charged": 0,
                "counted": 0
            }
        }

    """

    if str(user_id) not in data['users']:
        data['users'][str(user_id)] = {'credit': 0, 'services': {}, "is_blocked": 0, "is_invited": 0, "inviter_got_commission": 0, "inviter_id": 0, "commissions": {}, "last_test": 0}
        with open('data.json', 'w') as f:
            json.dump(data, f)
   
    user_joined_channel = 0
    chat_member = bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
    try:
        if chat_member.status == 'member' or chat_member.status == 'administrator' or chat_member.status == 'creator' or chat_member.status == 'owner':
            user_joined_channel = 1
    except:
        user_joined_channel = 0


    if not user_joined_channel:
        keyboard = [[InlineKeyboardButton("عضویت در کانال", url=f"https://t.me/+Jh0kkspDstAzNzBk")], [InlineKeyboardButton("✅عضو شدم", callback_data="start")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=user_id, text=f"لطفا برای استفاده از بات در کانال ما عضو شوید:\n https://t.me/+Jh0kkspDstAzNzBk", reply_markup=reply_markup)
        return None

    # if this is admin of bot
    start_message = data['messages']['start_message']
    start_message.replace('\\n', '\n')
    if (user_id == int(ADMIN_CHAT_ID)):
        keyboard = [[InlineKeyboardButton("Brodcast Message", callback_data=f"brodcast")], [InlineKeyboardButton("Send Config", callback_data=f"admin_send_config"), InlineKeyboardButton("Send Test", callback_data="admin_send_test")], [InlineKeyboardButton("users list", callback_data="admin_users_list")], [InlineKeyboardButton("Packages List", callback_data=f"packages")], [InlineKeyboardButton("Help", callback_data="admin_help")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=user_id, text=f"""
        سلام! به پنل •ادمین• بات  خوش آمدید!

        شما میتوانید از کامند های پایین استفاده بفرمایید:

        /brodcast 
        ارسال پیام به همه‌ی کاربران
        
        /admin_message CHAT_ID 
        برای ارسال پیام دستی به یک آیدی خاص
        
        /set_credit CHAT_ID 
        تعیین دستی موجودی برای یک آیدی خاص
        
        /admin_user_info CHAT_ID 
        دریافت دستی اطلاعات از کاربر خاص
        
        /admin_edit_packages 
        برای ادیت زدن پکیج ها
        
        /admin_users_list 
        لیست کاربران
        
        /admin_send_config 
        ارسال کانفیگ به بات
        
        /admin_send_test 
        ارسال کانفیگ تست
        
        /admin_edit_messages 
        ادیت زدن پیام های بات
        
        /block CHAT_ID 
        مسدود کردن یک کاربر خاص
        
        /unblock CHAT_ID 
        رفع مسدودیت یک کاربر خاص
        
        /lookup_configs 
        نمایش تعداد کانفیگ های موجود
        
        /del_conf ID 
        حذف کانفیگ های یک ID به خصوص
        
        /reply MESSAGE_ID 
        بات پیام با آیدی درخواستی را ریپلای میکند

        /set_description PACKAGE_ID
        برای یک پکیج آیدی خاص توضیح ثبت میکند.

        /set_cards NUMBER_OF_CARDS
        برای تعیین کردن شماره کارت ها

        /del_cards
        برای حذف کردن لیست شماره کارت ها
        
        /add_unlimited_test CHAT_ID
        برای اضافه کردن یک آیدی خاص به لیست معاف از محدودیت هفته‌ای تست

        /remove_from_exception CHAT_ID
        برای حذف یک آیدی به خصوص از معافیت تست

        /db_backup
        برای دریافت فایل دیتابیس بکاپ بات

        """, reply_markup=reply_markup)
    
    # normal users

    else:
        keyboard = [[InlineKeyboardButton("🛒 مشاهده پکیج ها", callback_data=f"packages")], [InlineKeyboardButton("⏰ دریافت تست", callback_data="test_vpn"), InlineKeyboardButton("👨‍🏫 آموزش اتصال", callback_data="tutorial")], [InlineKeyboardButton("📝 اطلاعات اکانت", callback_data="account"), InlineKeyboardButton("💳 کیف پول", callback_data="credit")], [InlineKeyboardButton("👨‍💻 پیام به پشتیبان", callback_data="support")], [InlineKeyboardButton("🆘 راهنما", callback_data="help")], [InlineKeyboardButton("🤝 کمیسیون های شما", callback_data="commission")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        # Send the welcome message to the user
        start_message = data['messages']['start_message']
        if start_message == "":
            start_message = "hi!"
        context.bot.send_message(chat_id=user_id, text=start_message, reply_markup=reply_markup)

########## END GLOBAL ###############
























   
######## ADMIN ZONE ##########
# Global Brodcast message
def brodcast(update, context):
    user_id = update.effective_user.id
    if user_id == ADMIN_CHAT_ID:
        context.bot.send_message(chat_id=ADMIN_CHAT_ID, text='🌏 شما در حال ارسال پیام به همه‌ی کاربران هستید!\n(برای لغو /cancel را ارسال کنید.)')
        return SEND_BROD
    else:
        context.bot.send_message(chat_id=user_id, text='🟥 خطا: شما به این بخش دسترسی ندارید.')
        return ConversationHandler.END
def send_brodcast(update, context):
    user_id = update.effective_user.id
    if user_id != ADMIN_CHAT_ID:
        context.bot.send_message(chat_id=user_id, text='🟥 خطا: شما به این بخش دسترسی ندارید.')
    else:
        num = 0
        for users in data['users']:
            try:
                context.bot.copy_message(chat_id=users, from_chat_id=ADMIN_CHAT_ID, message_id=update.message.message_id)
                num += 1
            except:
                pass
        context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f'DONE!\nsent this message to {num} users.')
    return ConversationHandler.END

# Send message to one user
def admin_message(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    if user_id == ADMIN_CHAT_ID:
        lst = update.message.text.split()
        try:
            lst[1] = int(lst[1])
            context.user_data['id'] = lst[1]
            idd = context.user_data['id']
            context.bot.send_message(chat_id=user_id, text=f'💬 شما در حال پیام خصوصی به {idd} هستید\n( برای لغو /cancel را ارسال کنید..)')
            return FIRST2
        except:
            context.bot.send_message(chat_id=ADMIN_CHAT_ID, text='🟥 خطا: فرمت ارسال پیام نادرست است.')
    else:
        context.bot.send_message(chat_id=user_id, text='🟥 خطا: کامند نادرست است.')
def send_admin_message(update, context):
    user_id = update.effective_user.id
    try:
        context.bot.send_message(chat_id=context.user_data['id'], text='📣 شما یک پیام جدید از ادمین دارید')
        context.bot.copy_message(chat_id=context.user_data['id'], from_chat_id=update.message.chat_id, message_id=update.message.message_id)
        context.bot.send_message(chat_id=ADMIN_CHAT_ID, text='پیام با موفقیت ارسال شد ✅')
    except:
        context.bot.send_message(chat_id=ADMIN_CHAT_ID, text='🟥 خطا: چنین کاربری وجود ندارد یا مشکلی پیش آمده است.')
    return ConversationHandler.END

def set_credit(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    if user_id != ADMIN_CHAT_ID:
        context.bot.send_message(chat_id=user_id, text='🟥 خطا: شما به این بخش دسترسی ندارید.')
        return ConversationHandler.END
    else:
        try:
            context.user_data['chat_id'] = update.message.text.split()[1]
            user_credit = data['users'][update.message.text.split()[1]]['credit']
            context.bot.send_message(chat_id=user_id, text=f"""❕ شما در حال تعیین موجودی برای این کاربر هستید: {context.user_data['chat_id']}.
            این کاربر {user_credit} در کیف پول خود دارد.
            مقدار مد نظر برای این کیف پول را ارسال کنید، و یا برای لغو /cancel را ارسال کنید.
            """)
            return CREDIT
        except:
            context.bot.send_message(chat_id=user_id, text='Invalid format.')
            return ConversationHandler.END
def credit_change(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    if user_id != ADMIN_CHAT_ID:
        context.bot.send_message(chat_id=user_id, text='🟥 خطا: شما به این بخش دسترسی ندارید.')
        return ConversationHandler.END
    else:
        try:
            data['users'][str(context.user_data['chat_id'])]['credit'] = int(update.message.text)
            with open('data.json', 'w') as f:
                json.dump(data, f)
            context.bot.send_message(chat_id=context.user_data['chat_id'], text=f'💲 اعتبار جدید کیف پول شما: {update.message.text}')
            context.bot.send_message(chat_id=user_id, text='انجام شد ✅')
            return ConversationHandler.END
        except:
            context.bot.send_message(chat_id=user_id, text='🟥 خطا: عملیات لغو شد.')
            return ConversationHandler.END

def admin_users_list(update, context):
    user_id = update.effective_user.id
    if (ADMIN_CHAT_ID == user_id):
        s = "👤 لیست کاربران:"
        for users in data['users']:
            s += '\n\nآیدی کاربر: ' + str(users) + ' اعتبار کاربر: ' + str(data['users'][users]['credit'])
        context.bot.send_message(chat_id=user_id, text=s)
    else:
        context.bot.send_message(chat_id=user_id, text='🟥 خطا: شما به این بخش دسترسی ندارید.')

def admin_edit_packages(update, context):
    user_id = update.effective_user.id
    if user_id != ADMIN_CHAT_ID:
        context.bot.send_message(chat_id=user_id, text='🟥 خطا: شما به این بخش دسترسی ندارید.')
        return ConversationHandler.END
    else:
        user_id = update.effective_user.id

        button1 = InlineKeyboardButton("*", callback_data=f"none")
        button2 = InlineKeyboardButton("package name", callback_data="none")
        button3 = InlineKeyboardButton("price", callback_data="none")
        button4 = InlineKeyboardButton("ID", callback_data="none")
        keyboard = [[button4, button1, button2, button3]]

        for i in data['packages']:
            if (i == 'commission_rate'):
                button1 = InlineKeyboardButton("*", callback_data=f"none")
            else:
                button1 = InlineKeyboardButton("Delete", callback_data=f"del_{i}")
            button2 = InlineKeyboardButton(str(data['packages'][str(i)]['name']), callback_data="none")
            button3 = InlineKeyboardButton(str(data['packages'][str(i)]['price']), callback_data="none")
            button4 = InlineKeyboardButton(f"{i}", callback_data="none")

            keyboard.append([button4, button1, button2, button3])

        inline_keyboard = InlineKeyboardMarkup(keyboard)

        msg = data['messages']['packages']
        context.bot.send_message(chat_id=user_id, text=msg, reply_markup=inline_keyboard)

        context.bot.send_message(chat_id=user_id, text="""❕شما در حال ادیت لیست قیمت ها هستید. \nبرای ادامه لطفا یک پیام به فرمت زیر ارسال کنید:

        id name price
        id name price
        id name price
        ...

        توجه کنید که بین اسامی فوق فاصله وجود دارد.
        میتوانید هر تعدادی که خواستید id جدید اضافه کنید، فقط توجه کنید که این آیدی ها به صورت عدد باشند. آیدی با نام تفاوت دارد.

        برنامه برای انجام خودکار عملیات فروش از این آیدی ها استفاده میکند. اما این آیدی ها به کاربران نمایش داده نمیشوند.

        ( برای لغو /cancel را ارسال کنید.)""")
        return SET_PACK

def admin_set_packages(update, context): # use to set packages prices
    user_id = update.effective_user.id
    if user_id != ADMIN_CHAT_ID:
        context.bot.send_message(chat_id=user_id, text='🟥 خطا: شما به این بخش دسترسی ندارید.')
        return ConversationHandler.END
    else:
        msg = update.message.text.split()
        if len(msg) % 3: # odd numbers cant be in corroct form
            context.bot.send_message(chat_id=user_id, text='🟥 خطا: الگوی فوق نادرست است.')
            return ConversationHandler.END
        
        i = 0
        while i < len(msg):
            try:
                data['packages'][msg[i]] = {"name": msg[i + 1], "price": int(msg[i + 2])}
                write_to_db()
            except:
                context.bot.send_message(chat_id=user_id, text=f'📮 امکان ویرایش {msg[i]} به علت یک مشکل وجود نداشت. این مورد تغییر نیافت')
            i += 3

        write_to_db()

        context.bot.send_message(chat_id=user_id, text='Done!')
        s = "\n"
        for i in data['packages']:
            s += i + ' ' + str(data['packages'][i]) + '\n'
        context.bot.send_message(chat_id=user_id, text=f"""
        📊 برای مشاهده‌ی لیست پکیج ها /packages را ارسال کنید.
        """)
        return ConversationHandler.END

def admin_edit_messages(update, context):
    user_id = update.effective_user.id
    if user_id != ADMIN_CHAT_ID:
        context.bot.send_message(chat_id=user_id, text='🟥 خطا: شما به این بخش دسترسی ندارید.')
        return ConversationHandler.END
    else:
        context.bot.send_message(chat_id=user_id, text="""
        ❕ شما در حال ویرایش پیام های بات هستید.
        مطابق زیر عمل کنید:
        اولین کلمه‌ی پیام تان، پیامی باشد که قصد ویرایش آن را دارید. و سپس هر چیزی که قصد دارید با آن پیام جایگزین شود را تایپ کنید.
        to edit packages message, do the same but replace start_message with packages.
        
        🔹 به عنوان مثال: 
        \"
        start_message

        سلام این پیام جدید خوشامد گویی به بات است.
        \"

        🔹 موارد قابل ویرایش:

        start_message: پیام خوش آمد گویی به بات
        packages: پیامی که در بالای لیست قیمت ها قرار میگیرد 
        tutorials_link: لینک آموزش ها      


        برای لغو /cancel را ارسال کنید..

        """)
        return EDIT_MESSAGE
def admin_set_messages(update, context):
    user_id = update.effective_user.id
    if user_id != ADMIN_CHAT_ID:
        context.bot.send_message(chat_id=user_id, text='🟥 خطا: شما به این بخش دسترسی ندارید.')
        return ConversationHandler.END
    else:
        msg = update.message.text.split()
        msgtype = msg[0]
        msg = msg[1:]
        msg = ' '.join(msg)
        msg.replace('\\n', '\n')

        if msgtype not in data['messages']:
            context.bot.send_message(chat_id=user_id, text='🟥 خطا: الگوی متنی اشتباه است.')
            return ConversationHandler.END

        data['messages'][msgtype] = msg
        write_to_db()    

        context.bot.send_message(chat_id=user_id, text='انجام شد ✅')
        return ConversationHandler.END

# admin get user info
def admin_user_info(update, context):
    user_id = update.effective_user.id
    if user_id != ADMIN_CHAT_ID:
        context.bot.send_message(chat_id=user_id, text="🟥 خطا: شما به این بخش دسترسی ندارید.")
    else:
        try:
            if update.message.text[0:4] == 'info':
                idd = int(update.message.text[4:])
            else:
                idd = int(update.message.text.split()[1])
            crdit = data['users'][str(idd)]['credit']
            srvs = data['users'][str(idd)]['services']

            # test
            button1 = InlineKeyboardButton("User Credit", callback_data=f"set_credit{idd}") # 349
            button2 = InlineKeyboardButton("Message to user", callback_data=f"msg{idd}")
            button3 = InlineKeyboardButton("User Info", callback_data=f'info{idd}')
            keyboard = [[button1, button2], [button3]]
            inline_keyboard = InlineKeyboardMarkup(keyboard)
            # End test

            context.bot.send_message(chat_id=user_id, text=f"""
            👤 اطلاعات این کاربر مطابق زیر است:

            آیدی: {idd}
            اعتبار کیف پول: {crdit} تومان
            لیست سرویس‌ها: {str(srvs)}
            """, reply_markup=inline_keyboard)
        except:
            context.bot.send_message(chat_id=user_id, text="🟥 خطا: فرمت پیام ارسالی اشتباه است.")

def admin_help(update, context):
    user_id = update.effective_user.id
    if user_id != ADMIN_CHAT_ID:
        context.bot.send_message(chat_id=user_id, text="🟥 خطا: شما به این بخش دسترسی ندارید.!")
    else:
        context.bot.send_message(chat_id=user_id, text="برای مشاهده‌ی راهنمای کامل کامند ها /start را بزنید.")

def block_user(update, context):
    user_id = update.effective_user.id
    if (user_id != ADMIN_CHAT_ID):
        context.bot.send_message(chat_id=user_id, text="🟥 خطا: شما به این بخش دسترسی ندارید.")
    else:
        try:
            should_block = str(update.message.text.split()[1])
            for i in data['users']:
                if i == should_block:
                    data['users'][i]['is_blocked'] = 1
                    write_to_db()
                    context.bot.send_message(chat_id=should_block, text="⛔️ دسترسی شما توسط ادمین محدود شد: شما نمیتوانید به پشتیبانی پیام ارسال کنید.")
                    context.bot.send_message(chat_id=user_id, text=f"کاربر {should_block} بلاک شد ⛔️")
                    break
            else:
                context.bot.send_message(chat_id=user_id, text="🟥 خطا: چنین کاربری وجود ندارد.")
        except:
            context.bot.send_message(chat_id=user_id, text="🟥 خطا: عملیات لغو شد.")
def unblock_user(update, context):
    user_id = update.effective_user.id
    if (user_id != ADMIN_CHAT_ID):
        context.bot.send_message(chat_id=user_id, text="🟥 خطا: شما به این بخش دسترسی ندارید.")
    else:
        try:
            should_block = str(update.message.text.split()[1])
            for i in data['users']:
                if i == should_block:
                    data['users'][i]['is_blocked'] = 0
                    write_to_db()
                    context.bot.send_message(chat_id=should_block, text="💡 شما توسط ادمین رفع مسدودیت شدید. از اکنون مجددا میتوانید به پشتیبانی پیام ارسال کنید.")
                    context.bot.send_message(chat_id=user_id, text=f"کاربر {should_block} رفع مسدودیت شد. ✅")
                    break
            else:
                context.bot.send_message(chat_id=user_id, text="🟥 خطا: چنین کاربری وجود ندارد.")
        except:
            context.bot.send_message(chat_id=user_id, text="🟥 خطا: عملیات لغو شد.")

def send_config(update, context):
    user_id = update.effective_user.id
    context.user_data['x'] = 0
    context.user_data['got'] = 0

    if (user_id != ADMIN_CHAT_ID):
        context.bot.send_message(chat_id=user_id, text="🟥 خطا: شما به این بخش دسترسی ندارید.")
        return ConversationHandler.END
    else:
        context.bot.send_message(chat_id=user_id, text="👍 حله!\n بهم بگو که چند تا کانفیگ میخوای برام ارسال کنی و برای کدوم پکیج هستن.\nبه این فرمت به من بگو:\nnumber_of_configs service_id\nبرای لغو /cancel را ارسال کنید.")
        return GET_CONFIGS
def get_configs(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    if (user_id != ADMIN_CHAT_ID):
        context.bot.send_message(chat_id=user_id, text="🟥 خطا: شما به این بخش دسترسی ندارید.")
        return ConversationHandler.END
    else:
        if context.user_data['x'] != 0:
            if(context.user_data['got'] == context.user_data['x']):
                context.bot.send_message(chat_id=user_id, text=f"✅ انجام شد \n تعداد {context.user_data['x']} کانفیگ اضافه شد به {context.user_data['service_id']}\n/lookup_configs برای دریافت اطلاعات کانفیگ ها")
                return ConversationHandler.END
            try:
                temp = data['configs']['ok'][context.user_data['service_id']]
            except:
                data['configs']['ok'][context.user_data['service_id']] = {}
            data['configs']['ok'][context.user_data['service_id']][str(update.message.message_id)] = 0
            context.user_data['got'] += 1
            write_to_db()
            return GET_CONFIGS
        else:
            try:
                context.user_data['x'] = int(update.message.text.split()[0])
                context.user_data['service_id'] = update.message.text.split()[1]
                context.user_data['got'] = 0
                context.bot.send_message(chat_id=user_id, text="👍 گرفتم\nتعدادی که مشخص کردی رو برام بفرست. وقتی که تموم شدی کلمه‌ی end رو برام ارسال کن. تعداد اشتباه نفرستی یه وقت! \nبرای لغو /cancel را ارسال کنید..")
            except:
                context.bot.send_message(chat_id=user_id, text="🟥 خطا: تعداد و آیدی را مجددا ارسال کنید:")
                return GET_CONFIGS
            
def admin_send_test(update, context):
    user_id = update.effective_user.id
    context.user_data['x'] = 0
    context.user_data['got'] = 0

    if (user_id != ADMIN_CHAT_ID):
        context.bot.send_message(chat_id=user_id, text="🟥 خطا: شما به این بخش دسترسی ندارید.")
        return ConversationHandler.END
    else:
        context.bot.send_message(chat_id=user_id, text="👍 اوکی! \nکانفیگ تستت رو برام ارسال کن. \nبرای لغو /cancel را ارسال کنید.")
        return GET_TEST
def get_test(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    data['configs']['test'] = update.message.message_id
    write_to_db()
    context.bot.send_message(chat_id=user_id, text="✅ انجام شد\nاین کانفیگ از اکنون به عنوان کانفیگ تست تعیین شد.", reply_to_message_id=update.message.message_id)
    return ConversationHandler.END

def config_lookup(update, context):
    user_id = update.effective_user.id
    if user_id != ADMIN_CHAT_ID:
        context.bot.send_message(chat_id=user_id, text="🟥 خطا: شما به این بخش دسترسی ندارید.")
        return None
    else:
        test_config = data['configs']['test']
        context.bot.send_message(chat_id=user_id, text="این یکی که کانفیگ تست شماست:", reply_to_message_id=test_config)
        s = ""
        for i in data['configs']['ok']:
            s += '\nبرای آیدی ' + str(i) + ': '
            cnt = 0
            for j in data['configs']['ok'][i]:
                cnt += 1
            s += str(cnt) + ' کانفیگ موجود است'

        context.bot.send_message(chat_id=user_id, text=f"بقیه کانفیگاتم اینا هستن:\n {s}")

def del_conf(update, context):
    user_id = update.effective_user.id
    if (user_id != ADMIN_CHAT_ID):
        context.bot.send_message(chat_id=user_id, text="🟥 خطا: شما به این بخش دسترسی ندارید.")
    else:
        try:
            idd = update.message.text.split()[1]
            data['configs']['ok'][str(idd)] = {}
            write_to_db()
            context.bot.send_message(chat_id=user_id, text=f"همه‌ی کانفیگ‌های آیدی {idd} حذف شدند ✅")
        except:
            context.bot.send_message(chat_id=user_id, text="🟥 خطا: مشکلی وجود داشت.")

def reply_msg(update, context):
    user_id = update.effective_user.id
    if (user_id != ADMIN_CHAT_ID):
        context.bot.send_message(chat_id=user_id, text="🟥 خطا: شما به این بخش دسترسی ندارید.")
        return None
    else:
        msg = update.message.text.split()
        try:
            context.bot.send_message(chat_id=user_id, text="این پیامیه که گفتی ریپلای کنم.", reply_to_message_id=msg[1])
        except:
            context.bot.send_message(chat_id=user_id, text="💔 چنین پیامی وجود نداره!", reply_to_message_id=update.message.message_id)

def check_commission(user_id, context):
    has_inviter = 0 if data['users'][str(user_id)]['is_invited'] == 0 else 1
    inviter_got_commission = 0 if data['users'][str(user_id)]['inviter_got_commission'] == 0 else 1
    inviter = data['users'][str(user_id)]['inviter_id']
    commission_rate = data['packages']['commission_rate']['price']


    if has_inviter and (not inviter_got_commission):

        context.bot.send_message(chat_id=int(inviter), text=f"🤑 تبریک! یکی از زیر مجموعه های شما اولین خریدش رو کرد و مبلغ {commission_rate} به کیف پول شما واریز شد!")
        try:
            data['users'][str(inviter)]['credit'] += commission_rate
            data['users'][str(user_id)]['inviter_got_commission'] = 1
            write_to_db()
            context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"کمیسیون به کاربر {inviter} به علت خرید یکی از زیر مجموعه هایش تعلق گرفت.")
        except:
            context.bot.send_message(chat_id=user_id, text="خطای ارسال پول به معرف")
    

def admin_set_description(update, context):
    user_id = update.effective_user.id
    if (user_id != ADMIN_CHAT_ID):
        context.bot.send_message(chat_id=user_id, text="شما به این بخش دسترسی ندارید.")
        return ConversationHandler.END
    else:
        context.user_data['package_id'] = update.message.text.split()[1]
        context.bot.send_message(chat_id=user_id, text=f"حله. شما دارید برای {context.user_data['package_id']} توضیحات ست میکنید. پیامی که بفرستید به عنوان توضیح برای کاربران ارسال خواهد شد. \n برای لغو /cancel")
        return GET_DESCRIPTION
def admin_get_description(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    try:
        data['packages'][str(context.user_data['package_id'])]['desc'] = update.message.message_id
        context.bot.send_message(chat_id=user_id, text="توضیح ست شد.")
        write_to_db()
    except:
        context.bot.send_message(chat_id=user_id, text="خطایی رخ داده است.")
    return ConversationHandler.END

def set_cards(update, context):
    user_id = update.effective_user.id
    if (user_id != ADMIN_CHAT_ID):
        context.bot.send_message(chat_id=user_id, text="No! You cant do this to me. stop or I will ban you.")
        return ConversationHandler.END
    else:
        num = update.message.text.split()[1]
        context.user_data['x'] = int(num)
        context.bot.send_message(chat_id=user_id, text=f"حله! {num} تا پیام برام بفرست که توی هر کدومش شماره کارت و توضیحات مربوطه‌ش اومده. در آخر end رو بفرست.\n /cancel")
        return GET_CARDS
def get_cards(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    if (user_id != ADMIN_CHAT_ID):
        context.bot.send_message(chat_id=user_id, text="Stop.")
        return ConversationHandler.END
    else:
        if context.user_data['x'] != 0:
            try:
                data['messages'].append(update.message.message_id)
                write_to_db()
                context.user_data['x'] -= 1
                return GET_CARDS
            except:
                context.bot.send_message(chat_id=user_id, text="Error. Operation Ended. try again.")
                return ConversationHandler.END
        else:
            context.bot.send_message(chat_id=user_id, text="انجام شد.")
            return ConversationHandler.END

def delete_cards(update, context):
    user_id = update.effective_user.id
    if user_id != ADMIN_CHAT_ID:
        context.bot.send_message(chat_id=ADMIN_CHAT_ID, text="Error. You cant do this.")
    else:
        try:
            data['messages']['cards'] = []
            write_to_db()
            context.bot.send_message(chat_id=user_id, text="همه‌ی کارت ها با موفقیت حذف شدند.")
        except:
            context.bot.send_message(chat_id=user_id, text="یک خطا رخ داد. مجدد تلاش کنید.")

def db_backup(update, context):
    user_id = update.effective_user.id
    if user_id != ADMIN_CHAT_ID:
        context.bot.send_message(chat_id=user_id, text="You cant do this. stop.")
    else:
        context.bot.send_message(chat_id=user_id, text=f"database backup in:\n{datetime.date}\n{datetime.time}:")
        with open('data.json', 'rb') as f:
            context.bot.send_document(chat_id=user_id, document=f)

def add_unlimited_test(update, context):
    user_id = update.effective_user.id
    if user_id != ADMIN_CHAT_ID:
        context.bot.send_message(chat_id=user_id, text="Error. you cant do this operation.")
        return ConversationHandler.END
    else:
        try:
            idd = int(update.message.text.split()[1])
            data['exceptions'].append(idd)
            write_to_db()
            context.bot.send_message(chat_id=user_id, text=f"کاربر با آیدی زیر با موفقیت به لیست معافیت از یک هفته اضافه شد:{idd}")
        except:
            context.bot.send_message(chat_id=user_id, text="خطایی رخ داده است. مجدد امتحان کنید.")
def remove_from_exception(update, context):
    user_id = update.effective_user.id
    if user_id != ADMIN_CHAT_ID:
        context.bot.send_message(chat_id=user_id, text="You can not do this.")
    else:
        idd = int(update.message.text.split()[1])
        try:
            for item in data['exceptions']:
                if item == idd:
                    data['exceptions'].remove(item)
                    write_to_db()
                    context.bot.send_message(chat_id=user_id, text=f"کاربر با آیدی زیر با موفقیت از لیست معافیت یک هفته ای حذف شد.{idd}")
        except:
            context.bot.send_message(chat_id=user_id, text="خطایی رخ داده است. مجدد امتحان کنید.")
######## END ADMIN ZONE ##########
















######### CLIENT ZONE ###########

def commission(update, context): # *** should be updated
    user_id = update.effective_user.id
    commission_rate = data['packages']['commission_rate']['price']
    context.bot.send_message(chat_id=user_id, text=f'🤝با دعوت دوستانتان به بات، پس از اولین خرید آنها شما {commission_rate} تومان دریافت خواهید کرد! کد شما: \n{user_id}\n از آنها بخواهید پیش از انجام اولین خرید از طریق همین منو معرفشان را تنظیم کنند. \nبرای وارد کردن کد معرف /set_my_inviter را بزنید.')
def set_my_inviter(update, context): # *** should be updated
    user_id = update.effective_user.id
    context.bot.send_message(chat_id=user_id, text="حله! 👍\n کد معرفت رو برام بفرست \n برای لغو /cancel را ارسال کنید.")
    return SET_INVITER
def set_inviter(update, context):
    user_id = update.effective_user.id
    msg = update.message.text
    inviter_exists = 0
    for i in data['users']:
        if i == msg:
            inviter_exists = 1
            break
    if (str(user_id) == msg):
        context.bot.send_message(chat_id=user_id, text="😄 شما نمیتونید معرف خودتون باشید")
        return ConversationHandler.END
    if not inviter_exists:
        context.bot.send_message(chat_id=user_id, text="☹️ متاسفانه چنین کاربری یافت نشد.")
        return ConversationHandler.END
    try:
        data['users'][str(user_id)]['is_invited'] = 1
        data['users'][str(user_id)]['inviter_id'] = msg
        write_to_db()
        context.bot.send_message(chat_id=user_id, text=f"گرفتم! معرف شما {msg} است. پس از اولین خرید شما هزینه کمیسیون به حساب ایشان واریز خواهد شد.")
    except:
        context.bot.send_message(chat_id=user_id, text="🟥 خطا: عملیات انجام نشد.")
    return ConversationHandler.END



def packages(update, context):
    user_id = update.effective_user.id

    button1 = InlineKeyboardButton("*", callback_data=f"none")
    button2 = InlineKeyboardButton("نام پکیج", callback_data="none")
    button3 = InlineKeyboardButton("قیمت 💰", callback_data="none")
    keyboard = [[button1, button2, button3]]

    for i in data['packages']:
        if (i == 'commission_rate' or i == 'commission'):
            continue
        button1 = InlineKeyboardButton("🛒 خرید", callback_data=f"buy_{i}")
        button2 = InlineKeyboardButton(str(data['packages'][str(i)]['name']), callback_data="none")
        button3 = InlineKeyboardButton(str(data['packages'][str(i)]['price']), callback_data="none")

        keyboard.append([button1, button2, button3])

    inline_keyboard = InlineKeyboardMarkup(keyboard)

    msg = data['messages']['packages']
    context.bot.send_message(chat_id=user_id, text=msg, reply_markup=inline_keyboard)


# Define the function to handle the /credit command
def credit(update, context):
    user_id = update.effective_user.id
    user_credit = int(data['users'][str(user_id)]['credit'])
    context.bot.send_message(chat_id=user_id, text=f'💰 شما {user_credit} تومان در کیف پول خود دارید.\nبرای افزایش موجودی /credit_charge را بزنید.')

def credit_charge(update, context):
    user_id = update.effective_user.id
    msg_id = random.choice(data['messages']['cards'])
    card_number = data['messages']['card_number']
    card_owner = data['messages']['card_owner']
    context.bot.copy_message(chat_id=user_id, from_chat_id=ADMIN_CHAT_ID, message_id=msg_id)

    # context.bot.send_message(chat_id=user_id, text=f"""
    # حله 👍 لطفا موارد پایین رو به دقت بخون 🙏
    # 💳 برای افزایش موجودی:
    # ۱. مبلغ مورد نظرتون رو به شماره کارت {card_number} به نام {card_owner} واریز کنید.
    # ۲. رسید واریزی رو اینجا بفرستید
    # ۳. پس از تایید ادمین، اعتبار کیف پول شما شارژ میشه.

    # لازم نیست نگران باشید، هر مقداری که واریز کنید همون مقدار به کیف پولتون اضافه میشه پس با خیال راحت شارژ رو انجام بدید. 😊

    # ❗️ لطفا هیچ پیامی به جز رسید نفرستین 🙏

    # برای لغو عملیات /cancel را بزنید.
    # """)

    return FIRST1
def send_resid(update, context):
    user_id = update.effective_user.id

    # test
    button1 = InlineKeyboardButton("💵 ویرایش اعتبار", callback_data=f"set_credit{user_id}")
    button2 = InlineKeyboardButton("💬 ارسال پیام", callback_data=f"msg{user_id}")
    button3 = InlineKeyboardButton("ℹ️ اطلاعات کاربر", callback_data=f'info{user_id}')
    keyboard = [[button1, button2], [button3]]
    inline_keyboard = InlineKeyboardMarkup(keyboard)
    # End test

    context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f'🔽💸 پرداختی جدید از کاربر {user_id}:')
    context.bot.forward_message(chat_id=ADMIN_CHAT_ID, from_chat_id=user_id, message_id=update.message.message_id)
    context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f'چه کنم؟', reply_markup=inline_keyboard)
    context.bot.send_message(chat_id=user_id, text='✅ درخواست افزایش موجودی شما ارسال شد. بلافاصله پس از تایید ادمین حساب کاربری شما شارژ خواهد شد. لطفا در صورتی که پس از 24 ساعت اکانت شما شارژ نشد پشتیبانی را مطلع بفرمایید 🙏')
    return ConversationHandler.END

def support(update, context):
    user_id = update.effective_user.id
    if data['users'][str(user_id)]['is_blocked'] == 1:
        context.bot.send_message(chat_id=user_id, text="🟥 خطا: شما به این بخش دسترسی ندارید.")
        return ConversationHandler.END
    context.bot.send_message(chat_id=user_id, text='💬 شما در حال ارسال پیام به پشتیبانی هستید.\nلطفا از ارسال هرگونه پیام غیر مرتبط خودداری بفرمایید 🙏\nبرای لغو عملیات /cancel را ارسال کنید.')
    return FIRST

# Define the function to handle the payment confirmation message
def payment_confirmation(update, context):
    user_id = update.effective_user.id
    confirmation_code = update.message.text
    # Verify the payment confirmation code and update the user data
    if confirmation_code == '1234': # Replace with payment confirmation logic
        data[str(user_id)]['credit_verified'] = True
        with open('data.json', 'w') as f:
            json.dump(data, f)
        context.bot.send_message(chat_id=user_id, text='Your payment has been verified.')
    else:
        context.bot.send_message(chat_id=user_id, text='Invalid payment confirmation code.')

# Define the function to handle the /tutorial command
def tutorial(update, context):
    user_id = update.effective_user.id
    # Send the tutorial video to the user
    tutorials_link = data['messages']['tutorials_link']
    context.bot.send_message(chat_id=user_id, text=f'👨‍🏫 شما میتوانید آموزش اتصال را از لینک زیر ببینید:\n{tutorials_link}')

# user account info
def account(update, context):
    user_id = update.effective_user.id
    credit = data['users'][str(user_id)]['credit']
    context.bot.send_message(chat_id=user_id, text=f"""ℹ️ اطلاعات اکانت شما به شرح زیر میباشد:
    ID: {user_id}
    اعتبار کیف پول: {credit}

    سرویس های شما:

    {str(data['users'][str(user_id)]['services'])}
    """)

# test vpn
def test_vpn(update, context):
    user_id = update.effective_user.id
    timestamp = float(data['users'][str(user_id)]['last_test'])
    dt = datetime.datetime.fromtimestamp(timestamp)
    now = datetime.datetime.now()
    duration = now - dt
    if duration.total_seconds() >= 500000:
        data['users'][str(user_id)]['last_test'] = str(now.timestamp())
        send_test_to_user(user_id, context)
        write_to_db()
    else:
        context.bot.send_message(chat_id=user_id, text="شما در هفته فقط مجاز به دریافت یک تست هستید. هنوز یک هفته نگذشته!")
def send_test_to_user(user_id, context):
    try:
        msg_id = data['configs']['test']
        context.bot.copy_message(chat_id=user_id, from_chat_id=ADMIN_CHAT_ID, message_id=msg_id)
    except:
        context.bot.send_message(chat_id=user_id, text="خطایی رخ داده است. لطفا مجددا تلاش کنید یا به پشتیبانی اطلاع دهید.")

# Send messages to admin:
def message_handler(update, context):
    user_id = update.effective_user.id
    if update.message.text == '/cancel': # if the user wants to cancel operation
        context.bot.send_message(chat_id=user_id, text="❕ عملیات با موفقیت کنسل شد.")
        return ConversationHandler.END

    if data['users'][str(user_id)]['is_blocked'] == 1:
        context.bot.send_message(chat_id=user_id, text="🟥 خطا: شما به این بخش دسترسی ندارید.")
        return ConversationHandler.END

    # test
    button1 = InlineKeyboardButton("User Credit", callback_data=f"set_credit{user_id}")
    button2 = InlineKeyboardButton("Reply to user", callback_data=f"msg{user_id}")
    button3 = InlineKeyboardButton("User Info", callback_data=f'info{user_id}')
    keyboard = [[button1, button2], [button3]]
    inline_keyboard = InlineKeyboardMarkup(keyboard)
    # End test

    # Send any other messages to the support admin
    context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f'📩 یک تیکت پشتیبانی جدید از کاربر {user_id}:\n')
    context.bot.forward_message(chat_id=ADMIN_CHAT_ID, from_chat_id=update.message.chat_id, message_id=update.message.message_id)
    context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f'گزینه‌های مدیریتی کاربر: {user_id}', reply_markup=inline_keyboard)
    context.bot.send_message(chat_id=user_id, text="✅ پیام شما به پشتیبانی ارسال شد.\nلطفا از ارسال پیام های اضافه در همین باره خودداری بفرمایید، پشتیبانی در اسرع وقت به پیام شما پاسخ خواهد داد. از شکیبایی شما متشکریم 🙏")
    return ConversationHandler.END

def cancel(update, context):
    user_id = update.effective_user.id
    context.bot.send_message(chat_id=user_id, text="❕ عملیات با موفقیت لغو شد.")
    return ConversationHandler.END

def help_info(update, context):
    user_id = update.effective_user.id
    context.bot.send_message(chat_id=user_id, text=f"""
        به بات V2Nap خوش اومدید! 😊
        میتونید از کامند های پایین استفاده کنید:

        /start start or restart bot
        /support send message to support
        /credit charge your account
        /test_vpn to test server (one in a week)
        /tutorial how to connect
        /packages list of packages
        /commission Your commisions list (10k Toomans for every new user!)
        /account Get to know your account information


        توجه: آیدی شما {user_id} است. ممکن است در آینده به آن نیاز داشته باشید!
        """)

def config_available(service_id):
    for i in data['configs']['ok'][str(service_id)]:
        if (data['configs']['ok'][str(service_id)][i] == 0):
            return True
    return False


def buy(update, context):
    user_id = update.effective_user.id
    query = update.callback_query
    query.answer()
    button_pressed = query.data
    bp = button_pressed

    ordered_plan = button_pressed[4:]
    user_credit = int(data['users'][str(user_id)]['credit'])
    name = data['packages'][ordered_plan]['name']
    price = int(data['packages'][ordered_plan]['price'])

    context.user_data['user_credit'] = user_credit
    context.user_data['name'] = name
    context.user_data['price'] = price
    context.user_data['ordered_plan'] = ordered_plan

    
    try:
        msg_description = data['packages'][str(ordered_plan)]['desc']
        context.bot.copy_message(chat_id=user_id, from_chat_id=ADMIN_CHAT_ID, message_id=msg_description)
    except:
        context.bot.send_message(chat_id=user_id, text="توضیحی برای این پکیج وجود ندارد.")

    context.bot.send_message(chat_id=user_id, text=f"❕ شما در حال خرید {name} با هزینه‌ی {price} هستید. (آیدی این پکیج: {ordered_plan}). حتما ابتدا توضیحات بالا را بخوانید و سپس اقدام به تایید فرایند خرید کنید.\nاعتبار کیف پول شما {user_credit} تومان است. برای ادامه 1 لاتین را ارسال کنید. \n برای لغو /cancel را ارسال کنید.")
    return CONFIRM_BUY
def do_buy(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    msg = update.message.text

    user_credit = int(context.user_data['user_credit'])
    price = int(context.user_data['price'])
    name = context.user_data['name']
    ordered_plan = context.user_data['ordered_plan']


    if (msg == '1'):
        try:
            user_credit_is_ok = False if (price > user_credit) else True
            if user_credit_is_ok:
                if not (config_available(ordered_plan)):
                    context.bot.send_message(chat_id=user_id, text="متاسفانه در حال حاضر این سرویس موجود نیست ☹️ \n اما نگران نباشید، تا دقایقی دیگه موجود میشه 😇")
                    context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"⭕یکی از کاربران قصد خرید سرویس ({ordered_plan})  {name} رو داشت که متاسفانه موجود نبود.")
                    return ConversationHandler.END
                context.bot.send_message(chat_id=user_id, text="✅ اعتبار حساب کاربری شما کافی است. خرید انجام شد")
                try:
                    check_commission(str(user_id), context)
                except:
                    pass
                product_id = 0
                for i in data['configs']['ok'][str(ordered_plan)]:
                    try:
                        product_id = i
                        try:
                            data['configs']['sold'][str(ordered_plan)][str(i)] = user_id
                            data['configs']['ok'][str(ordered_plan)].pop(str(i))
                        except:
                            data['configs']['sold'][str(ordered_plan)] = {}
                            data['configs']['sold'][str(ordered_plan)][str(i)] = user_id
                            data['configs']['ok'][str(ordered_plan)].pop(str(i))
                        try: 
                            context.bot.copy_message(chat_id=user_id, from_chat_id=ADMIN_CHAT_ID, message_id=product_id)
                            data['users'][str(user_id)]['services'][str(product_id)] = context.user_data['name']
                        except:
                            context.bot.send_message(chat_id=user_id, text="❌ خطایی از سمت ادمین رخ داده است. لطفا از ادمین بخواهید به صورت دستی کانفیگ تان را برایتان ارسال کند.")
                            context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"❌ در حین عملیات خرید توسط کاربر {user_id} خطایی رخ داده است: کانفیگ از سمت شما پاک شده است. لطفا یک عدد کانفیگ {context.user_data['name']} با آیدی {ordered_plan} برای ایشان ارسال کنید.")
                        write_to_db()
                        break
                    except:
                        context.bot.send_message(chat_id=user_id, text="⭕ خطایی ناشناس رخ داده است. لطفا در صورت کسری موجودی با پشتیبانی در ارتباط باشید")
                        context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"⭕ حین عملیات خرید برای کاربر {user_id} خطایی رخ داده است.")
                # data['users'][str(user_id)]['services'][str(product_id)] = 1
                data['users'][str(user_id)]['credit'] -= price
                write_to_db()
                user_credit = data['users'][str(user_id)]['credit']
                context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"🛒 خرید جدید: کاربر {user_id} سرویس {name} ({ordered_plan}) را با قیمت {price} خریداری کرد.\n آیدی سرویس: {product_id}\n هزینه از کیف پول ایشان کم شد. موجودی جدید: {user_credit}", reply_to_message_id=product_id)
                # send the config ***
                context.bot.send_message(chat_id=user_id, text="برای دریافت آموزش اتصال /tutorial را بزنید.")
                context.bot.send_message(chat_id=user_id, text=f"💲 اعتبار جدید کیف پول شما: {user_credit}")
            else:
                context.bot.send_message(chat_id=user_id, text="❌ اعتبار حساب شما کافی نیست. برای افزایش موجودی /credit را بزنید.")
        except:
            context.bot.send_message(chat_id=user_id, text="⭕ خطایی ناشناس رخ داده است. لطفا در صورت کسری موجودی با پشتیبانی در ارتباط باشید")
            context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"⭕ حین عملیات خرید برای کاربر {user_id} خطایی رخ داده است.")

    else:
        context.bot.send_message(chat_id=user_id, text='برای ادامه 1 لاتین را ارسال کنید.\nبرای لغو /cancel را ارسال کنید.')
        return CONFIRM_BUY
    return ConversationHandler.END










################## BUTTONS ########################
# button handler
def button_click_callback(update, context):
    query = update.callback_query
    query.answer()
    button_pressed = query.data
    bp = button_pressed
    if button_pressed[0:3] == 'msg':
        context.user_data['id'] = button_pressed[3:]
        idd = context.user_data['id']
        context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f'شما در حال ارسال پیام به {idd} هستید:\n( برای لغو /cancel را ارسال کنید..)')
        return FIRST2
    elif button_pressed[0:4] == 'info':
        idd = bp[4:]
        user_id = ADMIN_CHAT_ID
        user_credit = data['users'][idd]['credit']
        try:
            button1 = InlineKeyboardButton("💵 ویرایش اعتبار", callback_data=f"set_credit{idd}")
            button2 = InlineKeyboardButton("💬 ارسال پیام", callback_data=f"msg{idd}")
            keyboard = [[button1, button2]]
            inline_keyboard = InlineKeyboardMarkup(keyboard)
            s = f"""
            ❕ اطلاعات کاربر مدنظر به شرح زیر است.

            ID: {idd}
            اعتبار کیف پول: {user_credit}

            سرویس‌های خریداری شده:

            """

            # {(i + '\n') for i in data['users'][idd][services]}

            for i in data['users'][idd]['services']:
                s += i + ' : ' + data['users'][idd]['services'][i] + '\n'

            context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=s, reply_markup=inline_keyboard)
        except:
            pass

    elif button_pressed[0:4] == 'del_':
        user_id = update.effective_user.id
        if (user_id != ADMIN_CHAT_ID):
            context.bot.send_message("Error")
            return False
        data['packages'].pop(button_pressed[4:])
        write_to_db()
        context.bot.send_message(chat_id=user_id, text="✅ پکیج مدنظر با موفقیت حذف شد")

    elif button_pressed[0:10] == 'set_credit':
        user_id = ADMIN_CHAT_ID
        try:
            context.user_data['chat_id'] = int(button_pressed[10:])
            user_credit = data['users'][str(context.user_data['chat_id'])]['credit']
            context.bot.send_message(chat_id=user_id, text=f"""❕ شما در حال تعیین موجودی برای کاربر {context.user_data['chat_id']} هستید.
            💰 موجودی فعلی کاربر: {user_credit}
            بهم بگو موجودی چقدر باید باشه؟\n برای لغو /cancel را ارسال کنید.
            """)
            return CREDIT
        except:
            context.bot.send_message(chat_id=user_id, text='🟥 خطا: فرمت پیام نادرست است.')
            return ConversationHandler.END

def button_client_callback(update, context): # client{user_id}+
    query = update.callback_query
    query.answer()
    button_pressed = query.data
    bp = button_pressed
    if button_pressed[len(bp)-6:] == 'credit':
        pass
    elif button_pressed[len(bp)-7] == 'support':
        pass
    elif button_pressed[len(bp)-7] == 'account':
        pass













#################################### /*
# conversations:
support_conv_handler = ConversationHandler (
    entry_points=[CommandHandler('support', support), CallbackQueryHandler(support, pattern="^support$")],
    states={
        FIRST: [MessageHandler(Filters.text & ~Filters.command, message_handler)],
        SECOND: [MessageHandler(Filters.text & ~Filters.command, message_handler)]
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)

credit_conv_handler = ConversationHandler (
    entry_points=[CommandHandler('credit_charge', credit_charge)],
    states={
        FIRST1: [MessageHandler(~Filters.command, send_resid)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)

set_credit_conv_handler = ConversationHandler (
    entry_points=[CommandHandler('set_credit', set_credit), CallbackQueryHandler(button_click_callback, pattern="^set_credit")],
    states={
        CREDIT: [MessageHandler(~Filters.command, credit_change)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)

admin_support_conv_handler = ConversationHandler (
    entry_points=[CommandHandler('admin_message', admin_message), CallbackQueryHandler(button_click_callback, pattern="^msg")],
    states={
        ADMIN_SEND_MESSAGE: [admin_message],
        FIRST2: [MessageHandler(~Filters.command, send_admin_message)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)

brodcast_conv_handler = ConversationHandler (
    entry_points=[CommandHandler('brodcast', brodcast), CallbackQueryHandler(brodcast, pattern="^brodcast$")],
    states={
        SEND_BROD: [MessageHandler(~Filters.command, send_brodcast)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)

set_packages_conv_handler = ConversationHandler (
    entry_points=[CommandHandler('admin_edit_packages', admin_edit_packages)],
    states={
        SET_PACK: [MessageHandler(~Filters.command, admin_set_packages)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)

admin_edit_messages_conv_handler = ConversationHandler (
    entry_points=[CommandHandler('admin_edit_messages', admin_edit_messages)],
    states={
        EDIT_MESSAGE: [MessageHandler(~Filters.command, admin_set_messages)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)

buy_conv_handler = ConversationHandler (
    entry_points=[CallbackQueryHandler(buy, pattern="^buy_")],
    states={
        CONFIRM_BUY: [MessageHandler(~Filters.command, do_buy)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)

config_send_conv_handler = ConversationHandler (
    entry_points=[CallbackQueryHandler(send_config, pattern="^admin_send_config$"), CommandHandler('admin_send_config', send_config)],
    states={
        GET_CONFIGS: [MessageHandler(~Filters.command, get_configs)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)

test_config_conv_handler = ConversationHandler (
    entry_points=[CallbackQueryHandler(admin_send_test, pattern="^admin_send_test$"), CommandHandler('admin_send_test', admin_send_test)],
    states={
        GET_TEST: [MessageHandler(~Filters.command, get_test)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)

set_inviter_conv_handler = ConversationHandler (
    entry_points=[CommandHandler('set_my_inviter', set_my_inviter)],
    states={
        SET_INVITER: [MessageHandler(~Filters.command, set_inviter)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)
set_package_des_conv_handler = ConversationHandler (
    entry_points=[CommandHandler('set_description', admin_set_description)],
    states={
        GET_DESCRIPTION: [MessageHandler(~Filters.command, admin_get_description)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)

set_cards_conv_handler = ConversationHandler (
    entry_points=[CommandHandler('set_cards', set_cards)],
    states={
        GET_CARDS: [MessageHandler(~Filters.command, get_cards)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)

################################## */











# Define the main function to start the bot
def main():

    # Add the command handlers to the bot
    updater.dispatcher.add_handler(CommandHandler('start', start))

    updater.dispatcher.add_handler(CommandHandler('credit', credit))
    updater.dispatcher.add_handler(CallbackQueryHandler(credit, pattern="^credit$"))

    updater.dispatcher.add_handler(CommandHandler('tutorial', tutorial))
    updater.dispatcher.add_handler(CallbackQueryHandler(tutorial, pattern='^tutorial$'))

    updater.dispatcher.add_handler(CommandHandler('account', account))
    updater.dispatcher.add_handler(CallbackQueryHandler(account, pattern='^account$'))

    updater.dispatcher.add_handler(CommandHandler('packages', packages))
    updater.dispatcher.add_handler(CallbackQueryHandler(packages, pattern='^packages$'))

    updater.dispatcher.add_handler(CommandHandler('commission', commission))
    updater.dispatcher.add_handler(CallbackQueryHandler(commission, pattern='^commission$'))

    updater.dispatcher.add_handler(CommandHandler('admin_users_list', admin_users_list))
    updater.dispatcher.add_handler(CallbackQueryHandler(admin_users_list, pattern='^admin_users_list$'))

    updater.dispatcher.add_handler(CommandHandler('test_vpn', test_vpn))
    updater.dispatcher.add_handler(CallbackQueryHandler(test_vpn, pattern='^test_vpn$'))

    updater.dispatcher.add_handler(CommandHandler('admin_user_info', admin_user_info))
    updater.dispatcher.add_handler(CallbackQueryHandler(button_click_callback, pattern="^info"))

    updater.dispatcher.add_handler(CommandHandler('help', help_info))
    updater.dispatcher.add_handler(CallbackQueryHandler(help_info, pattern="^help$"))

    updater.dispatcher.add_handler(CommandHandler('admin_help', admin_help))
    updater.dispatcher.add_handler(CallbackQueryHandler(admin_help, pattern="^admin_help$"))

    updater.dispatcher.add_handler(CallbackQueryHandler(button_click_callback, pattern="^del_"))

    updater.dispatcher.add_handler(CommandHandler('block', block_user))
    updater.dispatcher.add_handler(CommandHandler('unblock', unblock_user))

    updater.dispatcher.add_handler(CommandHandler('lookup_configs', config_lookup))

    updater.dispatcher.add_handler(CommandHandler('del_conf', del_conf))
    
    updater.dispatcher.add_handler(CommandHandler('reply', reply_msg))
    
    updater.dispatcher.add_handler(CommandHandler('db_backup', db_backup))

    updater.dispatcher.add_handler(CommandHandler('del_cards', delete_cards))

    updater.dispatcher.add_handler(CommandHandler('add_unlimited_test', add_unlimited_test))
    updater.dispatcher.add_handler(CommandHandler('remove_from_exception', remove_from_exception))

    updater.dispatcher.add_handler(CallbackQueryHandler(start, pattern='^start$'))








    # Buttons:

    # updater.dispatcher.add_handler(CallbackQueryHandler(button_click_callback))

    # End Buttons

    updater.dispatcher.add_handler(support_conv_handler)
    updater.dispatcher.add_handler(credit_conv_handler)
    updater.dispatcher.add_handler(set_credit_conv_handler)
    updater.dispatcher.add_handler(admin_support_conv_handler)
    updater.dispatcher.add_handler(brodcast_conv_handler)
    updater.dispatcher.add_handler(set_packages_conv_handler)
    updater.dispatcher.add_handler(admin_edit_messages_conv_handler)
    updater.dispatcher.add_handler(buy_conv_handler)
    updater.dispatcher.add_handler(config_send_conv_handler)
    updater.dispatcher.add_handler(test_config_conv_handler)
    updater.dispatcher.add_handler(set_inviter_conv_handler)
    updater.dispatcher.add_handler(set_package_des_conv_handler)
    updater.dispatcher.add_handler(set_cards_conv_handler)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
