async def lamqtv(update: Update, context: CallbackContext) -> None:
    chat_member = await context.bot.get_chat_member(update.effective_chat.id, update.effective_user.id)
    if is_admin(update.effective_user.id, chat_member):
        if context.args:
            username = context.args[0].lstrip('@')
            try:
                user = await context.bot.get_chat_member(update.effective_chat.id, username)
                await context.bot.promote_chat_member(update.effective_chat.id, user.user.id, 
                                                       can_change_info=True,
                                                       can_post_messages=True,
                                                       can_edit_messages=True,
                                                       can_delete_messages=True,
                                                       can_invite_to_chat=True,
                                                       can_restrict_members=True,
                                                       can_pin_messages=True,
                                                       can_promote_members=True)
                await update.message.reply_text(f"Đã tăng quyền quản trị viên cho @{username}.")
            except Exception as e:
                logging.error(f"Lỗi khi tăng quyền cho @{username}: {e}")
                await update.message.reply_text("Có lỗi xảy ra trong quá trình tăng quyền.")
        else:
            await update.message.reply_text("Vui lòng cung cấp username cần tăng quyền.")
    else:
        await update.message.reply_text("Bạn không có quyền truy cập lệnh này.")

async def off(update: Update, context: CallbackContext) -> None:
    chat_member = await context.bot.get_chat_member(update.effective_chat.id, update.effective_user.id)
    if is_admin(update.effective_user.id, chat_member):
        global bot_running
        bot_running = False
        await update.message.reply_text("Bot đang tắt...")
    else:
        await update.message.reply_text("Bạn không có quyền truy cập lệnh này.")
