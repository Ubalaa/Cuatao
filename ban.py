async def ban(update: Update, context: CallbackContext) -> None:
    chat_member = await context.bot.get_chat_member(update.effective_chat.id, update.effective_user.id)
    if is_admin(update.effective_user.id, chat_member):
        if context.args:
            username = context.args[0].lstrip('@')
            try:
                user = await context.bot.get_chat_member(update.effective_chat.id, username)
                if user.status in ['member', 'restricted']:
                    await context.bot.ban_chat_member(update.effective_chat.id, user.user.id)
                    await update.message.reply_text(f"Đã ban người dùng @{username}.")
                else:
                    await update.message.reply_text(f"Người dùng @{username} không phải là thành viên.")
            except Exception as e:
                logging.error(f"Lỗi khi cấm người dùng @{username}: {e}")
                await update.message.reply_text("Có lỗi xảy ra trong quá trình cấm người dùng.")
        else:
            await update.message.reply_text("Vui lòng cung cấp username cần cấm.")
    else:
        await update.message.reply_text("Bạn không có quyền truy cập lệnh này.")