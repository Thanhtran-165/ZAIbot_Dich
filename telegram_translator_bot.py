#!/usr/bin/env python3
"""
🌐 Telegram Translator Bot - Open Source Version
=================================================
A powerful Telegram bot for instant translation to Vietnamese using Z.AI's GLM-4.5-Flash model.

Author: Bo
Version: 2.0 Open Source
License: MIT
GitHub: [Your GitHub URL]

Requirements:
- Python 3.8+
- Telegram Bot Token
- Z.AI API Key
"""

import os
import sys
import logging
import asyncio
import json
from typing import Dict, Any, Optional
from datetime import datetime
from zai import ZaiClient
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, 
    CallbackQueryHandler, filters, ContextTypes
)
from dotenv import load_dotenv

# ASCII Art Banner
BANNER = """
╔══════════════════════════════════════════════════════╗
║     🌐 TELEGRAM TRANSLATOR BOT - OPEN SOURCE 🌐      ║
║           Powered by Z.AI GLM-4.5-Flash              ║
╚══════════════════════════════════════════════════════╝
"""

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration class
class Config:
    """Bot configuration management"""
    
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    ZAI_API_KEY = os.getenv('ZAI_API_KEY')
    
    # Optional configurations
    MAX_MESSAGE_LENGTH = int(os.getenv('MAX_MESSAGE_LENGTH', '4000'))
    DEFAULT_LANGUAGE = os.getenv('DEFAULT_LANGUAGE', 'vi')  # Vietnamese
    ENABLE_STATS = os.getenv('ENABLE_STATS', 'true').lower() == 'true'
    ADMIN_USER_ID = os.getenv('ADMIN_USER_ID', '')
    
    @classmethod
    def validate(cls) -> tuple[bool, str]:
        """Validate required configurations"""
        errors = []
        
        if not cls.TELEGRAM_TOKEN:
            errors.append("❌ TELEGRAM_TOKEN not found in .env file")
        elif not cls.TELEGRAM_TOKEN.startswith(('bot', '')) or ':' not in cls.TELEGRAM_TOKEN:
            errors.append("❌ TELEGRAM_TOKEN format appears invalid")
            
        if not cls.ZAI_API_KEY:
            errors.append("❌ ZAI_API_KEY not found in .env file")
            
        if errors:
            return False, "\n".join(errors)
        return True, "✅ Configuration validated successfully"

# Default user preferences
DEFAULT_PREFERENCES = {
    'style': 'professional',
    'temperature': 0.3,
    'format_preserve': True,
    'add_notes': False,
    'target_language': 'vi',
    'show_original': False
}

# Store user preferences and statistics
user_preferences: Dict[int, Dict[str, Any]] = {}
user_statistics: Dict[int, Dict[str, Any]] = {}

# Translation styles with detailed configurations
TRANSLATION_STYLES = {
    'professional': {
        'name': '💼 Chuyên nghiệp',
        'description': 'Phong cách trang trọng, chính xác về thuật ngữ',
        'system_prompt': 'Bạn là một dịch giả chuyên nghiệp với kinh nghiệm cao. Dịch văn bản với phong cách trang trọng, chính xác về mặt thuật ngữ chuyên môn.',
        'temperature': 0.3
    },
    'casual': {
        'name': '😊 Thân thiện',
        'description': 'Phong cách tự nhiên, dễ hiểu',
        'system_prompt': 'Bạn là một dịch giả thân thiện. Dịch văn bản với phong cách tự nhiên, dễ hiểu, gần gũi với người đọc.',
        'temperature': 0.5
    },
    'academic': {
        'name': '🎓 Học thuật',
        'description': 'Chính xác cao, giữ thuật ngữ chuyên ngành',
        'system_prompt': 'Bạn là một dịch giả học thuật chuyên sâu. Dịch văn bản với độ chính xác cao, giữ nguyên thuật ngữ chuyên ngành khi cần thiết, kèm giải thích.',
        'temperature': 0.2
    },
    'creative': {
        'name': '🎨 Sáng tạo',
        'description': 'Linh hoạt, giữ thần văn bản',
        'system_prompt': 'Bạn là một dịch giả sáng tạo. Dịch văn bản một cách linh hoạt, sáng tạo nhưng vẫn giữ được tinh thần và ý nghĩa của văn bản gốc.',
        'temperature': 0.7
    },
    'technical': {
        'name': '⚙️ Kỹ thuật',
        'description': 'Chuyên cho tài liệu kỹ thuật, IT',
        'system_prompt': 'Bạn là một dịch giả chuyên về kỹ thuật và công nghệ. Dịch chính xác các thuật ngữ kỹ thuật, giữ nguyên code, commands và technical terms khi cần.',
        'temperature': 0.2
    }
}

# Supported languages
SUPPORTED_LANGUAGES = {
    'vi': '🇻🇳 Tiếng Việt',
    'en': '🇬🇧 English',
    'zh': '🇨🇳 中文',
    'ja': '🇯🇵 日本語',
    'ko': '🇰🇷 한국어',
    'fr': '🇫🇷 Français',
    'de': '🇩🇪 Deutsch',
    'es': '🇪🇸 Español',
    'ru': '🇷🇺 Русский',
    'th': '🇹🇭 ไทย'
}

# Initialize Z.AI client
zai_client: Optional[ZaiClient] = None

def initialize_zai_client():
    """Initialize Z.AI client with error handling"""
    global zai_client
    try:
        if Config.ZAI_API_KEY:
            zai_client = ZaiClient(api_key=Config.ZAI_API_KEY)
            logger.info("✅ Z.AI client initialized successfully")
        else:
            logger.error("❌ Z.AI API key not configured")
    except Exception as e:
        logger.error(f"❌ Failed to initialize Z.AI client: {e}")
        zai_client = None

def get_user_prefs(user_id: int) -> Dict[str, Any]:
    """Get or create user preferences"""
    if user_id not in user_preferences:
        user_preferences[user_id] = DEFAULT_PREFERENCES.copy()
    return user_preferences[user_id]

def update_user_stats(user_id: int, action: str):
    """Update user statistics"""
    if not Config.ENABLE_STATS:
        return
        
    if user_id not in user_statistics:
        user_statistics[user_id] = {
            'translations': 0,
            'commands': 0,
            'first_use': datetime.now().isoformat(),
            'last_use': datetime.now().isoformat()
        }
    
    stats = user_statistics[user_id]
    if action == 'translation':
        stats['translations'] += 1
    elif action == 'command':
        stats['commands'] += 1
    stats['last_use'] = datetime.now().isoformat()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message when /start is issued"""
    user = update.effective_user
    update_user_stats(user.id, 'command')
    
    welcome_text = (
        f"🌐 *Xin chào {user.first_name}! Chào mừng đến với Bot Dịch Thuật*\n\n"
        "🤖 *Tôi có thể:*\n"
        "• Dịch văn bản sang nhiều ngôn ngữ\n"
        "• Giữ nguyên format văn bản\n"
        "• Hỗ trợ nhiều phong cách dịch\n\n"
        "📝 *Cách sử dụng:*\n"
        "Gửi văn bản → Nhận bản dịch ngay lập tức\n\n"
        "⚙️ *Lệnh hữu ích:*\n"
        "/style - Chọn phong cách dịch\n"
        "/language - Chọn ngôn ngữ đích\n"
        "/settings - Tùy chỉnh cài đặt\n"
        "/stats - Xem thống kê sử dụng\n"
        "/help - Hướng dẫn chi tiết\n\n"
        "💡 _Gửi văn bản bất kỳ để bắt đầu dịch!_"
    )
    
    keyboard = [
        [InlineKeyboardButton("🎨 Chọn phong cách", callback_data="menu_style")],
        [InlineKeyboardButton("🌍 Chọn ngôn ngữ", callback_data="menu_language")],
        [InlineKeyboardButton("📚 Hướng dẫn", callback_data="menu_help")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_text,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show comprehensive help"""
    update_user_stats(update.effective_user.id, 'command')
    
    help_text = (
        "📚 *HƯỚNG DẪN SỬ DỤNG CHI TIẾT*\n\n"
        "🔹 *Tính năng chính:*\n"
        "• Dịch đa ngôn ngữ với AI tiên tiến\n"
        "• Giữ nguyên format (bold, italic, code...)\n"
        "• 5 phong cách dịch chuyên biệt\n"
        "• Tùy chỉnh độ sáng tạo (temperature)\n"
        "• Thống kê sử dụng cá nhân\n\n"
        "🔹 *Các lệnh:*\n"
        "`/start` - Khởi động bot\n"
        "`/style` - Chọn phong cách dịch\n"
        "`/language` - Chọn ngôn ngữ đích\n"
        "`/settings` - Cài đặt cá nhân\n"
        "`/temp [0.1-1.0]` - Điều chỉnh độ sáng tạo\n"
        "`/stats` - Xem thống kê\n"
        "`/reset` - Đặt lại cài đặt mặc định\n"
        "`/about` - Thông tin bot\n\n"
        "🔹 *Phong cách dịch:*\n"
        "💼 Chuyên nghiệp - Trang trọng, chính xác\n"
        "😊 Thân thiện - Tự nhiên, dễ hiểu\n"
        "🎓 Học thuật - Chính xác cao\n"
        "🎨 Sáng tạo - Linh hoạt, hay\n"
        "⚙️ Kỹ thuật - Cho tài liệu IT\n\n"
        "💡 *Mẹo:*\n"
        "• Có thể gửi văn bản dài (max 4000 ký tự)\n"
        "• Hỗ trợ Markdown format\n"
        "• Chọn phong cách phù hợp nội dung\n\n"
        "🔗 *Liên kết:*\n"
        "[Z.AI Platform](https://z.ai) | [Telegram Bot API](https://core.telegram.org/bots)"
    )
    
    await update.message.reply_text(
        help_text,
        parse_mode='Markdown',
        disable_web_page_preview=True
    )

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show about information"""
    update_user_stats(update.effective_user.id, 'command')
    
    about_text = (
        "🤖 *TELEGRAM TRANSLATOR BOT*\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "📌 *Version:* 2.0 Open Source\n"
        "🧠 *AI Model:* GLM-4.5-Flash (Z.AI)\n"
        "⚡ *Framework:* Python + python-telegram-bot\n"
        "📄 *License:* MIT\n\n"
        "✨ *Features:*\n"
        "• Multi-language translation\n"
        "• Format preservation\n"
        "• Multiple translation styles\n"
        "• User preferences\n"
        "• Usage statistics\n\n"
        "🛠️ *Tech Stack:*\n"
        "• Python 3.8+\n"
        "• Z.AI SDK\n"
        "• Telegram Bot API\n"
        "• Async/await architecture\n\n"
        "👨‍💻 *Developer:* Bo\n"
        "📧 *Contact:* @your_username\n"
        "🌟 *GitHub:* [Source Code](https://github.com/...)\n\n"
        "_Open source translation bot for everyone_"
    )
    
    await update.message.reply_text(
        about_text,
        parse_mode='Markdown',
        disable_web_page_preview=True
    )

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user statistics"""
    user_id = update.effective_user.id
    update_user_stats(user_id, 'command')
    
    if not Config.ENABLE_STATS:
        await update.message.reply_text(
            "📊 Thống kê đã bị tắt bởi admin."
        )
        return
    
    if user_id not in user_statistics:
        await update.message.reply_text(
            "📊 Bạn chưa có thống kê nào. Hãy bắt đầu dịch!"
        )
        return
    
    stats = user_statistics[user_id]
    prefs = get_user_prefs(user_id)
    
    stats_text = (
        "📊 *THỐNG KÊ SỬ DỤNG CỦA BẠN*\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"📝 *Số lần dịch:* {stats['translations']}\n"
        f"⚡ *Lệnh đã dùng:* {stats['commands']}\n"
        f"🎨 *Phong cách hiện tại:* {TRANSLATION_STYLES[prefs['style']]['name']}\n"
        f"🌍 *Ngôn ngữ đích:* {SUPPORTED_LANGUAGES.get(prefs['target_language'], 'Unknown')}\n"
        f"📅 *Lần đầu sử dụng:* {stats['first_use'][:10]}\n"
        f"🕒 *Lần cuối sử dụng:* {stats['last_use'][:10]}\n\n"
        "_Cảm ơn bạn đã sử dụng bot!_"
    )
    
    await update.message.reply_text(
        stats_text,
        parse_mode='Markdown'
    )

async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Reset user preferences to default"""
    user_id = update.effective_user.id
    update_user_stats(user_id, 'command')
    
    user_preferences[user_id] = DEFAULT_PREFERENCES.copy()
    
    await update.message.reply_text(
        "🔄 *Đã đặt lại cài đặt mặc định!*\n\n"
        "Tất cả tùy chỉnh của bạn đã được khôi phục về mặc định.",
        parse_mode='Markdown'
    )

async def language_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show language selection menu"""
    user_id = update.effective_user.id
    update_user_stats(user_id, 'command')
    current_lang = get_user_prefs(user_id)['target_language']
    
    keyboard = []
    for lang_code, lang_name in SUPPORTED_LANGUAGES.items():
        check = "✅" if lang_code == current_lang else ""
        button_text = f"{check} {lang_name}"
        keyboard.append([InlineKeyboardButton(
            button_text,
            callback_data=f"lang_{lang_code}"
        )])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🌍 *Chọn ngôn ngữ đích cho bản dịch:*\n\n"
        "_Ngôn ngữ này sẽ được sử dụng cho tất cả bản dịch_",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def style_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show style selection menu"""
    user_id = update.effective_user.id
    update_user_stats(user_id, 'command')
    current_style = get_user_prefs(user_id)['style']
    
    keyboard = []
    for style_key, style_info in TRANSLATION_STYLES.items():
        check = "✅" if style_key == current_style else ""
        button_text = f"{check} {style_info['name']}"
        keyboard.append([InlineKeyboardButton(
            button_text,
            callback_data=f"style_{style_key}"
        )])
    
    keyboard.append([InlineKeyboardButton("ℹ️ Chi tiết phong cách", callback_data="style_info")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🎨 *Chọn phong cách dịch:*\n\n"
        "_Mỗi phong cách có cách diễn đạt riêng phù hợp với từng loại nội dung_",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show settings menu"""
    user_id = update.effective_user.id
    update_user_stats(user_id, 'command')
    prefs = get_user_prefs(user_id)
    
    style_name = TRANSLATION_STYLES[prefs['style']]['name']
    lang_name = SUPPORTED_LANGUAGES.get(prefs['target_language'], 'Unknown')
    
    settings_text = (
        "⚙️ *CÀI ĐẶT HIỆN TẠI*\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🎨 *Phong cách:* {style_name}\n"
        f"🌍 *Ngôn ngữ đích:* {lang_name}\n"
        f"🌡️ *Độ sáng tạo:* {prefs['temperature']}\n"
        f"📝 *Giữ format:* {'✅ Có' if prefs['format_preserve'] else '❌ Không'}\n"
        f"📌 *Thêm ghi chú:* {'✅ Có' if prefs['add_notes'] else '❌ Không'}\n"
        f"👁️ *Hiện bản gốc:* {'✅ Có' if prefs['show_original'] else '❌ Không'}\n\n"
        "_Dùng các nút bên dưới để thay đổi_"
    )
    
    keyboard = [
        [
            InlineKeyboardButton(
                f"📝 Format: {'Bật' if prefs['format_preserve'] else 'Tắt'}",
                callback_data="toggle_format"
            ),
            InlineKeyboardButton(
                f"📌 Ghi chú: {'Bật' if prefs['add_notes'] else 'Tắt'}",
                callback_data="toggle_notes"
            )
        ],
        [
            InlineKeyboardButton(
                f"👁️ Bản gốc: {'Bật' if prefs['show_original'] else 'Tắt'}",
                callback_data="toggle_original"
            )
        ],
        [
            InlineKeyboardButton("🎨 Đổi phong cách", callback_data="menu_style"),
            InlineKeyboardButton("🌍 Đổi ngôn ngữ", callback_data="menu_language")
        ],
        [
            InlineKeyboardButton("🔄 Đặt lại mặc định", callback_data="reset_settings")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        settings_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def temp_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Adjust temperature/creativity"""
    user_id = update.effective_user.id
    update_user_stats(user_id, 'command')
    
    if not context.args:
        current_temp = get_user_prefs(user_id)['temperature']
        await update.message.reply_text(
            "🌡️ *ĐIỀU CHỈNH ĐỘ SÁNG TẠO*\n\n"
            "📊 *Cách dùng:* `/temp <giá trị>`\n"
            "📏 *Phạm vi:* 0.1 - 1.0\n\n"
            "🎯 *Hướng dẫn:*\n"
            "• `0.1-0.3` - Dịch sát nghĩa, ít sáng tạo\n"
            "• `0.4-0.6` - Cân bằng tốt\n"
            "• `0.7-1.0` - Sáng tạo, linh hoạt cao\n\n"
            f"📍 *Giá trị hiện tại:* `{current_temp}`\n\n"
            "_Ví dụ: /temp 0.5_",
            parse_mode='Markdown'
        )
        return
    
    try:
        temp = float(context.args[0])
        if 0.1 <= temp <= 1.0:
            prefs = get_user_prefs(user_id)
            prefs['temperature'] = round(temp, 1)
            await update.message.reply_text(
                f"✅ Đã điều chỉnh độ sáng tạo: *{temp}*\n\n"
                f"_Áp dụng cho các bản dịch tiếp theo_",
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(
                "⚠️ Giá trị phải từ 0.1 đến 1.0"
            )
    except ValueError:
        await update.message.reply_text(
            "⚠️ Vui lòng nhập số hợp lệ (0.1 - 1.0)"
        )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle all button callbacks"""
    query = update.callback_query
    user_id = update.effective_user.id
    
    await query.answer()
    
    # Style selection
    if query.data.startswith("style_"):
        if query.data == "style_info":
            info_text = "📖 *CHI TIẾT CÁC PHONG CÁCH DỊCH*\n\n"
            for style_key, style_info in TRANSLATION_STYLES.items():
                info_text += f"{style_info['name']}\n"
                info_text += f"_{style_info['description']}_\n\n"
            
            await query.edit_message_text(
                info_text,
                parse_mode='Markdown'
            )
        else:
            style = query.data.replace("style_", "")
            prefs = get_user_prefs(user_id)
            prefs['style'] = style
            
            style_name = TRANSLATION_STYLES[style]['name']
            await query.edit_message_text(
                f"✅ Đã chọn phong cách: *{style_name}*\n\n"
                f"_{TRANSLATION_STYLES[style]['description']}_",
                parse_mode='Markdown'
            )
    
    # Language selection
    elif query.data.startswith("lang_"):
        lang = query.data.replace("lang_", "")
        prefs = get_user_prefs(user_id)
        prefs['target_language'] = lang
        
        lang_name = SUPPORTED_LANGUAGES[lang]
        await query.edit_message_text(
            f"✅ Đã chọn ngôn ngữ đích: *{lang_name}*",
            parse_mode='Markdown'
        )
    
    # Toggle settings
    elif query.data == "toggle_format":
        prefs = get_user_prefs(user_id)
        prefs['format_preserve'] = not prefs['format_preserve']
        status = "Bật" if prefs['format_preserve'] else "Tắt"
        await query.answer(f"Giữ format: {status}")
        await settings_command(update, context)
    
    elif query.data == "toggle_notes":
        prefs = get_user_prefs(user_id)
        prefs['add_notes'] = not prefs['add_notes']
        status = "Bật" if prefs['add_notes'] else "Tắt"
        await query.answer(f"Thêm ghi chú: {status}")
        await settings_command(update, context)
    
    elif query.data == "toggle_original":
        prefs = get_user_prefs(user_id)
        prefs['show_original'] = not prefs['show_original']
        status = "Bật" if prefs['show_original'] else "Tắt"
        await query.answer(f"Hiện bản gốc: {status}")
        await settings_command(update, context)
    
    # Menu navigation
    elif query.data == "menu_style":
        await style_command(update, context)
    
    elif query.data == "menu_language":
        await language_command(update, context)
    
    elif query.data == "menu_help":
        await help_command(update, context)
    
    elif query.data == "reset_settings":
        user_preferences[user_id] = DEFAULT_PREFERENCES.copy()
        await query.edit_message_text(
            "🔄 *Đã đặt lại cài đặt mặc định!*",
            parse_mode='Markdown'
        )

async def translate_text(text: str, user_id: int) -> tuple[str, bool]:
    """
    Translate text using Z.AI SDK
    Returns: (translated_text, success)
    """
    if not zai_client:
        return "❌ Z.AI client chưa được khởi tạo. Kiểm tra API key!", False
    
    prefs = get_user_prefs(user_id)
    style = TRANSLATION_STYLES[prefs['style']]
    target_lang = SUPPORTED_LANGUAGES.get(prefs['target_language'], 'Tiếng Việt')
    
    # Build prompt
    prompt_parts = [f"Translate the following text to {target_lang}."]
    
    if prefs['format_preserve']:
        prompt_parts.append("Preserve all formatting (bold, italic, line breaks, bullet points, etc.).")
    
    if prefs['add_notes']:
        prompt_parts.append("Add brief explanatory notes in parentheses for difficult terms if needed.")
    
    prompt_parts.append("Return only the translation without any additional explanation.")
    prompt_parts.append(f"\nText to translate:\n{text}")
    
    prompt = " ".join(prompt_parts)
    
    try:
        response = zai_client.chat.completions.create(
            model="glm-4.5-flash",
            messages=[
                {
                    "role": "system",
                    "content": style['system_prompt']
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=prefs['temperature'],
            max_tokens=Config.MAX_MESSAGE_LENGTH
        )
        
        translated_text = response.choices[0].message.content
        return translated_text, True
    except Exception as e:
        logger.error(f"Translation error for user {user_id}: {str(e)}")
        return f"❌ Lỗi khi dịch: {str(e)}", False

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming messages for translation"""
    user_text = update.message.text
    user_id = update.effective_user.id
    
    # Check message length
    if len(user_text) > Config.MAX_MESSAGE_LENGTH:
        await update.message.reply_text(
            f"⚠️ Văn bản quá dài! Tối đa {Config.MAX_MESSAGE_LENGTH} ký tự.\n"
            f"Văn bản của bạn: {len(user_text)} ký tự.",
            parse_mode='Markdown'
        )
        return
    
    # Log and update stats
    logger.info(f"User {user_id} ({update.effective_user.username}): {user_text[:50]}...")
    update_user_stats(user_id, 'translation')
    
    # Send processing message
    processing_msg = await update.message.reply_text(
        "🔄 *Đang dịch...*",
        parse_mode='Markdown'
    )
    
    # Send typing action
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action="typing"
    )
    
    # Translate
    translated, success = await translate_text(user_text, user_id)
    
    # Format response
    prefs = get_user_prefs(user_id)
    style_emoji = TRANSLATION_STYLES[prefs['style']]['name'].split()[0]
    lang_emoji = SUPPORTED_LANGUAGES[prefs['target_language']].split()[0]
    
    if success:
        response_parts = [
            f"{style_emoji} *Phong cách:* {TRANSLATION_STYLES[prefs['style']]['name']}",
            f"{lang_emoji} *Ngôn ngữ:* {SUPPORTED_LANGUAGES[prefs['target_language']]}",
            "━━━━━━━━━━━━━━━━━━━━",
            translated
        ]
        
        if prefs['show_original']:
            response_parts.extend([
                "\n━━━━━━━━━━━━━━━━━━━━",
                "📄 *Bản gốc:*",
                f"_{user_text}_"
            ])
        
        response = "\n".join(response_parts)
    else:
        response = translated  # Error message
    
    # Delete processing message and send result
    try:
        await processing_msg.delete()
    except:
        pass
    
    await update.message.reply_text(
        response,
        parse_mode='Markdown'
    )
    
    logger.info(f"Translation {'succeeded' if success else 'failed'} for user {user_id}")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    logger.error(f"Update {update} caused error: {context.error}")
    
    if update and update.message:
        error_message = (
            "❌ *Đã xảy ra lỗi!*\n\n"
            "Vui lòng thử lại sau hoặc liên hệ admin.\n"
            "Sử dụng /help để xem hướng dẫn."
        )
        
        try:
            await update.message.reply_text(
                error_message,
                parse_mode='Markdown'
            )
        except:
            pass

async def main():
    """Main function to run the bot"""
    print(BANNER)
    
    # Validate configuration
    is_valid, message = Config.validate()
    print(message)
    
    if not is_valid:
        print("\n⚠️  Configuration Error!")
        print("Please create a .env file with:")
        print("TELEGRAM_TOKEN=your_telegram_bot_token")
        print("ZAI_API_KEY=your_zai_api_key")
        print("\nRefer to README.md for detailed setup instructions.")
        sys.exit(1)
    
    # Initialize Z.AI client
    initialize_zai_client()
    
    if not zai_client:
        print("❌ Failed to initialize Z.AI client. Check your API key.")
        sys.exit(1)
    
    # Create application
    print("🚀 Starting Telegram bot...")
    application = Application.builder().token(Config.TELEGRAM_TOKEN).build()
    
    # Initialize application
    await application.initialize()
    
    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))
    application.add_handler(CommandHandler("style", style_command))
    application.add_handler(CommandHandler("language", language_command))
    application.add_handler(CommandHandler("settings", settings_command))
    application.add_handler(CommandHandler("temp", temp_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("reset", reset_command))
    
    # Register callback handler
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Register message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Register error handler
    application.add_error_handler(error_handler)
    
    # Start bot
    await application.start()
    await application.updater.start_polling(allowed_updates=Update.ALL_TYPES)
    
    print("✅ Bot is running! Press Ctrl+C to stop.")
    print(f"🤖 Bot username: @{(await application.bot.get_me()).username}")
    print("━" * 50)
    
    # Keep running
    try:
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down bot...")
    finally:
        await application.stop()
        print("👋 Bot stopped. Goodbye!")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Bot terminated by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)