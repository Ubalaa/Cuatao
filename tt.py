import logging
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

API_KEY = 'ba4e1e498fa55a0d9da395574502ad86'

async def thoitiet(update: Update, context: CallbackContext) -> None:
    if context.args:
        city_name = " ".join(context.args)
    else:
        await update.message.reply_text("Vui lòng nhập tên thành phố để tra cứu thời tiết.\nVí dụ: /thoitiet Hà Nội")
        return

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name},Vietnam&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        res = response.json()
        logger.info(res)

        if res["cod"] != 200:
            await update.message.reply_text("Không tìm thấy dữ liệu của thành phố bạn tra cứu 🙁 \nVui lòng thử tìm thành phố khác.")
        else:
            data = res["main"]
            live_temperature = data["temp"]
            live_pressure = data["pressure"]
            weather_description = res["weather"][0]["description"]

            weather_info = (
                f"Bạn đã tra cứu dữ liệu thời tiết cho {city_name}.\n"
                f"- Nhiệt độ: {live_temperature:.0f}°C\n"
                f"- Áp suất: {live_pressure} hPa\n"
                f"- Tình trạng thời tiết: {weather_description.capitalize()}"
            )
            await update.message.reply_text(weather_info)
    except Exception as e:
        logger.error(f"Lỗi khi lấy dữ liệu thời tiết: {e}")
        await update.message.reply_text("Có lỗi xảy ra trong quá trình lấy dữ liệu thời tiết.")

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Chào bạn! Tôi là bot thời tiết. Hãy gõ /thoitiet [Tên thành phố] để tra cứu thời tiết.")

def main() -> None:
    updater = Updater("7625460762:AAHuCb0kEZAgOES9wH4aH-44iscrMm4_ekU")

    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("thoitiet", thoitiet))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
