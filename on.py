async def on(update: Update, context: CallbackContext) -> None:
    global bot_running
    chat_member = await context.bot.get_chat_member(update.effective_chat.id, update.effective_user.id)
    if is_admin(update.effective_user.id, chat_member):
        if not bot_running:
            bot_running = True
            await update.message.reply_text("Bot đang bật...")
            main()  # Khởi động lại bot chỉ khi cần thiết
        else:
            await update.message.reply_text("Bot đã hoạt động.")
    else:
        await update.message.reply_text("Bạn không có quyền truy cập lệnh này.")