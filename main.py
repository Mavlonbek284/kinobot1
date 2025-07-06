import telebot

# === Bot token ===
BOT_TOKEN = '8186601135:AAGyDlVVW878v1QtLOLfVxn7oXhV6SFMG2A'
bot = telebot.TeleBot(BOT_TOKEN)

# === Kanal usernamelari ===
KANALLAR = ['@Daqiqauzb24', '@TarjimaKinoPlusbot']

# === Kinolar bazasi ===
KINOLAR = {
    "1": {
        "file_id": "VIDEO_FILE_ID_1",  # bu yerga haqiqiy file_id kiriting
        "nomi": "Ultrabinavsha",
        "yili": "2006"
    },
    "9": {
        "file_id": "VIDEO_FILE_ID_2",
        "nomi": "Batman",
        "yili": "2023"
    }
}

# === Obuna tekshiruvchi funksiya ===
def obuna_tekshir(user_id):
    for kanal in KANALLAR:
        try:
            member = bot.get_chat_member(kanal, user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                return False
        except:
            return False
    return True

# === /start komandasi ===
@bot.message_handler(commands=['start'])
def boshlash(message):
    bot.send_message(message.chat.id, "🎬 Kino kodini kiriting (masalan: 1, 9):")

# === Kod yuborilganda ishlovchi funksiya ===
@bot.message_handler(func=lambda m: m.text.isdigit())
def kino_ber(message):
    user_id = message.from_user.id
    kod = message.text.strip()

    if not obuna_tekshir(user_id):
        markup = telebot.types.InlineKeyboardMarkup()
        for kanal in KANALLAR:
            markup.add(telebot.types.InlineKeyboardButton("➕ Obuna bo‘lish", url=f"https://t.me/{kanal.strip('@')}"))
        markup.add(telebot.types.InlineKeyboardButton("✅ Tekshirish", callback_data='check_sub'))
        bot.send_message(message.chat.id, "📛 Iltimos, quyidagi kanallarga obuna bo‘ling:", reply_markup=markup)
        return

    if kod in KINOLAR:
        kino = KINOLAR[kod]
        bot.send_video(message.chat.id, kino["file_id"], caption=f"🎬 {kino['nomi']}\n📅 {kino['yili']}")
    else:
        bot.send_message(message.chat.id, "❌ Bunday koddagi kino topilmadi.")

# === Obunani qayta tekshiruvchi tugma ===
@bot.callback_query_handler(func=lambda call: call.data == 'check_sub')
def tekshir_callback(call):
    user_id = call.from_user.id
    if obuna_tekshir(user_id):
        bot.answer_callback_query(call.id, "✅ Obuna tasdiqlandi.")
        bot.send_message(call.message.chat.id, "✅ Endi kino kodini kiriting:")
    else:
        bot.answer_callback_query(call.id, "❌ Hali obuna bo‘lmagansiz.")

# === Kinoga video yuborganda file_id ni chiqarish uchun ===
@bot.message_handler(content_types=['video'])
def video_qabul(message):
    bot.send_message(message.chat.id, f"📽 file_id: `{message.video.file_id}`", parse_mode="Markdown")

bot.polling()