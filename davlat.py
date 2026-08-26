import json
import os
import re
import asyncio

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# =========================================================
# 🔐 BOT TOKEN
# =========================================================

TOKEN = "8928289217:AAHpVm6ohPoRri7PpNuHl6UbSzKfPqBXfaw"

# =========================================================
# 👑 ADMIN ID
# =========================================================

ADMIN_ID = 7125514459

# =========================================================
# 💾 FAYLLAR
# =========================================================

DATA_FILE = "countries_data.json"
STATS_FILE = "bot_stats.json"


# =========================================================
# 🌍 DAVLATLAR VA POYTAXTLAR
# =========================================================

countries = {
    "afg'oniston": "Kobul",
    "albaniya": "Tirana",
    "aljir": "Aljir",
    "andorra": "Andorra-la-Velya",
    "angola": "Luanda",
    "antigua va barbuda": "Sent-Jons",
    "argentina": "Buenos-Ayres",
    "armaniston": "Yerevan",
    "avstraliya": "Kanberra",
    "avstriya": "Vena",
    "ozarbayjon": "Boku",
    "bagama orollari": "Nassau",
    "bahrayn": "Manama",
    "bangladesh": "Dakka",
    "barbados": "Bridjtaun",
    "belarus": "Minsk",
    "belgiya": "Bryussel",
    "beliz": "Belmopan",
    "benin": "Porto-Novo",
    "butan": "Timfu",
    "boliviya": "Sucre",
    "bosniya va gersegovina": "Sarayevo",
    "botsvana": "Gaborone",
    "braziliya": "Brasiliya",
    "bruney": "Bandar-Seri-Begavan",
    "bolgariya": "Sofiya",
    "burkina-faso": "Uagadugu",
    "burundi": "Gitega",
    "kabo-verde": "Praya",
    "kambodja": "Pnompen",
    "kamerun": "Yaunde",
    "kanada": "Ottava",
    "markaziy afrika respublikasi": "Bangui",
    "chad": "Njamena",
    "chili": "Santyago",
    "xitoy": "Pekin",
    "kolumbiya": "Bogota",
    "komor orollari": "Moroni",
    "kongo": "Brazzavil",
    "kongo demokratik respublikasi": "Kinshasa",
    "kosta-rika": "San-Xose",
    "kot-d'ivuar": "Yamusukro",
    "xorvatiya": "Zagreb",
    "kuba": "Gavana",
    "kipr": "Nikosiya",
    "chexiya": "Praga",
    "daniya": "Kopengagen",
    "djibuti": "Jibuti",
    "dominika": "Rozo",
    "dominikan respublikasi": "Santo-Domingo",
    "ekvador": "Kito",
    "misr": "Qohira",
    "salvador": "San-Salvador",
    "ekvatorial gvineya": "Malabo",
    "eritriya": "Asmara",
    "estoniya": "Tallin",
    "esvatini": "Mbabane",
    "efiopiya": "Addis-Abeba",
    "fiji": "Suva",
    "finlyandiya": "Helsinki",
    "fransiya": "Parij",
    "gabon": "Librevil",
    "gambiya": "Banjul",
    "gruziya": "Tbilisi",
    "germaniya": "Berlin",
    "ghana": "Akra",
    "gretsiya": "Afina",
    "grenada": "Sent-Jorjes",
    "gvatemala": "Gvatemala",
    "gvineya": "Konakri",
    "gvineya-bisau": "Bisau",
    "gayana": "Jorjtaun",
    "gaiti": "Port-o-Prens",
    "gonduras": "Tegusigalpa",
    "vengriya": "Budapesht",
    "hindiston": "Nyu-Dehli",
    "indoneziya": "Jakarta",
    "eron": "Tehron",
    "iroq": "Bag'dod",
    "irlandiya": "Dublin",
    "isroil": "Quddus",
    "islandiya": "Reykyavik",
    "italiya": "Rim",
    "yamayka": "Kingston",
    "yaponiya": "Tokio",
    "iordaniya": "Amman",
    "qozog'iston": "Astana",
    "keniya": "Nayrobi",
    "kiribati": "Janubiy Tarava",
    "shimoliy koreya": "Pxenyan",
    "janubiy koreya": "Seul",
    "kuvayt": "Al-Kuvayt",
    "qirg'iziston": "Bishkek",
    "laos": "Vyentyan",
    "latviya": "Riga",
    "livan": "Bayrut",
    "lesoto": "Maseru",
    "liberiya": "Monroviya",
    "liviyan": "Tripoli",
    "lixtenshteyn": "Vaduts",
    "litva": "Vilnyus",
    "lyuksemburg": "Lyuksemburg",
    "madagaskar": "Antananarivu",
    "malavi": "Lilongve",
    "malayziya": "Kuala-Lumpur",
    "maldiv orollari": "Male",
    "mali": "Bamako",
    "malta": "Valletta",
    "marshall orollari": "Majuro",
    "mavritaniya": "Nuakshot",
    "mavrikiy": "Port-Lui",
    "meksika": "Mexiko",
    "mikroneziya": "Palikir",
    "moldova": "Kishinyov",
    "monako": "Monako",
    "mo'g'uliston": "Ulan-Bator",
    "chernogoriya": "Podgoritsa",
    "marokash": "Rabot",
    "mozambik": "Maputu",
    "myanma": "Neypyido",
    "namibiya": "Vindxuk",
    "nauru": "Yaren",
    "nepal": "Katmandu",
    "niderlandiya": "Amsterdam",
    "yangi zelandiya": "Vellington",
    "nikaragua": "Managua",
    "niger": "Niamey",
    "nigeriya": "Abuja",
    "shimoliy makedoniya": "Skopye",
    "norvegiya": "Oslo",
    "ummon": "Maskat",
    "pokiston": "Islomobod",
    "palau": "Ngerulmud",
    "panama": "Panama",
    "papua-yangi gvineya": "Port-Morsbi",
    "paragvay": "Asunsion",
    "peru": "Lima",
    "filippin": "Manila",
    "polsha": "Varshava",
    "portugaliya": "Lissabon",
    "qatar": "Doha",
    "ruminiya": "Buxarest",
    "rossiya": "Moskva",
    "ruanda": "Kigali",
    "sent-kits va nevis": "Baster",
    "sent-lusiya": "Kastri",
    "sent-vinsent va grenadinlar": "Kingstaun",
    "samoa": "Apia",
    "san-marino": "San-Marino",
    "san-tome va prinsipi": "San-Tome",
    "saudiya arabistoni": "Ar-Riyod",
    "senegal": "Dakar",
    "serbiya": "Belgrad",
    "sey­shel orollari": "Viktoriya",
    "syerra-leone": "Fritaun",
    "singapur": "Singapur",
    "slovakiya": "Bratislava",
    "sloveniya": "Lyublyana",
    "solomon orollari": "Xoniara",
    "somali": "Mogadisho",
    "janubiy afrika": "Pretoriya",
    "janubiy sudan": "Juba",
    "ispaniya": "Madrid",
    "sri-lanka": "Shri-Jayavardenepura-Kotte",
    "sudan": "Xartum",
    "surinam": "Paramaribo",
    "shvetsiya": "Stokgolm",
    "shveytsariya": "Bern",
    "suriya": "Damashq",
    "tojikiston": "Dushanbe",
    "tanzaniya": "Dodoma",
    "tailand": "Bangkok",
    "timor-leste": "Dili",
    "togo": "Lome",
    "tonga": "Nuku'alofa",
    "trinidad va tobago": "Port-of-Speyn",
    "tunis": "Tunis",
    "turkiya": "Anqara",
    "turkmaniston": "Ashxobod",
    "tuvalu": "Funafuti",
    "uganda": "Kampala",
    "ukraina": "Kyiv",
    "birlashgan arab amirliklari": "Abu-Dabi",
    "buyuk britaniya": "London",
    "aqsh": "Vashington",
    "amerika": "Vashington",
    "urugvay": "Montevideo",
    "o'zbekiston": "Toshkent",
    "uzbekiston": "Toshkent",
    "vanuatu": "Port-Vila",
    "vatikan": "Vatikan",
    "venesuela": "Karakas",
    "vetnam": "Xanoy",
    "yaman": "Sana",
    "zambiya": "Lusaka",
    "zimbabve": "Xarare",
}


# =========================================================
# 💾 SAQLASH
# =========================================================

def save_countries():
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(countries, file, ensure_ascii=False, indent=4)


def load_countries():
    global countries

    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            if isinstance(data, dict):
                countries.update(data)

        except Exception:
            print("⚠️ countries_data.json o'qilmadi.")


# =========================================================
# 📊 STATISTIKA
# =========================================================

stats = {
    "users": [],
    "searches": 0,
    "successful_searches": 0,
}


def save_stats():
    with open(STATS_FILE, "w", encoding="utf-8") as file:
        json.dump(stats, file, ensure_ascii=False, indent=4)


def load_stats():
    global stats

    if os.path.exists(STATS_FILE):
        try:
            with open(STATS_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            if isinstance(data, dict):
                stats.update(data)

        except Exception:
            print("⚠️ bot_stats.json o'qilmadi.")


def register_user(user_id):

    if user_id not in stats["users"]:
        stats["users"].append(user_id)

    save_stats()


# =========================================================
# 🧹 MATNNI TOZALASH
# =========================================================

def clean_text(text):

    text = text.strip().lower()

    text = text.replace("’", "'")
    text = text.replace("‘", "'")
    text = text.replace("`", "'")

    text = re.sub(r"\s+", " ", text)

    return text


# =========================================================
# 👑 ADMIN TEKSHIRISH
# =========================================================

def is_admin(update):

    return update.effective_user.id == ADMIN_ID


# =========================================================
# 🏠 ASOSIY MENYU
# =========================================================

def main_menu(admin=False):

    buttons = [
        ["🌍 Davlatlar", "🏙 Poytaxtlar"],
        ["❓ Yordam", "ℹ️ Bot haqida"],
    ]

    if admin:
        buttons.append(["👑 Admin panel"])

    return ReplyKeyboardMarkup(
        buttons,
        resize_keyboard=True
    )


# =========================================================
# 👑 ADMIN MENYU
# =========================================================

def admin_menu():

    return ReplyKeyboardMarkup(
        [
            ["➕ Davlat qo‘shish"],
            ["✏️ Davlatni o‘zgartirish"],
            ["🗑 Davlatni o‘chirish"],
            ["📋 Barcha davlatlar"],
            ["📊 Statistika"],
            ["🌍 Davlatlar soni"],
            ["🔙 Asosiy menyu"],
        ],
        resize_keyboard=True
    )


# =========================================================
# ⏳ ANIMATSIYA
# =========================================================

async def typing_animation(update):

    await update.message.chat.send_action("typing")
    await asyncio.sleep(0.5)


async def search_animation(update):

    msg = await update.message.reply_text("🔎 Qidirilmoqda...")

    await asyncio.sleep(0.5)

    await msg.edit_text("🌍 Ma'lumot tekshirilmoqda...")

    await asyncio.sleep(0.5)

    await msg.edit_text("⚡ Deyarli tayyor...")

    await asyncio.sleep(0.5)

    return msg


# =========================================================
# 🚀 START
# =========================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data.clear()

    register_user(update.effective_user.id)

    await typing_animation(update)

    admin = is_admin(update)

    text = (
        "✨ <b>DAVLAT & POYTAXT BOT</b> ✨\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "👋 Assalomu alaykum!\n\n"
        "🌍 Menga <b>davlat nomini</b> yozing — "
        "men uning poytaxtini topaman.\n\n"
        "🏙 Menga <b>poytaxt nomini</b> yozing — "
        "men uning davlatini topaman.\n\n"
        "🔤 Katta yoki kichik harfda yozishingiz mumkin.\n\n"
        "📌 <b>Misol:</b>\n\n"
        "🇺🇿 O‘zbekiston → 🏙 Toshkent\n"
        "🏙 Toshkent → 🇺🇿 O‘zbekiston\n\n"
        "👇 Pastdagi menyudan foydalaning."
    )

    await update.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=main_menu(admin)
    )


# =========================================================
# 🆔 ID
# =========================================================

async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        f"🆔 Sizning Telegram ID'ingiz:\n\n"
        f"<code>{update.effective_user.id}</code>",
        parse_mode="HTML"
    )


# =========================================================
# ❓ YORDAM
# =========================================================

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await typing_animation(update)

    await update.message.reply_text(
        "❓ <b>YORDAM</b>\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "🌍 Davlat yozing → poytaxt chiqadi.\n"
        "🏙 Poytaxt yozing → davlat chiqadi.\n\n"
        "📌 Masalan:\n"
        "🇨🇦 Kanada → 🏙 Ottava\n"
        "🏙 Ottava → 🇨🇦 Kanada\n\n"
        "🔤 Katta-kichik harflar farq qilmaydi.",
        parse_mode="HTML"
    )


# =========================================================
# ℹ️ BOT HAQIDA
# =========================================================

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await typing_animation(update)

    await update.message.reply_text(
        "ℹ️ <b>BOT HAQIDA</b>\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "🌍 <b>Davlat & Poytaxt Bot</b>\n\n"
        "📚 Davlat va poytaxtlarni tez topishga yordam beradi.\n\n"
        "⚡ Tezkor qidiruv\n"
        "🔤 Katta-kichik harf farqi yo‘q\n"
        "🌍 Davlat → Poytaxt\n"
        "🏙 Poytaxt → Davlat\n"
        "🔐 Himoyalangan Admin Panel\n"
        "💾 Ma'lumotlar saqlanadi",
        parse_mode="HTML"
    )


# =========================================================
# 🌍 DAVLATLAR
# =========================================================

async def show_countries(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await typing_animation(update)

    await update.message.reply_text(
        f"🌍 <b>DAVLATLAR</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        f"📚 Bazada <b>{len(countries)}</b> ta davlat yozuvi mavjud.\n\n"
        "Davlat nomini yozing — poytaxtini topaman.",
        parse_mode="HTML"
    )


# =========================================================
# 🏙 POYTAXTLAR
# =========================================================

async def show_capitals(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await typing_animation(update)

    capitals = set(countries.values())

    await update.message.reply_text(
        f"🏙 <b>POYTAXTLAR</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        f"📚 Bazada <b>{len(capitals)}</b> ta poytaxt mavjud.\n\n"
        "Poytaxt nomini yozing — davlatini topaman.",
        parse_mode="HTML"
    )


# =========================================================
# 👑 ADMIN PANEL
# =========================================================

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_admin(update):
        await update.message.reply_text(
            "⛔ <b>Ruxsat berilmadi!</b>",
            parse_mode="HTML"
        )
        return

    context.user_data.clear()

    await typing_animation(update)

    await update.message.reply_text(
        "👑 <b>ADMIN PANEL</b>\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "🔐 Xush kelibsiz, Admin!\n\n"
        f"🌍 Davlatlar: <b>{len(countries)}</b>\n"
        f"👤 Foydalanuvchilar: <b>{len(stats['users'])}</b>\n"
        f"🔎 Qidiruvlar: <b>{stats['searches']}</b>\n\n"
        "👇 Kerakli funksiyani tanlang:",
        parse_mode="HTML",
        reply_markup=admin_menu()
    )


# =========================================================
# ➕ DAVLAT QO'SHISH
# =========================================================

async def add_country_start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_admin(update):
        await update.message.reply_text("⛔ Ruxsat yo'q.")
        return

    context.user_data.clear()
    context.user_data["action"] = "add_country"

    await update.message.reply_text(
        "➕ <b>YANGI DAVLAT QO‘SHISH</b>\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "1️⃣ Davlat nomini yozing.\n\n"
        "Masalan:\n"
        "<code>O‘zbekiston</code>",
        parse_mode="HTML"
    )


# =========================================================
# ✏️ O'ZGARTIRISH
# =========================================================

async def edit_country_start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_admin(update):
        await update.message.reply_text("⛔ Ruxsat yo'q.")
        return

    context.user_data.clear()
    context.user_data["action"] = "edit_country"

    await update.message.reply_text(
        "✏️ <b>DAVLATNI O‘ZGARTIRISH</b>\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "Mavjud davlat nomini yozing.\n\n"
        "Masalan:\n"
        "<code>Kanada</code>",
        parse_mode="HTML"
    )


# =========================================================
# 🗑 O'CHIRISH
# =========================================================

async def delete_country_start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_admin(update):
        await update.message.reply_text("⛔ Ruxsat yo'q.")
        return

    context.user_data.clear()
    context.user_data["action"] = "delete_country"

    await update.message.reply_text(
        "🗑 <b>DAVLATNI O‘CHIRISH</b>\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "O‘chirmoqchi bo‘lgan davlat nomini yozing.\n\n"
        "Masalan:\n"
        "<code>Kanada</code>",
        parse_mode="HTML"
    )


# =========================================================
# 📋 BARCHA DAVLATLAR
# =========================================================

async def all_countries(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_admin(update):
        await update.message.reply_text("⛔ Ruxsat yo'q.")
        return

    names = sorted(countries.keys())

    chunk = ""

    for index, country in enumerate(names, 1):

        line = f"{index}. {country.title()} — {countries[country]}\n"

        if len(chunk) + len(line) > 3500:

            await update.message.reply_text(
                "📋 <b>BARCHA DAVLATLAR</b>\n\n" + chunk,
                parse_mode="HTML"
            )

            chunk = ""

        chunk += line

    if chunk:

        await update.message.reply_text(
            "📋 <b>BARCHA DAVLATLAR</b>\n\n" + chunk,
            parse_mode="HTML"
        )


# =========================================================
# 📊 STATISTIKA
# =========================================================

async def statistics(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_admin(update):
        await update.message.reply_text("⛔ Ruxsat yo'q.")
        return

    capitals = set(countries.values())

    await update.message.reply_text(
        "📊 <b>STATISTIKA</b>\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        f"🌍 Davlatlar: <b>{len(countries)}</b>\n"
        f"🏙 Poytaxtlar: <b>{len(capitals)}</b>\n"
        f"👤 Foydalanuvchilar: <b>{len(stats['users'])}</b>\n"
        f"🔎 Jami qidiruvlar: <b>{stats['searches']}</b>\n"
        f"✅ Topilgan qidiruvlar: <b>{stats['successful_searches']}</b>\n\n"
        f"👑 Admin ID: <code>{ADMIN_ID}</code>",
        parse_mode="HTML"
    )


# =========================================================
# 🌍 DAVLATLAR SONI
# =========================================================

async def country_count(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_admin(update):
        await update.message.reply_text("⛔ Ruxsat yo'q.")
        return

    await update.message.reply_text(
        f"🌍 <b>DAVLATLAR SONI</b>\n\n"
        f"📚 Hozir bazada <b>{len(countries)}</b> ta yozuv mavjud.",
        parse_mode="HTML"
    )


# =========================================================
# 💬 ASOSIY MESSAGE
# =========================================================

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message or not update.message.text:
        return

    user_id = update.effective_user.id

    register_user(user_id)

    original_text = update.message.text.strip()
    text = clean_text(original_text)

    # =====================================================
    # 👑 ADMIN ACTION
    # =====================================================

    action = context.user_data.get("action")

    # -----------------------------------------------------
    # ➕ DAVLAT QO'SHISH
    # -----------------------------------------------------

    if action == "add_country":

        if not is_admin(update):
            context.user_data.clear()
            await update.message.reply_text("⛔ Ruxsat yo'q.")
            return

        context.user_data["new_country"] = text
        context.user_data["action"] = "add_capital"

        await update.message.reply_text(
            "🏙 <b>2-QADAM</b>\n\n"
            "Endi shu davlatning poytaxtini yozing.\n\n"
            "Masalan:\n"
            "<code>Toshkent</code>",
            parse_mode="HTML"
        )
        return

    # -----------------------------------------------------
    # ➕ POYTAXTNI QABUL QILISH
    # -----------------------------------------------------

    if action == "add_capital":

        if not is_admin(update):
            context.user_data.clear()
            await update.message.reply_text("⛔ Ruxsat yo'q.")
            return

        country = context.user_data.get("new_country")
        capital = original_text

        if not country or not capital:
            context.user_data.clear()
            await update.message.reply_text(
                "❌ Ma'lumot noto'g'ri."
            )
            return

        if country in countries:
            await update.message.reply_text(
                "⚠️ Bu davlat allaqachon mavjud."
            )
            return

        countries[country] = capital

        save_countries()

        context.user_data.clear()

        await update.message.reply_text(
            "⏳ Saqlanmoqda..."
        )

        await asyncio.sleep(0.7)

        await update.message.reply_text(
            "🎉 <b>DAVLAT QO‘SHILDI!</b>\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            f"🌍 Davlat: <b>{country.title()}</b>\n"
            f"🏙 Poytaxt: <b>{capital}</b>\n\n"
            "💾 Ma'lumot doimiy saqlandi.",
            parse_mode="HTML",
            reply_markup=admin_menu()
        )

        return

    # -----------------------------------------------------
    # ✏️ O'ZGARTIRISH
    # -----------------------------------------------------

    if action == "edit_country":

        if not is_admin(update):
            context.user_data.clear()
            await update.message.reply_text("⛔ Ruxsat yo'q.")
            return

        if text not in countries:

            await update.message.reply_text(
                "❌ Bu davlat topilmadi.\n\n"
                "Davlat nomini qayta yozing."
            )

            return

        context.user_data["edit_country"] = text
        context.user_data["action"] = "edit_capital"

        await update.message.reply_text(
            f"✏️ <b>{text.title()}</b> topildi.\n\n"
            "🏙 Endi yangi poytaxtni yozing.",
            parse_mode="HTML"
        )

        return

    # -----------------------------------------------------
    # ✏️ YANGI POYTAXT
    # -----------------------------------------------------

    if action == "edit_capital":

        if not is_admin(update):
            context.user_data.clear()
            await update.message.reply_text("⛔ Ruxsat yo'q.")
            return

        country = context.user_data.get("edit_country")
        capital = original_text

        countries[country] = capital

        save_countries()

        context.user_data.clear()

        await update.message.reply_text(
            "⏳ O‘zgartirilmoqda..."
        )

        await asyncio.sleep(0.7)

        await update.message.reply_text(
            "✅ <b>MUVAFFAQIYATLI O‘ZGARTIRILDI!</b>\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            f"🌍 Davlat: <b>{country.title()}</b>\n"
            f"🏙 Yangi poytaxt: <b>{capital}</b>\n\n"
            "💾 Ma'lumot saqlandi.",
            parse_mode="HTML",
            reply_markup=admin_menu()
        )

        return

    # -----------------------------------------------------
    # 🗑 O'CHIRISH
    # -----------------------------------------------------

    if action == "delete_country":

        if not is_admin(update):
            context.user_data.clear()
            await update.message.reply_text("⛔ Ruxsat yo'q.")
            return

        if text not in countries:

            await update.message.reply_text(
                "❌ Bu davlat topilmadi."
            )

            return

        old_capital = countries[text]

        del countries[text]

        save_countries()

        context.user_data.clear()

        await update.message.reply_text(
            "⏳ O‘chirilmoqda..."
        )

        await asyncio.sleep(0.7)

        await update.message.reply_text(
            "🗑 <b>DAVLAT O‘CHIRILDI!</b>\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            f"🌍 Davlat: <b>{text.title()}</b>\n"
            f"🏙 Poytaxt: <b>{old_capital}</b>\n\n"
            "💾 O‘zgarish saqlandi.",
            parse_mode="HTML",
            reply_markup=admin_menu()
        )

        return

    # =====================================================
    # 🎛 MENYU
    # =====================================================

    if original_text == "❓ Yordam":
        await help_command(update, context)
        return

    if original_text == "ℹ️ Bot haqida":
        await about(update, context)
        return

    if original_text == "🌍 Davlatlar":
        await show_countries(update, context)
        return

    if original_text == "🏙 Poytaxtlar":
        await show_capitals(update, context)
        return

    if original_text == "👑 Admin panel":
        await admin_panel(update, context)
        return

    if original_text == "➕ Davlat qo‘shish":
        await add_country_start(update, context)
        return

    if original_text == "✏️ Davlatni o‘zgartirish":
        await edit_country_start(update, context)
        return

    if original_text == "🗑 Davlatni o‘chirish":
        await delete_country_start(update, context)
        return

    if original_text == "📋 Barcha davlatlar":
        await all_countries(update, context)
        return

    if original_text == "📊 Statistika":
        await statistics(update, context)
        return

    if original_text == "🌍 Davlatlar soni":
        await country_count(update, context)
        return

    if original_text == "🔙 Asosiy menyu":

        context.user_data.clear()

        await update.message.reply_text(
            "🏠 <b>ASOSIY MENYU</b>",
            parse_mode="HTML",
            reply_markup=main_menu(is_admin(update))
        )

        return

    # =====================================================
    # 🔎 QIDIRUV
    # =====================================================

    stats["searches"] += 1
    save_stats()

    loading = await search_animation(update)

    # -----------------------------------------------------
    # 🌍 DAVLAT
    # -----------------------------------------------------

    if text in countries:

        stats["successful_searches"] += 1
        save_stats()

        capital = countries[text]

        await loading.edit_text(
            "🎉 <b>TOPILDI!</b>\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            f"🌍 Davlat: <b>{text.title()}</b>\n"
            f"🏙 Poytaxti: <b>{capital}</b>\n\n"
            "✨ Yana davlat yoki poytaxt yozishingiz mumkin.",
            parse_mode="HTML"
        )

        return

    # -----------------------------------------------------
    # 🏙 POYTAXT
    # -----------------------------------------------------

    for country, capital in countries.items():

        if clean_text(capital) == text:

            stats["successful_searches"] += 1
            save_stats()

            await loading.edit_text(
                "🎉 <b>TOPILDI!</b>\n"
                "━━━━━━━━━━━━━━━━━━\n\n"
                f"🏙 Poytaxt: <b>{capital}</b>\n"
                f"🌍 Davlati: <b>{country.title()}</b>\n\n"
                "✨ Yana davlat yoki poytaxt yozishingiz mumkin.",
                parse_mode="HTML"
            )

            return

    # -----------------------------------------------------
    # ❌ TOPILMADI
    # -----------------------------------------------------

    await loading.edit_text(
        "❌ <b>TOPILMADI</b>\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "Men bu nomni davlat yoki poytaxt sifatida topa olmadim.\n\n"
        "📌 Masalan:\n"
        "🇨🇦 <code>Kanada</code>\n"
        "🏙 <code>Ottava</code>\n\n"
        "💡 Nomni yana bir marta tekshirib ko‘ring.",
        parse_mode="HTML"
    )


# =========================================================
# 👑 ADMIN COMMAND
# =========================================================

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_admin(update):

        await update.message.reply_text(
            "⛔ <b>Ruxsat berilmadi!</b>\n\n"
            "Bu bo‘lim faqat administrator uchun.",
            parse_mode="HTML"
        )

        return

    await admin_panel(update, context)


# =========================================================
# 🤖 ISHGA TUSHIRISH
# =========================================================

load_countries()
load_stats()

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("about", about))
app.add_handler(CommandHandler("id", get_id))
app.add_handler(CommandHandler("admin", admin_command))

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        message
    )
)


print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("🌍 DAVLAT & POYTAXT BOT")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("✅ Bot ishga tushdi!")
print("✨ Animatsiyalar: YOQ")
print("👑 Admin panel: YOQ")
print("🔐 Admin himoyasi: YOQ")
print("💾 Doimiy saqlash: YOQ")
print("📊 Statistika: YOQ")
print("🌍 Davlatlar:", len(countries))
print("👑 Admin ID:", ADMIN_ID)
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")


app.run_polling()