import os
import openai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram.ext import CallbackContext

# دریافت توکن تلگرام و کلید OpenAI از متغیرهای محیطی
TELEGRAM_TOKEN = os.getenv("77278576718:AAFbCmSzoWvaU41tRTdfLpN05ZKPy4hvFlA")
OPENAI_API_KEY = os.getenv("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")

# تنظیمات برای OpenAI API
openai.api_key = OPENAI_API_KEY

# تابعی برای شروع ربات
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("سلام! من ربات شما هستم. سوالی دارید؟")

# تابعی برای پردازش پیام‌های ورودی و ارسال به OpenAI
async def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text  # پیام ورودی کاربر
    try:
        # درخواست به OpenAI برای پردازش پیام
        response = openai.Completion.create(
            model="text-davinci-003",  # مدل مورد نظر
            prompt=user_message,  # ورودی کاربر به عنوان prompt
            max_tokens=150,  # تعداد توکن‌های خروجی
            temperature=0.7  # تنظیم دما برای ایجاد پاسخ
        )
        bot_reply = response.choices[0].text.strip()  # جواب OpenAI

        # ارسال جواب به کاربر در تلگرام
        await update.message.reply_text(bot_reply)

    except Exception as e:
        await update.message.reply_text(f"خطا در ارتباط با OpenAI: {e}")

# تابع اصلی که ربات را اجرا می‌کند
async def main() -> None:
    # ایجاد Application برای ربات تلگرام
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # افزودن دستورات به ربات
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # شروع ربات
    await application.run_polling()

# اجرای تابع اصلی
if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
