# 🌐 Telegram Translator Bot - Open Source Version

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Telegram Bot API](https://img.shields.io/badge/Telegram%20Bot%20API-Latest-blue)](https://core.telegram.org/bots)
[![Z.AI](https://img.shields.io/badge/Powered%20by-Z.AI%20GLM--4.5--Flash-purple)](https://z.ai)

A powerful, feature-rich Telegram bot for instant multi-language translation using Z.AI's advanced GLM-4.5-Flash model.

## ✨ Features

### Core Features
- 🌍 **Multi-language Translation** - Support for 10+ languages
- 📝 **Format Preservation** - Maintains bold, italic, code blocks, lists
- 🎨 **5 Translation Styles** - Professional, Casual, Academic, Creative, Technical
- ⚙️ **Customizable Settings** - Temperature, notes, format options
- 📊 **Usage Statistics** - Track your translation history
- 🔄 **Real-time Processing** - Instant translations with typing indicators

### Advanced Features
- 💾 User preference persistence
- 🌡️ Adjustable creativity (temperature)
- 📌 Optional explanatory notes
- 👁️ Show original text option
- 🔧 Admin controls
- 📈 Performance monitoring

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Telegram Bot Token
- Z.AI API Key

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/telegram-translator-bot.git
cd telegram-translator-bot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

Or use the setup script:
```bash
python setup.py install
```

### 3. Configure API Keys

#### Step 1: Get Telegram Bot Token
1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` and follow instructions
3. Copy your bot token (format: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

#### Step 2: Get Z.AI API Key
1. Visit [Z.AI Platform](https://z.ai)
2. Sign up or log in to your account
3. Go to Dashboard → API Keys
4. Create a new API key and copy it

#### Step 3: Create Configuration File
```bash
# Copy the example file
cp .env.example .env

# Edit .env with your favorite editor
nano .env  # or vim, code, etc.
```

Add your keys to `.env`:
```env
TELEGRAM_TOKEN=your_telegram_bot_token_here
ZAI_API_KEY=your_zai_api_key_here
```

### 4. Run the Bot
```bash
python telegram_translator_bot.py
```

You should see:
```
╔══════════════════════════════════════════════════════╗
║     🌐 TELEGRAM TRANSLATOR BOT - OPEN SOURCE 🌐      ║
║           Powered by Z.AI GLM-4.5-Flash              ║
╚══════════════════════════════════════════════════════╝
✅ Configuration validated successfully
🚀 Starting Telegram bot...
✅ Bot is running! Press Ctrl+C to stop.
🤖 Bot username: @your_bot_name
```

## 📖 Usage Guide

### Basic Commands
| Command | Description |
|---------|-------------|
| `/start` | Start the bot and see welcome message |
| `/help` | Show detailed help information |
| `/style` | Choose translation style |
| `/language` | Select target language |
| `/settings` | View and modify settings |
| `/temp [0.1-1.0]` | Adjust creativity level |
| `/stats` | View your usage statistics |
| `/reset` | Reset to default settings |
| `/about` | Bot information |

### Translation Styles
- 💼 **Professional** - Formal, accurate terminology
- 😊 **Casual** - Natural, easy to understand
- 🎓 **Academic** - High precision, preserves technical terms
- 🎨 **Creative** - Flexible, captures spirit of text
- ⚙️ **Technical** - For IT documentation and code

### Supported Languages
- 🇻🇳 Vietnamese (vi)
- 🇬🇧 English (en)
- 🇨🇳 Chinese (zh)
- 🇯🇵 Japanese (ja)
- 🇰🇷 Korean (ko)
- 🇫🇷 French (fr)
- 🇩🇪 German (de)
- 🇪🇸 Spanish (es)
- 🇷🇺 Russian (ru)
- 🇹🇭 Thai (th)

## ⚙️ Configuration

### Environment Variables
Create a `.env` file based on `.env.example`:

```env
# Required
TELEGRAM_TOKEN=your_token_here
ZAI_API_KEY=your_api_key_here

# Optional
MAX_MESSAGE_LENGTH=4000
DEFAULT_LANGUAGE=vi
ENABLE_STATS=true
ADMIN_USER_ID=your_telegram_id
LOG_LEVEL=INFO
```

### Advanced Configuration
Edit settings in `telegram_translator_bot.py`:
- Modify `TRANSLATION_STYLES` for custom styles
- Add languages to `SUPPORTED_LANGUAGES`
- Adjust `DEFAULT_PREFERENCES`

## 🛠️ Development

### Project Structure
```
telegram-translator-bot/
├── telegram_translator_bot.py  # Main bot file
├── requirements.txt            # Python dependencies
├── .env.example               # Configuration template
├── .env                       # Your configuration (git ignored)
├── README.md                  # This file
├── LICENSE                    # MIT License
└── setup.py                   # Installation script
```

### Running in Development Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
python telegram_translator_bot.py
```

### Docker Support (Optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "telegram_translator_bot.py"]
```

Build and run:
```bash
docker build -t telegram-translator .
docker run --env-file .env telegram-translator
```

## 🔧 Troubleshooting

### Common Issues

#### Bot doesn't respond
- Check if bot token is correct
- Ensure bot is not already running elsewhere
- Verify internet connection

#### Translation errors
- Verify Z.AI API key is valid
- Check API quota/limits
- Ensure model name is correct (`glm-4.5-flash`)

#### Configuration not found
- Make sure `.env` file exists
- Check file permissions
- Verify environment variable names

### Debug Mode
Enable debug logging:
```bash
export LOG_LEVEL=DEBUG
python telegram_translator_bot.py
```

## 📊 API Limits & Pricing

### Z.AI API
- Model: GLM-4.5-Flash
- Max tokens per request: 4000
- Rate limits apply based on your plan
- Visit [Z.AI Pricing](https://z.ai/pricing) for details

### Telegram Bot API
- No cost for bot usage
- Rate limits: 30 messages/second
- File size limits apply

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Z.AI](https://z.ai) for the powerful GLM-4.5-Flash model
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) for the excellent library
- Community contributors

## 📞 Support

- Create an issue on GitHub
- Contact: @your_username on Telegram
- Email: your.email@example.com

## 🚦 Status

![Bot Status](https://img.shields.io/badge/Status-Active-success)
![Version](https://img.shields.io/badge/Version-2.0-blue)
![Maintained](https://img.shields.io/badge/Maintained-Yes-green)

---

**Made with ❤️ by Bo**

*Happy Translating! 🌐*