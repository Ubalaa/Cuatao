async def view_notes(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id in user_notes and user_notes[user_id]:
        response = "\n".join([f"{idx + 1}. {note}" for idx, note in enumerate(user_notes[user_id])])
        await update.message.reply_text(f"Ghi chú của bạn:\n{response}")
    else:
        await update.message.reply_text("Bạn chưa lưu ghi chú nào.")