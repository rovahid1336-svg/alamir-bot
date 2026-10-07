import logging
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# توكن البوت الخاص بك
TOKEN = "8601689056:AAFq70pkrXPVQm8a5b3QhBOhWgiKgn8CAKk"

# إعداد الربط مع Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# فتح جدول البيانات الخاص بمطبعة الأمير
sheet = client.open("Al-Amir Printing Orders").sheet1

# إعداد نظام التسجيل
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if not text:
        return

    # تحديد القسم بناءً على الهاشتاق
    department = None
    if "#تصميم" in text:
        department = "التصميم"
    elif "#طباعة" in text:
        department = "الطباعة"
    elif "#مطبوعات" in text:
        department = "المطبوعات"
    elif "#cnc" in text or "#CNC" in text:
        department = "مصمم CNC"
    elif "#ورشة" in text:
        department = "الورشة"

    if department:
        user = update.message.from_user.first_name
        order_text = text
        
        # إضافة الطلب إلى جدول Google Sheets
        sheet.append_row([user, department, order_text, "قيد العمل"])
        
        # إرسال تأكيد في الجروب
        await update.message.reply_text(f"✅ تم تسجيل الطلب بنجاح في قسم: {department}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("🤖 بوت مطبعة الأمير يعمل الآن ويستمع للرسائل...")
    app.run_polling()