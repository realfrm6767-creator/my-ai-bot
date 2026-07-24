"""
utils/locales.py
-----------------
متن‌های چندزبانه رابط کاربری ربات و پرامپت سیستمی AI برای هر زبان.
زبان‌های پشتیبانی‌شده: fa, en, ar, ru
"""

SUPPORTED_LANGUAGES = ["fa", "en", "ar", "ru"]

LANGUAGE_NAMES = {"fa": "فارسی", "en": "English", "ar": "العربية", "ru": "Русский"}

TRANSLATIONS = {
    "fa": {
        "btn_ai": "🤖 AI", "btn_settings": "⚙️ تنظیمات", "btn_statistics": "📊 آمار", "btn_help": "❓ راهنما",
        "btn_leaderboard": "🏆 لیدربورد",
        "btn_back": "بازگشت",
        "panel_intro": "پنل مدیریت ربات 👇",
        "not_your_panel": "این پنل مال شما نیست. خودتون یه پنل جدید باز کنید.",
        "help_text": "راهنمای گابیمارو\n\nکافیه اسمم رو صدا بزنی (گابی یا گابیمارو) و هرچی می‌خوای بگی، یا مستقیم روی پیام‌هام ریپلای کنی.",
        "ai_section_text": "هوش مصنوعی گابیمارو فعاله! کافیه اسمم رو صدا بزنی و سوالت رو بپرسی.",
        "ai_access_denied": "این بخش فقط برای مالک قابل دسترسی است.",
        "settings_access_denied": "شما به بخش تنظیمات دسترسی ندارید.",
        "settings_intro": "تنظیمات ربات:",
        "btn_language": "🌐 زبان",
        "btn_memory_on": "حافظه: روشن ✅", "btn_memory_off": "حافظه: خاموش ❌",
        "btn_memory_reset": "🗑 ریست حافظه این چت",
        "memory_reset_done": "حافظه مکالمه این چت پاک شد.",
        "memory_turned_on": "حافظه روشن شد.", "memory_turned_off": "حافظه خاموش شد.",
        "language_menu_intro": "زبان مورد نظر رو انتخاب کن:",
        "language_set_confirm": "زبان ربات به {lang} تغییر کرد.",
        "panel_trigger": "پنل",
        "role_reply_required": "باید روی پیام همون شخص ریپلای کنی.",
        "role_access_main_owner_only_set": "فقط مالک اصلی می‌تواند مالک تنظیم کند.",
        "role_access_main_owner_only_remove": "فقط مالک اصلی می‌تواند مالک را حذف کند.",
        "role_access_owner_level_set": "فقط مالک اصلی یا مالک‌ها می‌توانند مدیر تنظیم کنند.",
        "role_access_owner_level_remove": "فقط مالک اصلی یا مالک‌ها می‌توانند مدیر را حذف کنند.",
        "access_denied_title": "دسترسی محدود",
        "role_set_owner_ok": "به‌عنوان مالک تنظیم شد.", "role_set_owner_already": "در حال حاضر مالک است.",
        "role_remove_owner_ok": "از لیست مالکان ربات حذف شد.", "role_remove_owner_not": "در لیست مالکان ربات وجود ندارد.",
        "role_set_admin_ok": "به‌عنوان مدیر تنظیم شد.", "role_set_admin_already": "در لیست مدیران ربات وجود دارد.",
        "role_remove_admin_ok": "از لیست مدیران ربات حذف شد.", "role_remove_admin_not": "در لیست مدیران ربات وجود ندارد.",
        "role_commands": {"تنظیم مالک": "set_owner", "حذف مالک": "remove_owner", "تنظیم مدیر": "set_admin", "حذف مدیر": "remove_admin"},
        "stat_name": "نام کاربر", "stat_id": "آیدی عددی", "stat_username": "یوزرنیم", "stat_username_none": "ندارد",
        "stat_photo_count": "تعداد تصاویر پروفایل", "stat_photo_unit": "عدد", "stat_role": "مقام کاربر",
        "stat_header": "آمار کاربر", "stat_today": "پیام های امروز", "stat_today_rank": "رتبه در تعداد پیام",
        "stat_total": "کل پیام ها", "stat_total_rank": "رتبه در کل پیام ها",
        "role_main_owner": "مالک اصلی", "role_owner": "مالک", "role_admin": "مدیر", "role_regular": "کاربر عادی",
        "rank_1": "🥇 نفر اول", "rank_2": "🥈 نفر دوم", "rank_3": "🥉 نفر سوم", "rank_unknown": "نامشخص",
        "ai_error": "یه مشکلی موقع پاسخ دادن پیش اومد، دوباره امتحان کن.",
        "leaderboard_header": "لیدربورد گروه",
        "leaderboard_empty": "هنوز کسی توی این گروه پیامی نداده.",
        "leaderboard_scope_today": "امروز", "leaderboard_scope_total": "کل زمان",
    },
    "en": {
        "btn_ai": "🤖 AI", "btn_settings": "⚙️ Settings", "btn_statistics": "📊 Statistics", "btn_help": "❓ Help",
        "btn_leaderboard": "🏆 Leaderboard",
        "btn_back": "Back",
        "panel_intro": "Bot control panel 👇",
        "not_your_panel": "This panel isn't yours. Open your own panel.",
        "help_text": "Gabimaru Help\n\nJust say my name (Gabi or Gabimaru) followed by what you need, or reply directly to my messages.",
        "ai_section_text": "Gabimaru AI is active! Just say my name and ask your question.",
        "ai_access_denied": "This section is only available to the owner.",
        "settings_access_denied": "You don't have access to Settings.",
        "settings_intro": "Bot settings:",
        "btn_language": "🌐 Language",
        "btn_memory_on": "Memory: ON ✅", "btn_memory_off": "Memory: OFF ❌",
        "btn_memory_reset": "🗑 Reset this chat's memory",
        "memory_reset_done": "This chat's conversation memory has been cleared.",
        "memory_turned_on": "Memory turned on.", "memory_turned_off": "Memory turned off.",
        "language_menu_intro": "Choose a language:",
        "language_set_confirm": "Bot language changed to {lang}.",
        "panel_trigger": "panel",
        "role_reply_required": "You need to reply to that person's message.",
        "role_access_main_owner_only_set": "Only the main owner can set an owner.",
        "role_access_main_owner_only_remove": "Only the main owner can remove an owner.",
        "role_access_owner_level_set": "Only the main owner or owners can set an admin.",
        "role_access_owner_level_remove": "Only the main owner or owners can remove an admin.",
        "access_denied_title": "Access restricted",
        "role_set_owner_ok": "has been set as owner.", "role_set_owner_already": "is already an owner.",
        "role_remove_owner_ok": "has been removed from owners.", "role_remove_owner_not": "is not in the owners list.",
        "role_set_admin_ok": "has been set as admin.", "role_set_admin_already": "is already an admin.",
        "role_remove_admin_ok": "has been removed from admins.", "role_remove_admin_not": "is not in the admins list.",
        "role_commands": {"set owner": "set_owner", "remove owner": "remove_owner", "set admin": "set_admin", "remove admin": "remove_admin"},
        "stat_name": "Name", "stat_id": "User ID", "stat_username": "Username", "stat_username_none": "none",
        "stat_photo_count": "Profile photos", "stat_photo_unit": "", "stat_role": "Role",
        "stat_header": "User Stats", "stat_today": "Messages today", "stat_today_rank": "Today's rank",
        "stat_total": "Total messages", "stat_total_rank": "Overall rank",
        "role_main_owner": "Main Owner", "role_owner": "Owner", "role_admin": "Admin", "role_regular": "Regular User",
        "rank_1": "🥇 1st place", "rank_2": "🥈 2nd place", "rank_3": "🥉 3rd place", "rank_unknown": "unknown",
        "ai_error": "Something went wrong while replying, try again.",
        "leaderboard_header": "Group Leaderboard",
        "leaderboard_empty": "No one has sent a message in this group yet.",
        "leaderboard_scope_today": "Today", "leaderboard_scope_total": "All Time",
    },
    "ar": {
        "btn_ai": "🤖 الذكاء الاصطناعي", "btn_settings": "⚙️ الإعدادات", "btn_statistics": "📊 الإحصائيات", "btn_help": "❓ المساعدة",
        "btn_leaderboard": "🏆 المتصدرون",
        "btn_back": "رجوع",
        "panel_intro": "لوحة تحكم البوت 👇",
        "not_your_panel": "هذه اللوحة ليست لك. افتح لوحتك الخاصة.",
        "help_text": "مساعدة غابيمارو\n\nفقط قل اسمي (غابي أو غابيمارو) متبوعًا بما تحتاجه، أو رد مباشرة على رسائلي.",
        "ai_section_text": "الذكاء الاصطناعي لغابيمارو مفعّل! فقط قل اسمي واطرح سؤالك.",
        "ai_access_denied": "هذا القسم متاح فقط للمالك.",
        "settings_access_denied": "لا تملك صلاحية الوصول إلى الإعدادات.",
        "settings_intro": "إعدادات البوت:",
        "btn_language": "🌐 اللغة",
        "btn_memory_on": "الذاكرة: تعمل ✅", "btn_memory_off": "الذاكرة: متوقفة ❌",
        "btn_memory_reset": "🗑 إعادة تعيين ذاكرة هذه المحادثة",
        "memory_reset_done": "تم مسح ذاكرة هذه المحادثة.",
        "memory_turned_on": "تم تشغيل الذاكرة.", "memory_turned_off": "تم إيقاف الذاكرة.",
        "language_menu_intro": "اختر اللغة:",
        "language_set_confirm": "تم تغيير لغة البوت إلى {lang}.",
        "panel_trigger": "لوحة",
        "role_reply_required": "يجب الرد على رسالة ذلك الشخص.",
        "role_access_main_owner_only_set": "فقط المالك الرئيسي يمكنه تعيين مالك.",
        "role_access_main_owner_only_remove": "فقط المالك الرئيسي يمكنه إزالة مالك.",
        "role_access_owner_level_set": "فقط المالك الرئيسي أو المالكون يمكنهم تعيين مدير.",
        "role_access_owner_level_remove": "فقط المالك الرئيسي أو المالكون يمكنهم إزالة مدير.",
        "access_denied_title": "الوصول مقيد",
        "role_set_owner_ok": "تم تعيينه كمالك.", "role_set_owner_already": "هو بالفعل مالك.",
        "role_remove_owner_ok": "تمت إزالته من قائمة المالكين.", "role_remove_owner_not": "غير موجود في قائمة المالكين.",
        "role_set_admin_ok": "تم تعيينه كمدير.", "role_set_admin_already": "هو بالفعل مدير.",
        "role_remove_admin_ok": "تمت إزالته من قائمة المديرين.", "role_remove_admin_not": "غير موجود في قائمة المديرين.",
        "role_commands": {"تعيين المالك": "set_owner", "إزالة المالك": "remove_owner", "تعيين المدير": "set_admin", "إزالة المدير": "remove_admin"},
        "stat_name": "الاسم", "stat_id": "المعرف الرقمي", "stat_username": "اسم المستخدم", "stat_username_none": "لا يوجد",
        "stat_photo_count": "عدد صور الملف الشخصي", "stat_photo_unit": "", "stat_role": "الرتبة",
        "stat_header": "إحصائيات المستخدم", "stat_today": "رسائل اليوم", "stat_today_rank": "الترتيب اليومي",
        "stat_total": "إجمالي الرسائل", "stat_total_rank": "الترتيب الإجمالي",
        "role_main_owner": "المالك الرئيسي", "role_owner": "مالك", "role_admin": "مدير", "role_regular": "مستخدم عادي",
        "rank_1": "🥇 المرتبة الأولى", "rank_2": "🥈 المرتبة الثانية", "rank_3": "🥉 المرتبة الثالثة", "rank_unknown": "غير معروف",
        "ai_error": "حدث خطأ أثناء الرد، حاول مرة أخرى.",
        "leaderboard_header": "متصدرو المجموعة",
        "leaderboard_empty": "لم يرسل أحد رسالة في هذه المجموعة بعد.",
        "leaderboard_scope_today": "اليوم", "leaderboard_scope_total": "كل الوقت",
    },
    "ru": {
        "btn_ai": "🤖 ИИ", "btn_settings": "⚙️ Настройки", "btn_statistics": "📊 Статистика", "btn_help": "❓ Помощь",
        "btn_leaderboard": "🏆 Лидерборд",
        "btn_back": "Назад",
        "panel_intro": "Панель управления ботом 👇",
        "not_your_panel": "Эта панель не ваша. Откройте свою собственную панель.",
        "help_text": "Помощь Gabimaru\n\nПросто произнеси моё имя (Габи или Габимару), а затем скажи, что нужно, или ответь прямо на моё сообщение.",
        "ai_section_text": "ИИ Gabimaru активен! Просто позови меня и задай вопрос.",
        "ai_access_denied": "Этот раздел доступен только владельцу.",
        "settings_access_denied": "У вас нет доступа к настройкам.",
        "settings_intro": "Настройки бота:",
        "btn_language": "🌐 Язык",
        "btn_memory_on": "Память: Вкл ✅", "btn_memory_off": "Память: Выкл ❌",
        "btn_memory_reset": "🗑 Сбросить память этого чата",
        "memory_reset_done": "Память этого чата очищена.",
        "memory_turned_on": "Память включена.", "memory_turned_off": "Память выключена.",
        "language_menu_intro": "Выберите язык:",
        "language_set_confirm": "Язык бота изменён на {lang}.",
        "panel_trigger": "панель",
        "role_reply_required": "Нужно ответить на сообщение этого человека.",
        "role_access_main_owner_only_set": "Только главный владелец может назначить владельца.",
        "role_access_main_owner_only_remove": "Только главный владелец может снять владельца.",
        "role_access_owner_level_set": "Только главный владелец или владельцы могут назначить админа.",
        "role_access_owner_level_remove": "Только главный владелец или владельцы могут снять админа.",
        "access_denied_title": "Доступ ограничен",
        "role_set_owner_ok": "назначен владельцем.", "role_set_owner_already": "уже является владельцем.",
        "role_remove_owner_ok": "удалён из владельцев.", "role_remove_owner_not": "не найден в списке владельцев.",
        "role_set_admin_ok": "назначен админом.", "role_set_admin_already": "уже является админом.",
        "role_remove_admin_ok": "удалён из админов.", "role_remove_admin_not": "не найден в списке админов.",
        "role_commands": {"назначить владельца": "set_owner", "снять владельца": "remove_owner", "назначить админа": "set_admin", "снять админа": "remove_admin"},
        "stat_name": "Имя", "stat_id": "ID", "stat_username": "Юзернейм", "stat_username_none": "нет",
        "stat_photo_count": "Кол-во фото профиля", "stat_photo_unit": "", "stat_role": "Роль",
        "stat_header": "Статистика пользователя", "stat_today": "Сообщений сегодня", "stat_today_rank": "Место сегодня",
        "stat_total": "Всего сообщений", "stat_total_rank": "Общее место",
        "role_main_owner": "Главный владелец", "role_owner": "Владелец", "role_admin": "Админ", "role_regular": "Обычный пользователь",
        "rank_1": "🥇 1 место", "rank_2": "🥈 2 место", "rank_3": "🥉 3 место", "rank_unknown": "неизвестно",
        "ai_error": "Что-то пошло не так, попробуй ещё раз.",
        "leaderboard_header": "Лидерборд группы",
        "leaderboard_empty": "В этой группе пока никто не писал.",
        "leaderboard_scope_today": "Сегодня", "leaderboard_scope_total": "За всё время",
    },
}

SYSTEM_PROMPTS = {
    "fa": (
        "تو گابیمارو هستی، یک ربات هوش مصنوعی داخل تلگرام. "
        "با لحن محاوره‌ای و عامیانه‌ی خودمونی جواب بده، دقیقاً همونجوری که "
        "یه آدم عادی توی چت تایپ می‌کنه، نه رسمی و نه با ادای دوستی مصنوعی. "
        "جواب‌ها کوتاه و مستقیم باشن. از ایموجی خیلی کم استفاده کن، فقط "
        "توی موارد حساس یا مهم یه ایموجی مناسب بذار. "
        "همیشه فقط به فارسی جواب بده، حتی اگه کاربر زبان دیگه‌ای بنویسه."
    ),
    "en": (
        "You are Gabimaru, an AI bot inside Telegram. "
        "Reply in a casual, slang-heavy, everyday texting tone — not formal, "
        "and not overly friendly or performative. Keep replies short and direct. "
        "Use emojis rarely, only for sensitive or important moments. "
        "Always reply only in English, even if the user writes in another language."
    ),
    "ar": (
        "أنت غابيمارو، بوت ذكاء اصطناعي داخل تيليجرام. "
        "أجب بأسلوب عامي ودارج، كأنك شخص عادي يكتب في المحادثة. "
        "اجعل الردود قصيرة ومباشرة. استخدم الرموز التعبيرية نادرًا. "
        "أجب دائمًا باللغة العربية فقط، حتى لو كتب المستخدم بلغة أخرى."
    ),
    "ru": (
        "Ты Gabimaru, ИИ-бот в Telegram. "
        "Отвечай в неформальном, разговорном тоне, как обычный человек в чате. "
        "Ответы короткие и по делу. Используй эмодзи редко. "
        "Всегда отвечай только на русском языке, даже если пользователь пишет на другом языке."
    ),
}


def t(key: str, lang: str) -> str:
    lang_dict = TRANSLATIONS.get(lang, TRANSLATIONS["fa"])
    return lang_dict.get(key, TRANSLATIONS["fa"].get(key, key))


def get_role_commands(lang: str) -> dict:
    return TRANSLATIONS.get(lang, TRANSLATIONS["fa"]).get("role_commands", {})


def get_panel_trigger(lang: str) -> str:
    return t("panel_trigger", lang)


def get_system_prompt(lang: str) -> str:
    return SYSTEM_PROMPTS.get(lang, SYSTEM_PROMPTS["fa"])