async def handle_role_command(update: Update, context: ContextTypes.DEFAULT_TYPE, command: str) -> None:
    reply = update.message.reply_to_message
    if reply is None or reply.from_user is None:
        await update.message.reply_text("باید روی پیام همون شخص ریپلای کنی 🙂")
        return

    actor_id = update.effective_user.id
    target_user = reply.from_user
    target_id = target_user.id
    name = target_user.first_name

    if command == "set_owner":
        if not is_main_owner(actor_id):
            await update.message.reply_text(
                "⛔️ <b>دسترسی نداری</b>\nفقط مالک اصلی می‌تونه مالک جدید تنظیم کنه.",
                parse_mode="HTML",
            )
            return
        if add_owner(target_id):
            await update.message.reply_text(
                f"👑 <b>{name}</b> به‌عنوان <b>مالک</b> تنظیم شد.",
                parse_mode="HTML",
            )
        else:
            await update.message.reply_text("⚠️ این کاربر از قبل مالکه (یا مالک اصلیه).")

    elif command == "remove_owner":
        if not is_main_owner(actor_id):
            await update.message.reply_text(
                "⛔️ <b>دسترسی نداری</b>\nفقط مالک اصلی می‌تونه مالک رو حذف کنه.",
                parse_mode="HTML",
            )
            return
        if remove_owner(target_id):
            await update.message.reply_text(
                f"❌ مالکیت <b>{name}</b> حذف شد.",
                parse_mode="HTML",
            )
        else:
            await update.message.reply_text("⚠️ این کاربر مالک نبود.")

    elif command == "set_admin":
        if not (is_main_owner(actor_id) or is_owner(actor_id)):
            await update.message.reply_text(
                "⛔️ <b>دسترسی نداری</b>\nفقط مالک اصلی یا مالک‌ها می‌تونن مدیر تنظیم کنن.",
                parse_mode="HTML",
            )
            return
        if add_admin(target_id):
            await update.message.reply_text(
                f"🛡 <b>{name}</b> به‌عنوان <b>مدیر</b> تنظیم شد.",
                parse_mode="HTML",
            )
        else:
            await update.message.reply_text("⚠️ این کاربر از قبل مدیره.")

    elif command == "remove_admin":
        if not (is_main_owner(actor_id) or is_owner(actor_id)):
            await update.message.reply_text(
                "⛔️ <b>دسترسی نداری</b>\nفقط مالک اصلی یا مالک‌ها می‌تونن مدیر رو حذف کنن.",
                parse_mode="HTML",
            )
            return
        if remove_admin(target_id):
            await update.message.reply_text(
                f"❌ مدیریت <b>{name}</b> حذف شد.",
                parse_mode="HTML",
            )
        else:
            await update.message.reply_text("⚠️ این کاربر مدیر نبود.")