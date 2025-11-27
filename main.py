import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from datetime import datetime, timedelta

# 🔥 API KEY KERAKMAS — lokal model ishlatiladi (Qwen mini)
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Modelni yuklash
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct")
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct")

# 🚀 Telegram bot tokenini shu yerga yozasiz
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# Ban ro'yxati
ban_list = {}

def ai_answer(message: str):
    inputs = tokenizer(message, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=200)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

@dp.message_handler()
async def handle_message(msg: types.Message):
    user_id = msg.from_user.id
    text = msg.text.lower()

    # ❗ So‘kinish tekshiruvi
    bad_words = ["onani ami" , "xaromi" , "aminga skey" , "dalbayob" , "qotoq" , "am bashara" , "fuck" , " nigga"]  # kerak bo‘lsa kengaytirasan

    if any(b in text for b in bad_words):
        ban_list[user_id] = datetime.now() + timedelta(days=14)
        await msg.answer("❌ Siz 2 hafta ban qilindingiz.")
        return

    # Agar ban bo'lsa
    if user_id in ban_list:
        if datetime.now() < ban_list[user_id]:
            await msg.answer("❌ Siz hali ban holatidasiz.")
            return
        else:
            del ban_list[user_id]  # ban o‘chadi

    # AI dan javob
    answer = ai_answer(msg.text)
    await msg.answer(answer)

if __name__ == "__main__":
    executor.start_polling(dp)
