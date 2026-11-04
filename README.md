# LingoLearning - Nền tảng Học Đa Ngôn Ngữ (Bắt đầu với Tiếng Đức 'de')

> **Senior Full-stack Architecture**: Nền tảng web học đa ngôn ngữ chuẩn CEFR (A1 - C2), thiết kế giao diện Gamification hiện đại, kết hợp backend Supabase và nguồn dữ liệu câu mở rộng từ Tatoeba API. Sẵn sàng đóng gói sang ứng dụng di động Android & iOS.

---

## 1. Ràng buộc Công nghệ (Strict Tech Stack)

- **Frontend Core**: HTML5, **Bootstrap 5.3** (qua CDN), **Bootstrap Icons**, Vanilla JavaScript (**ES6 Modules**).
- **Tuyệt đối KHÔNG sử dụng Tailwind CSS**.
- **CSS Tùy chỉnh**: Sử dụng chuẩn CSS Custom Properties (`:root`), hỗ trợ chuyển đổi **Light/Dark Mode**.
- **Quy ước màu sắc Tiếng Đức (German Color Convention)**:
  - 🔵 **Giống đực (`der`)**: `--gender-der: #2563eb` (Xanh dương)
  - 🔴 **Giống cái (`die`)**: `--gender-die: #e11d48` (Đỏ san hô)
  - 🟢 **Giống trung (`das`)**: `--gender-das: #16a34a` (Xanh lục)
- **Hiệu ứng Gamification 3D**: Nút bấm tactile `.btn-3d` có độ lún cơ học khi nhấn, bo góc mềm mại (`--radius-lg: 18px`), thanh năng lượng (Hearts), điểm kinh nghiệm (XP) và chuỗi ngày học liên tục (Streak 🔥).
- **Backend**: **Supabase** (PostgreSQL, Row Level Security - RLS, Auth, Edge Functions, Storage).

---

## 2. Cấu trúc Thư mục Dự án

```
LingoLearning/
├── index.html                  # Giao diện chính Học viên (Dashboard, Cấp độ A1-C2, Mini-Games)
├── admin.html                  # AdminCP chuẩn SaaS (Quản lý từ vựng, Ingest Tatoeba API, Cấu hình)
├── css/
│   ├── variables.css           # CSS Variables (:root, Dark Mode, Quy ước màu der/die/das)
│   ├── main.css                # Base CSS, typography, tactile 3D buttons, badges, mobile nav
│   ├── games.css               # CSS cho 4 Mini-games (Speed Sorter, Scramble, Cloze, Flashcard 3D)
│   └── admin.css               # CSS giao diện SaaS AdminCP
├── js/
│   ├── config.js               # Cấu hình Supabase, Tatoeba OpenAPI, CEFR levels
│   ├── supabaseClient.js       # Client kết nối Supabase và cơ chế fallback Local Store
│   ├── api/
│   │   ├── tatoeba.js          # Module kết nối Tatoeba API (https://api.tatoeba.org/openapi)
│   │   └── dataService.js      # Data Access Layer: CRUD từ vựng, câu mẫu, số liệu thống kê
│   ├── services/
│   │   ├── authService.js      # Quản lý Auth, vai trò Học viên / Admin, XP, Hearts, Streak
│   │   ├── soundService.js     # Web Audio API tạo âm thanh trò chơi và Speech Synthesis (de-DE)
│   │   └── progressService.js  # Thuật toán Spaced Repetition (SRS SuperMemo SM-2)
│   ├── games/
│   │   ├── articleGame.js      # Game 1: Phân loại giống từ Der / Die / Das siêu tốc
│   │   ├── wordScramble.js     # Game 2: Xếp chữ đoán từ với ngữ cảnh Tatoeba
│   │   ├── clozeGame.js        # Game 3: Điền từ vào chỗ trống câu thực tế Tatoeba
│   │   └── flashcards.js       # Game 4: Lật thẻ 3D Spaced Repetition (SRS)
│   ├── app.js                  # Điều khiển luồng ứng dụng phía Học viên
│   └── admin.js                # Điều khiển luồng SaaS AdminCP & Tool quét Tatoeba
└── sql/
    └── schema.sql              # Script khởi tạo Database PostgreSQL + RLS trên Supabase
```

---

## 3. Hướng dẫn Khởi chạy và Trải nghiệm Nhanh

Vì dự án được xây dựng với cấu trúc **Vanilla ES6 Modules** và thư viện qua CDN, bạn có thể chạy ngay bằng bất kỳ web server nhẹ nào:

### Cách 1: Sử dụng npx serve (Khuyên dùng)
```bash
npx serve /home/jikay/Desktop/LingoLearning -p 3000
```
Truy cập:
- **Giao diện Học viên**: `http://localhost:3000/index.html`
- **Giao diện AdminCP**: `http://localhost:3000/admin.html`

### Cách 2: Sử dụng Python
```bash
cd /home/jikay/Desktop/LingoLearning
python3 -m http.server 3000
```

---

## 4. Tích hợp Backend Supabase

1. Đăng nhập vào [Supabase Dashboard](https://supabase.com).
2. Tạo mới một Project.
3. Mở tab **SQL Editor** trong Supabase Dashboard, copy toàn bộ nội dung trong file [sql/schema.sql](file:///home/jikay/Desktop/LingoLearning/sql/schema.sql) và nhấn **Run**.
   - Thiết lập đầy đủ các bảng: `languages`, `cefr_levels`, `topics`, `vocabulary`, `sentences`, `profiles`, `user_word_progress`.
   - Cấu hình sẵn bảo mật Row Level Security (RLS) và Trigger tự động tạo Profile khi người dùng đăng ký.
4. Lấy `Project URL` và `Anon Public Key` từ **Project Settings -> API**.
5. Mở trang **AdminCP -> Cấu hình Supabase** (`admin.html`) và dán thông tin vào form để kích hoạt đồng bộ đám mây trực tiếp.

---

## 5. Tích hợp Tatoeba API & Adapter Mở rộng

Hệ thống kết nối trực tiếp đến **Tatoeba OpenAPI**:
- Route: `https://api.tatoeba.org/unstable/sentences`
- Hỗ trợ tìm kiếm câu mẫu tiếng Đức (`deu`) có bản dịch tiếng Việt (`vie`) hoặc tiếng Anh (`eng`).
- Trích xuất link phát âm giọng bản xứ (`audio_url`).
- **Tatoeba Importer Tool** trong AdminCP cho phép:
  1. Tìm kiếm câu mẫu theo từ khóa thời gian thực.
  2. Nghe thử âm thanh phát âm trước khi lưu.
  3. Gán cấp độ CEFR (A1-C2).
  4. Lưu 1-Click vào hệ thống cơ sở dữ liệu để tự động làm dữ liệu đầu vào cho các Mini-game.

---

## 6. Hướng dẫn Đóng gói Build sang Mobile App (Android & iOS)

Sử dụng **Capacitor.js** để đóng gói toàn bộ thư mục web thành ứng dụng native cho Android (`.apk/.aab`) và iOS (`.ipa`):

```bash
cd /home/jikay/Desktop/LingoLearning

# 1. Khởi tạo npm và cài đặt Capacitor
npm init -y
npm install @capacitor/core @capacitor/cli @capacitor/android @capacitor/ios

# 2. Khởi tạo cấu hình Capacitor
npx cap init LingoLearning com.lingolearning.app --web-dir .

# 3. Thêm nền tảng Android & iOS
npx cap add android
npx cap add ios

# 4. Đồng bộ mã nguồn
npx cap sync

# 5. Mở Android Studio hoặc Xcode để build
npx cap open android
npx cap open ios
```
*Giao diện đã được thiết kế sẵn thanh điều hướng Mobile Bottom Navigation Bar, cảm ứng chạm mượt mà và hỗ trợ đầy đủ màn hình tai thỏ/nốt ruồi.*

