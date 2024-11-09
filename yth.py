async def favorites(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id not in user_favorites:
        user_favorites[user_id] = []

    if context.args:
        favorite_movie = ' '.join(context.args)
        user_favorites[user_id].append(favorite_movie)
        await update.message.reply_text("Phim đã được thêm vào danh sách yêu thích!")
    else:
        await update.message.reply_text("• Vui lòng cung cấp tên phim để thêm vào danh sách yêu thích.\n• Ví dụ /favorites tên film hoặc link film yêu thích.\n😻 Xem nội dung yêu thích dùng lệnh /viewfavorites.")
