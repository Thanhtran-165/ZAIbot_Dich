# Bot Telegram Dịch Thuật

Bot Telegram tự động dịch văn bản sang tiếng Việt sử dụng Z.AI API.

## Tính năng
- Dịch tự động mọi tin nhắn sang tiếng Việt
- Giữ nguyên format văn bản (in đậm, in nghiêng, xuống dòng, v.v.)
- Sử dụng mô hình GPT-4.5 Flash của Z.AI

## Cài đặt

1. **Cài đặt các thư viện cần thiết:**
```bash
pip install -r requirements.txt
```

2. **Chạy bot:**
```bash
python telegram_bot.py
```

## Sử dụng

1. Tìm bot trên Telegram bằng token đã cung cấp
2. Gửi lệnh `/start` để bắt đầu
3. Gửi bất kỳ văn bản nào cần dịch
4. Bot sẽ tự động dịch và gửi lại bản dịch tiếng Việt

## Lưu ý
- Bot giữ nguyên format của văn bản gốc
- Hỗ trợ Markdown trong tin nhắn
- API keys đã được cấu hình sẵn trong file .env