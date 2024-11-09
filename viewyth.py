async def view_favorites(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id in user_favorites and user_favorites[user_id]:
        response = "\n".join(user_favorites[user_id])
        await update.message.reply_text(f"Phim yêu thích của bạn:\n{response}")
    else:
        await update.message.reply_text("Bạn chưa lưu phim nào vào danh sách yêu thích.")
