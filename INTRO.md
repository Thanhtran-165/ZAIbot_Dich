# 🌐 Bot Dịch Thuật Telegram - Phiên Bản Mã Nguồn Mở

## 📖 Giới Thiệu

**Telegram Translator Bot** là một bot dịch thuật thông minh, được xây dựng với công nghệ AI tiên tiến từ Z.AI (mô hình GLM-4.5-Flash). Bot có khả năng dịch đa ngôn ngữ với độ chính xác cao, phù hợp cho cả mục đích cá nhân và doanh nghiệp.

### ✨ Điểm Nổi Bật

🚀 **Dịch Tức Thì** - Nhận bản dịch ngay lập tức qua Telegram
🌍 **Đa Ngôn Ngữ** - Hỗ trợ 10+ ngôn ngữ phổ biến
🎨 **5 Phong Cách** - Chuyên nghiệp, Thân thiện, Học thuật, Sáng tạo, Kỹ thuật
📝 **Giữ Format** - Không làm mất định dạng văn bản gốc
⚙️ **Tùy Chỉnh Linh Hoạt** - Điều chỉnh theo nhu cầu của bạn
📊 **Thống Kê Chi Tiết** - Theo dõi lịch sử sử dụng
🔒 **Bảo Mật** - API keys riêng tư, dữ liệu an toàn

### 🎯 Ai Nên Sử Dụng?

- **Sinh viên & Học sinh** - Dịch tài liệu học tập
- **Doanh nghiệp** - Giao tiếp đa ngôn ngữ
- **Developers** - Dịch documentation kỹ thuật
- **Content Creators** - Dịch nội dung sáng tạo
- **Bất kỳ ai** cần dịch thuật nhanh chóng và chính xác

---

## 🚀 Hướng Dẫn Cài Đặt Nhanh

### 📋 Yêu Cầu Hệ Thống
- Python 3.8 trở lên
- Kết nối Internet ổn định
- Tài khoản Telegram

### 🔧 3 Bước Cài Đặt Đơn Giản

#### **Bước 1: Tải Mã Nguồn**
```bash
# Clone từ GitHub (hoặc download ZIP)
git clone https://github.com/yourusername/telegram-translator-bot.git
cd telegram-translator-bot

# Hoặc download và giải nén
unzip telegram-translator-bot.zip
cd telegram-translator-bot
```

#### **Bước 2: Lấy API Keys (QUAN TRỌNG)**

**🤖 Lấy Telegram Bot Token:**
1. Mở Telegram, tìm **@BotFather**
2. Gửi lệnh `/newbot`
3. Đặt tên cho bot (ví dụ: "My Translator")
4. Chọn username (ví dụ: "mytranslator_bot")
5. Copy token nhận được (dạng: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

**🔑 Lấy Z.AI API Key:**
1. Truy cập **[z.ai](https://z.ai)**
2. Đăng ký tài khoản miễn phí
3. Vào **Dashboard → API Keys**
4. Click **"Create New Key"**
5. Copy API key (dạng: `sk-xxxxxxxxxxxxxxxx`)

#### **Bước 3: Chạy Setup Tự Động**
```bash
# Chạy script cài đặt
python setup.py
```

Script sẽ tự động:
- ✅ Kiểm tra Python version
- ✅ Cài đặt thư viện cần thiết
- ✅ Hướng dẫn bạn nhập API keys
- ✅ Tạo file cấu hình
- ✅ Khởi động bot

---

## 💡 Cách Sử Dụng Bot

### 1️⃣ **Khởi Động Bot**
```bash
# Windows
start_bot.bat

# Mac/Linux
./start_bot.sh

# Hoặc chạy trực tiếp
python telegram_translator_bot.py
```

### 2️⃣ **Mở Telegram & Bắt Đầu Chat**
1. Tìm bot của bạn trên Telegram (username bạn đã tạo)
2. Nhấn **START** hoặc gửi `/start`
3. Gửi bất kỳ văn bản nào để dịch

### 3️⃣ **Các Lệnh Hữu Ích**
- `/style` - Chọn phong cách dịch
- `/language` - Chọn ngôn ngữ đích
- `/settings` - Tùy chỉnh cài đặt
- `/help` - Xem hướng dẫn

---

## 🆘 Gặp Vấn Đề?

### ❌ **Lỗi "API key not found"**
→ Kiểm tra file `.env` đã có đúng API keys chưa

### ❌ **Bot không phản hồi**
→ Kiểm tra token Telegram và kết nối mạng

### ❌ **Lỗi cài đặt thư viện**
→ Chạy: `pip install --upgrade pip` rồi thử lại

### 📞 **Cần Hỗ Trợ?**
- Tạo issue trên GitHub
- Email: support@example.com
- Telegram: @support_username

---

## 🎁 Tính Năng Premium (Sắp Ra Mắt)

- 🌟 Dịch file PDF/DOCX
- 🌟 Dịch hình ảnh (OCR)
- 🌟 Dịch voice messages
- 🌟 API cho developers
- 🌟 Dashboard quản lý

---

## 📄 Giấy Phép

Mã nguồn mở theo giấy phép **MIT License** - Bạn có thể tự do sử dụng, chỉnh sửa và phân phối.

---

**🚀 Bắt đầu ngay hôm nay!** Chỉ mất 5 phút để có bot dịch thuật AI của riêng bạn.

*Developed with ❤️ by Bo*