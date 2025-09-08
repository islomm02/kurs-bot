# import asyncio
# import logging
# import sys
# from os import getenv
#
# from aiogram import Bot, Dispatcher, html
# from aiogram.client.default import DefaultBotProperties
# from aiogram.enums import ParseMode
# from aiogram.filters import CommandStart
# from aiogram.types import Message
# from dotenv import load_dotenv
# load_dotenv()
#
# TOKEN = getenv("BOT_TOKEN")
#
#
# dp = Dispatcher()
#
#
# @dp.message(CommandStart())
# async def command_start_handler(message: Message) -> None:
#     await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")
#
#
# @dp.message()
# async def echo_handler(message: Message) -> None:
#     try:
#         await message.send_copy(chat_id=message.chat.id)
#     except TypeError:
#         await message.answer("Nice try!")
#
#
# async def main() -> None:
#     bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
#     await dp.start_polling(bot)
#
#
# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO, stream=sys.stdout)
#     asyncio.run(main())


# import torch
# import asyncio
# import logging
# import sys
# from os import getenv
#
# from aiogram import Bot, Dispatcher
# from aiogram.enums import ParseMode, ChatAction
# from aiogram.filters import CommandStart
# from aiogram.types import Message
# from aiogram.client.default import DefaultBotProperties
# from dotenv import load_dotenv
#
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForCausalLM
#
# # .env dan token yuklash
# load_dotenv()
# TOKEN = getenv("BOT_TOKEN")
#
# # ================= Modelni tanlash ================= #
# # Chat uchun yaxshiroq model
# model_name = "google/flan-t5-base"
#
# print("🔄 Model yuklanmoqda, biroz kuting...")
# tokenizer = AutoTokenizer.from_pretrained(model_name)
#
# if "flan-t5" in model_name:
#     model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
# else:
#     model = AutoModelForCausalLM.from_pretrained(model_name)
#
# device = "cuda" if torch.cuda.is_available() else "cpu"
# model.to(device)
# print(f"✅ Model yuklandi! Qurilma: {device}")
# # ==================================================== #
#
# dp = Dispatcher()
#
# # START komandasi
# @dp.message(CommandStart())
# async def start_handler(message: Message):
#     text = (
#         f"Assalomu alaykum, {message.from_user.first_name}! 👋\n\n"
#         "KursBotga xush kelibsiz! 🎓\n"
#         "Bu yerda siz mening yaratgan kurslarim haqida ma'lumot olasiz.\n\n"
#         "❓ Savollaringiz bo‘lsa yozib qoldiring."
#     )
#     await message.answer(text)
#
#
# @dp.message()
# async def ai_handler(message: Message):
#     try:
#         await message.bot.send_chat_action(message.chat.id, ChatAction.TYPING)
#
#         user_text = message.text
#         prompt = f"User: {user_text}\nBot:"   # <-- instruction beramiz
#
#         inputs = tokenizer(prompt, return_tensors="pt").to(device)
#
#         outputs = model.generate(**inputs, max_new_tokens=200)
#         reply = tokenizer.decode(outputs[0], skip_special_tokens=True)
#
#         # faqat "Bot:" dan keyin chiqgan javobni olish
#         if "Bot:" in reply:
#             reply = reply.split("Bot:")[-1].strip()
#
#         await message.answer(reply)
#
#     except Exception as e:
#         await message.answer("Xatolik yuz berdi ❌")
#         print("Error:", e)
#
#
#
# async def main():
#     bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
#     await dp.start_polling(bot)
#
#
# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO, stream=sys.stdout)
#     asyncio.run(main())

# import torch
# import asyncio
# import logging
# import sys
# from os import getenv
#
# from aiogram import Bot, Dispatcher
# from aiogram.enums import ParseMode, ChatAction
# from aiogram.filters import CommandStart
# from aiogram.types import Message
# from aiogram.client.default import DefaultBotProperties
# from dotenv import load_dotenv
#
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
#
# # .env dan token yuklash
# load_dotenv()
# TOKEN = getenv("BOT_TOKEN")
#
# # ================= Modelni tanlash ================= #
# # FLAN-T5 modeli uchun to'g'ri yuklash
# model_name = "google/flan-t5-base"
#
# print("🔄 Model yuklanmoqda, biroz kuting...")
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
#
# # Pipelines yordamida soddalashtirilgan ishlov
# text_generator = pipeline(
#     "text2text-generation",
#     model=model,
#     tokenizer=tokenizer,
#     device=0 if torch.cuda.is_available() else -1
# )
#
# print(f"✅ Model yuklandi! Qurilma: {'GPU' if torch.cuda.is_available() else 'CPU'}")
# # ==================================================== #
#
# dp = Dispatcher()
#
#
# # START komandasi
# @dp.message(CommandStart())
# async def start_handler(message: Message):
#     text = (
#         f"Assalomu alaykum, {message.from_user.first_name}! 👋\n\n"
#         "AI Botga xush kelibsiz! 🎓\n"
#         "Menga istalgan savolingizni berishingiz mumkin.\n\n"
#         "❓ Savollaringiz bo'lsa yozib qoldiring."
#     )
#     await message.answer(text)
#
#
# @dp.message()
# async def ai_handler(message: Message):
#     try:
#         await message.bot.send_chat_action(message.chat.id, ChatAction.TYPING)
#
#         user_text = message.text
#
#         # FLAN-T5 uchun to'g'ri prompt format
#         # Model instruction-following uchun mo'ljallangan
#         prompt = f"Savol: {user_text}\nJavob:"
#
#         # Modeldan javob olish
#         results = text_generator(
#             prompt,
#             max_length=200,
#             num_return_sequences=1,
#             temperature=0.7,
#             repetition_penalty=1.2,
#             do_sample=True
#         )
#
#         reply = results[0]['generated_text']
#
#         # Faqat javob qismini olish
#         if "Javob:" in reply:
#             reply = reply.split("Javob:")[-1].strip()
#
#         await message.answer(reply if reply else "Tushunmadim, qayta urinib ko'ring")
#
#     except Exception as e:
#         await message.answer("Xatolik yuz berdi ❌")
#         logging.error(f"Xato: {e}")
#
#
# async def main():
#     bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
#     await dp.start_polling(bot)
#
#
# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO, stream=sys.stdout)
#     asyncio.run(main())






# import torch
# import asyncio
# import logging
# import sys
# from os import getenv
# import random
#
# from aiogram import Bot, Dispatcher
# from aiogram.enums import ParseMode, ChatAction
# from aiogram.filters import CommandStart
# from aiogram.types import Message
# from aiogram.client.default import DefaultBotProperties
# from dotenv import load_dotenv
#
# from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
#
# # .env faylidan token yuklash
# load_dotenv()
# TOKEN = getenv("BOT_TOKEN")
#
# # Loggerni sozlash
# logging.basicConfig(level=logging.INFO, stream=sys.stdout)
# logger = logging.getLogger(__name__)
#
# # ================= Modelni yuklash ================= #
# try:
#     # Chat uchun yaxshiroq model
#     model_name = "microsoft/DialoGPT-medium"
#
#     print("🔄 Model yuklanmoqda, biroz kuting...")
#
#     # Tokenizer va modelni yuklash
#     tokenizer = AutoTokenizer.from_pretrained(model_name)
#     model = AutoModelForCausalLM.from_pretrained(model_name)
#
#     # Pad token sozlash
#     if tokenizer.pad_token is None:
#         tokenizer.pad_token = tokenizer.eos_token
#
#     # Pipeline yaratish
#     text_generator = pipeline(
#         "text-generation",
#         model=model,
#         tokenizer=tokenizer,
#         device=0 if torch.cuda.is_available() else -1
#     )
#
#     print(f"✅ Model muvaffaqiyatli yuklandi! Qurilma: {'GPU' if torch.cuda.is_available() else 'CPU'}")
#
# except Exception as e:
#     logger.error(f"Model yuklashda xato: {e}")
#     text_generator = None
# # ==================================================== #
#
# dp = Dispatcher()
#
# # Oddiy javoblar lug'ati
# simple_responses = {
#     "salom": ["Salom! Qandaysiz?", "Assalomu alaykum!", "Xush kelibsiz!", "Salom, nimaga yordam bera olaman?"],
#     "python": [
#         "Python - dunyodagi eng mashhur dasturlash tillaridan biri!",
#         "Python haqida savolingiz bo'lsa, javob berishga harakat qilaman.",
#         "Python dasturlash tili sodda va kuchli til hisoblanadi."
#     ],
#     "kurs": [
#         "Kurslar haqida ma'lumot berishim mumkin.",
#         "Qaysi kurs haqida bilmoqchisiz?",
#         "Bizda turli xil dasturlash kurslari mavjud."
#     ],
#     "nima gap": ["Yaxshi, o'zingizchi?", "Ishlar yaxshi, rahmat!", "Do'stona suhbat qilayotganimizdan xursandman!"],
#     "qalaysan": ["Yaxshiman, rahmat! Sizchi?", "Dastur sifatida yaxshi ishlayapman!",
#                  "Rahmat, yaxshi. Sizga qanday yordam bera olaman?"],
#     "dasturlash": [
#         "Dasturlash - bu kompyuterga vazifa bajarishni buyurish san'ati.",
#         "Dasturlashni o'rganish zamonaviy dunyoda muhim ko'nikmadir.",
#         "Dasturlash bir nechta tillarda amalga oshiriladi: Python, JavaScript, Java va boshqalar."
#     ],
#     "yordam": ["Nima yordam bera olaman?", "Qanday yordam kerak?",
#                "Savolingizni berishingiz mumkin, yordam berishga harakat qilaman."],
#     "rahmat": ["Arzimaydi!", "Xursand bo'ldim!", "Yana savolingiz bo'lsa, murojaat qiling!"],
#     "ha": ["Yaxshi!", "Qoyil!", "Davom etaylikmi?"],
#     "yoq": ["Tushunarli.", "Yana bir bor urinib ko'rmaylikmi?", "Boshqa savolingiz bormi?"]
# }
#
#
# # START komandasi
# @dp.message(CommandStart())
# async def start_handler(message: Message):
#     text = (
#         f"Assalomu alaykum, {message.from_user.first_name}! 👋\n\n"
#         "AI Botga xush kelibsiz! 🎓\n"
#         "Menga istalgan savolingizni berishingiz mumkin.\n\n"
#         "❓ Savollaringiz bo'lsa yozib qoldiring."
#     )
#     await message.answer(text)
#
#
# # Foydalanuvchi xabarlarini qayta ishlash
# @dp.message()
# async def ai_handler(message: Message):
#     try:
#         # Yozayotganlik harakatini ko'rsatish
#         await message.bot.send_chat_action(message.chat.id, ChatAction.TYPING)
#
#         user_text = message.text.lower()
#
#         # Avval oddiy javoblar lug'atini tekshirish
#         reply = None
#         for key in simple_responses:
#             if key in user_text:
#                 reply = random.choice(simple_responses[key])
#                 break
#
#         # Agar oddiy javob topilmasa, AI modeldan foydalanish
#         if not reply and text_generator:
#             # Model uchun prompt yaratish
#             prompt = f"User: {user_text}\nBot:"
#
#             # Modeldan javob olish
#             results = text_generator(
#                 prompt,
#                 max_length=150,
#                 num_return_sequences=1,
#                 temperature=0.8,
#                 repetition_penalty=1.1,
#                 pad_token_id=tokenizer.eos_token_id,
#                 do_sample=True
#             )
#
#             reply = results[0]['generated_text']
#
#             # Faqat Bot: dan keyingi qismini olish
#             if "Bot:" in reply:
#                 reply = reply.split("Bot:")[-1].strip()
#
#         # Agar hali ham javob bo'lmasa, standart javob
#         if not reply:
#             reply = "Tushunmadim, batafsilroq savol bering yoki boshqa so'zlar bilan ifodalab ko'ring"
#
#         await message.answer(reply)
#
#     except Exception as e:
#         logger.error(f"Xatolik: {e}")
#         await message.answer("Kechirasiz, texnik xatolik yuz berdi. Iltimos, keyinroq qayta urinib ko'ring.")
#
#
# # Asosiy funksiya
# async def main():
#     try:
#         bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
#         await dp.start_polling(bot)
#     except Exception as e:
#         logger.error(f"Bot ishga tushirishda xato: {e}")
#
#
# if __name__ == "__main__":
#     asyncio.run(main())



import asyncio
import logging
import ssl

import asyncpg
import os
import tempfile
from openpyxl import Workbook
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import (
    Message, ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

# ========================
# LOAD CONFIG
# ========================
load_dotenv()

API_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_NAME = os.getenv("ADMIN_NAME")
CHANNEL_ID = os.getenv("CHANNEL_ID")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

DATABASE_URL = os.getenv("DATABASE_URL")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))

# ========================
# LOGGING
# ========================
logging.basicConfig(level=logging.INFO)

# ========================
# BOT & DISPATCHER
# ========================
bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# ========================
# DATABASE
# ========================
# async def create_db_pool():
#     return await asyncpg.create_pool(
#         user=DB_USER,
#         password=DB_PASS,
#         database=DB_NAME,
#         host=DB_HOST,
#         port=DB_PORT
#     )
#
# db_pool = None
# ========================
# DATABASE
# ========================
async def create_db_pool():
    db_url = os.getenv("DATABASE_URL")

    # SSL konteksti yaratamiz
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    return await asyncpg.create_pool(dsn=db_url, ssl=ssl_context)



# ========================
# FSM HOLATLAR
# ========================
class AdminRegisterState(StatesGroup):
    name = State()
    age = State()
    phone = State()
    telegram_id = State()

class DeleteUserState(StatesGroup):
    waiting_for_id = State()


class AdminRegisterState(StatesGroup):
    name = State()
    age = State()
    phone = State()
    telegram_id = State()

class DeleteUserState(StatesGroup):
    waiting_for_id = State()
    confirm_delete = State()

# ========================
# START MENYU
# ========================
def start_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📚 Kurs haqida ma'lumot")],
            [KeyboardButton(text="📚 Oldingi kurs haqida ma'lumot")],
            [KeyboardButton(text="📞 Admin bilan bog'lanish")],
        ],
        resize_keyboard=True
    )

@dp.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer("Assalomu alaykum! Menyudan birini tanlang 👇", reply_markup=start_menu())

# ========================
# KURS HAQIDA MA'LUMOT
# ========================
@dp.message(F.text == "📚 Oldingi kurs haqida ma'lumot")
async def old_course(message: types.Message):
    await message.answer_document(
        document="https://t.me/kurs_bor/8",
        caption="📚 Oldingi kurs haqida batafsil ma'lumot"
    )

@dp.message(F.text == "📚 Kurs haqida ma'lumot")
async def course_info(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Yetmishboyev Shaxzod", callback_data="teacher_yetmishboyev")],
        [InlineKeyboardButton(text="Tilepova Abadan", callback_data="teacher_tilepova")],
        [InlineKeyboardButton(text="Bushuyev Yevgeniy", callback_data="teacher_bushuyev")],
    ])
    await message.answer("Ustozlardan birini tanlang 👇", reply_markup=kb)


@dp.callback_query(F.data.startswith("teacher_"))
async def teacher_info(callback: types.CallbackQuery):
    teacher = callback.data.split("_")[1]

    teacher_files = {
        "yetmishboyev": {"name": "📘 Yetmishboyev Shaxzod", "message_id": 5},
        "tilepova": {"name": "📘 Tilepova Abadan", "message_id": 6},
        "bushuyev": {"name": "📘 Bushuyev Yevgeniy", "message_id": 7},
    }
    teacher_texts = {
        "yetmishboyev": {"name": "📘 Yetmishboyev Shaxzod", "message_id": 12},
        "tilepova": {"name": "📘 Tilepova Abadan", "message_id": 11},
        "bushuyev": {"name": "📘 Bushuyev Yevgeniy", "message_id": 10},
    }

    file_info = teacher_files.get(teacher)
    text_info = teacher_texts.get(teacher)

    if not file_info or not text_info:
        await callback.message.answer("❌ Bu ustoz uchun ma’lumot topilmadi.")
        await callback.answer()
        return

    async with db_pool.acquire() as conn:
        user = await conn.fetchrow("SELECT * FROM users WHERE telegram_id=$1", callback.from_user.id)

    if user:
        try:
            await callback.bot.copy_message(
                chat_id=callback.from_user.id,
                from_chat_id=CHANNEL_ID,
                message_id=file_info["message_id"]
            )
        except Exception as e:
            await callback.message.answer(f"❌ {file_info['name']} yuborilmadi. Xato: {str(e)}")
    else:
        try:
            await callback.bot.copy_message(
                chat_id=callback.from_user.id,
                from_chat_id=CHANNEL_ID,
                message_id=text_info["message_id"]
            )
        except Exception as e:
            await callback.message.answer(f"❌ {text_info['name']} yuborilmadi. Xato: {str(e)}")

    await callback.answer()

# ========================
# ADMIN PANEL
# ========================


@dp.message(F.text.lower() == "admin")
async def admin_panel(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ Siz admin emassiz!")
        return

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="👤 Userlarni ro‘yxatdan o‘tkazish", callback_data="admin_register")],
            [InlineKeyboardButton(text="📊 Statistika", callback_data="admin_stats")],
            [InlineKeyboardButton(text="❌ Userlarni o‘chirish", callback_data="admin_delete")]
        ]
    )
    await message.answer("🔑 Admin paneliga xush kelibsiz!", reply_markup=kb)

main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(
            text="📞 Admin bilan bog‘lanish",
            url=f"https://t.me/{ADMIN_NAME}"
        )]
    ]
)

@dp.message(F.text == "📞 Admin bilan bog'lanish")
async def contact_admin(message: Message):
    await message.answer(
        "Quyidagi tugma orqali admin bilan bog‘lanishingiz mumkin 👇",
        reply_markup=main_menu
    )

# ========================
# USER DELETE
# ========================
async def delete_user(user_id: int):
    async with db_pool.acquire() as conn:
        await conn.execute("DELETE FROM users WHERE id = $1", user_id)



# ========================
# FSM HOLATLAR
# ========================



# ========================
# ADMIN PANEL
# ========================



# ========================
# ADMIN -> O‘CHIRISHNI BOSADI
# ========================
@dp.callback_query(F.data == "admin_delete")
async def ask_user_id(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("❌ Siz admin emassiz!", show_alert=True)
        return

    await callback.message.answer("🔢 O‘chirmoqchi bo‘lgan user ID ni kiriting:")
    await state.set_state(DeleteUserState.waiting_for_id)


# ========================
# ADMIN -> USER ID KIRITADI
# ========================
@dp.message(DeleteUserState.waiting_for_id)
async def process_user_id(message: Message, state: FSMContext):
    try:
        user_id = int(message.text)

        async with db_pool.acquire() as conn:
            user = await conn.fetchrow("SELECT * FROM users WHERE id=$1", user_id)

        if not user:
            await message.answer("❌ Bunday ID li foydalanuvchi topilmadi.")
            await state.clear()
            return

        text = (
            f"🆔 ID: {user['id']}\n"
            f"👤 Ism: {user['name']}\n"
            f"📅 Yosh: {user['age']}\n"
            f"📱 Telefon: {user['phone']}\n"
            f"💬 Telegram ID: {user['telegram_id']}"
        )

        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="✅ Ha, o‘chirilsin", callback_data=f"confirm_delete:{user_id}")],
                [InlineKeyboardButton(text="❌ Yo‘q, bekor qilinsin", callback_data="cancel_delete")]
            ]
        )

        await message.answer(f"❓ Ushbu foydalanuvchini o‘chirishni tasdiqlaysizmi?\n\n{text}", reply_markup=kb)
        await state.set_state(DeleteUserState.confirm_delete)
        await state.update_data(user_id=user_id)

    except ValueError:
        await message.answer("❌ Iltimos, faqat raqam kiriting (User ID).")


# ========================
# ADMIN -> TASDIQLASH
# ========================
@dp.callback_query(F.data.startswith("confirm_delete"))
async def confirm_delete(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = data.get("user_id")

    if not user_id:
        await callback.message.edit_text("❌ Xatolik: User ID topilmadi.")
        await state.clear()
        return

    async with db_pool.acquire() as conn:
        await conn.execute("DELETE FROM users WHERE id=$1", user_id)

    await callback.message.edit_text(f"✅ User ID {user_id} muvaffaqiyatli o‘chirildi!")
    await state.clear()
    await callback.answer()


@dp.callback_query(F.data == "cancel_delete")
async def cancel_delete(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("❌ O‘chirish bekor qilindi.")
    await state.clear()
    await callback.answer()


@dp.callback_query(F.data == "admin_delete")
async def ask_user_id(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("❌ Siz admin emassiz!", show_alert=True)
        return

    await callback.message.answer("🔢 O‘chirmoqchi bo‘lgan user ID ni kiriting:")
    await state.set_state(DeleteUserState.waiting_for_id)

@dp.message(DeleteUserState.waiting_for_id)
async def process_delete_user(message: Message, state: FSMContext):
    try:
        user_id = int(message.text)
        await delete_user(user_id)
        await message.answer(f"✅ User ID {user_id} muvaffaqiyatli o‘chirildi!")
    except Exception as e:
        await message.answer(f"⚠️ Xatolik: {e}")

    await state.clear()

# ========================
# ADMIN -> USER REGISTRATION
# ========================
@dp.callback_query(F.data == "admin_register")
async def admin_register(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("✍️ F.I ni kiriting:")
    await state.set_state(AdminRegisterState.name)
    await callback.answer()

@dp.message(AdminRegisterState.name)
async def reg_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("📅 Yoshini kiriting:")
    await state.set_state(AdminRegisterState.age)

@dp.message(AdminRegisterState.age)
async def reg_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❌ Yosh faqat raqam bo‘lishi kerak. Qayta kiriting:")
        return
    await state.update_data(age=int(message.text))
    await message.answer("📱 Telefon raqamini kiriting (998xxxxxxxx ko‘rinishda):")
    await state.set_state(AdminRegisterState.phone)

@dp.message(AdminRegisterState.phone)
async def reg_phone(message: Message, state: FSMContext):
    phone = message.text.strip()
    await state.update_data(phone=phone)
    await message.answer("🆔 Telegram ID ni kiriting (raqam ko‘rinishida):")
    await state.set_state(AdminRegisterState.telegram_id)

@dp.message(AdminRegisterState.telegram_id)
async def reg_tg_id(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❌ Telegram ID faqat raqam bo‘lishi kerak. Qayta kiriting:")
        return

    telegram_id = int(message.text)
    data = await state.get_data()
    name = data["name"]
    age = data["age"]
    phone = data["phone"]

    async with db_pool.acquire() as conn:
        existing = await conn.fetchrow(
            "SELECT * FROM users WHERE phone=$1 OR telegram_id=$2",
            phone, telegram_id
        )
        if existing:
            await message.answer("❌ Bu foydalanuvchi allaqachon ro‘yxatdan o‘tgan!")
            await state.clear()
            return

        await conn.execute("""
            INSERT INTO users(name, age, phone, telegram_id)
            VALUES($1, $2, $3, $4)
        """, name, age, phone, telegram_id)

    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="⬅️ Exit")]],
        resize_keyboard=True
    )
    await message.answer("✅ Ma’lumot muvaffaqiyatli saqlandi!", reply_markup=kb)
    await state.clear()

# ========================
# ADMIN -> STATISTIKA
# ========================
@dp.callback_query(F.data == "admin_stats")
async def admin_stats(callback: types.CallbackQuery):
    async with db_pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM users ORDER BY id")

    if not rows:
        await callback.message.answer("📊 Bazada hech qanday foydalanuvchi yo‘q.")
        await callback.answer()
        return

    wb = Workbook()
    ws = wb.active
    ws.title = "Users"
    ws.append(["ID", "Name", "Age", "Phone", "Telegram ID", "Created At"])

    for row in rows:
        ws.append([
            row["id"],
            row["name"],
            row["age"],
            row["phone"],
            row["telegram_id"],
            row["created_at"].strftime("%Y-%m-%d %H:%M:%S") if row["created_at"] else ""
        ])

    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
        wb.save(tmp.name)
        file_path = tmp.name

    await callback.message.answer_document(
        types.FSInputFile(file_path),
        caption="📊 Foydalanuvchilar statistikasi"
    )
    await callback.answer()

# ========================
# EXIT
# ========================
@dp.message(F.text == "⬅️ Exit")
async def exit_handler(message: Message):
    await message.answer("🔙 Bosh menyuga qaytdingiz!", reply_markup=start_menu())

# ========================
# MAIN
# ========================
async def main():
    global db_pool
    db_pool = await create_db_pool()

    async with db_pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id SERIAL PRIMARY KEY,
                name TEXT,
                age INT,
                phone TEXT UNIQUE,
                telegram_id BIGINT UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
