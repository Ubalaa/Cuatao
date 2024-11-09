await update.message.reply_text(message)

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
        logging.info(res)

        if res["cod"] != "404":
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
        else:
            await update.message.reply_text("Không tìm thấy dữ liệu của thành phố bạn tra cứu 🙁 \nVui lòng thử tìm thành phố khác.")
    except Exception as e:
        logging.error(f"Lỗi khi lấy dữ liệu thời tiết: {e}")
        await update.message.reply_text("Có lỗi xảy ra trong quá trình lấy dữ liệu thời tiết.")
