import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "8870740034:AAEnii8gXQqBvOdo_yaOodJt22yrhsBnGsQ")
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://khnzvskyutkrmaiyvaqgc.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imtobnp2c2t5dXRrcm1haXl2YXFnYyIsInJvbGUiOiJhbm9uIiwiaWF0IjoxNzU5NjM5NDI5LCJleHAiOjIwNzUyMTU0Mjl9.J1QJ45ah01InwToYv99iFPyyc1timSs9_3N1bzTMqmQ")

logging.basicConfig(level=logging.INFO)

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    try:
        logging.info(f"/start from {message.from_user.id}")
        res = supabase.table("products").select("*").eq("is_active", True).execute()
        products = res.data

        if not products:
            await message.answer("المتجر فاضي حالياً. ضيف منتجات في جدول products وخلي is_active = true")
            return

        keyboard = []
        for p in products:
            try:
                stock = supabase.table("stock").select("*", count="exact").eq("product_id", p['id']).eq("is_sold", False).execute()
                count = stock.count if hasattr(stock, 'count') and stock.count is not None else len(stock.data)
            except Exception as e:
                logging.error(f"stock error {e}")
                count = 0
            status = f"{count} متوفر" if count > 0 else "نفذ"
            keyboard.append([InlineKeyboardButton(text=f"{p['title']} - {p['price']} جنيه ({status})", callback_data=f"buy_{p['id']}")])

        await message.answer("💡 أهلاً بيك في Fekra AI\nاختر المنتج:", reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))
    except Exception as e:
        logging.exception(e)
        await message.answer(f"حصل خطأ، تأكد من Supabase: {e}")

@dp.callback_query(lambda c: c.data.startswith("buy_"))
async def buy_callback(callback: types.CallbackQuery):
    try:
        product_id = callback.data.replace("buy_", "")
        stock_res = supabase.table("stock").select("*").eq("product_id", product_id).eq("is_sold", False).limit(1).execute()
        if not stock_res.data:
            await callback.answer("نفذ للأسف", show_alert=True)
            return
        stock = stock_res.data[0]
        supabase.table("stock").update({"is_sold": True}).eq("id", stock['id']).execute()
        product = supabase.table("products").select("title").eq("id", product_id).single().execute()
        await callback.message.answer(f"✅ تم!\n\n📦 المنتج: {product.data['title']}\n🔑 الكود:\n`{stock['code_value']}`\n\nانسخ الكود واستمتع", parse_mode="Markdown")
        await callback.answer()
    except Exception as e:
        logging.exception(e)
        await callback.answer(f"خطأ: {e}", show_alert=True)

async def main():
    logging.info("البوت شغال على Render...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
