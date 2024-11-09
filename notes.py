async def note(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id not in user_notes:
        user_notes[user_id] = []

    if context.args:
        note_text = ' '.join(context.args)
        user_notes[user_id].append(note_text)
        await update.message.reply_text("Ghi chú đã được lưu!")
    else:
        await update.message.reply_text("• Vui lòng cung cấp nội dung ghi chú.\n• Ví dụ /note nội dung.\n📝 Xem nội dung ghi chú dùng lệnh /viewnotes")