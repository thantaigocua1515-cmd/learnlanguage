# Data Sources & Open License Attributions (Ghi nhận nguồn dữ liệu & Giấy phép mở)

Dự án **LingoLearning** tuân thủ nghiêm ngặt các quy định về sở hữu trí tuệ và giấy phép nguồn mở (Open Source Data Licenses) đối với 3 nguồn dữ liệu học thuật:

---

### 1. DWDS & Goethe-Institut (Khung cấp độ CEFR A1, A2, B1)
- **Nguồn:** [Digitales Wörterbuch der deutschen Sprache (DWDS)](https://www.dwds.de/) hợp tác cùng **Goethe-Institut**.
- **Dữ liệu trích xuất:** Danh mục từ vựng chuẩn hóa (`Lemma`), phân loại từ loại (`Wortart`), giống ngữ pháp (`Genus`), và mạo từ (`Artikel`).
- **Cam kết bản quyền:** Dự án chỉ sử dụng danh sách từ vựng và khung cấp độ chuẩn CEFR của Goethe/DWDS phục vụ mục đích phân loại học tập; **tuyệt đối không sao chép** câu ví dụ ngữ cảnh hay bản dịch nguyên văn từ tài liệu có bản quyền của viện Goethe.

---

### 2. Kaikki.org / Wiktionary (Chi tiết từ điển & Biến hình từ vựng)
- **Nguồn:** [Kaikki.org](https://kaikki.org/) trích xuất có cấu trúc từ **German Wiktionary**.
- **Giấy phép:** [Creative Commons Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0)](https://creativecommons.org/licenses/by-sa/3.0/) và GFDL.
- **Dữ liệu trích xuất:**
  - Phiên âm quốc tế chuẩn IPA (`sounds[].ipa`)
  - Bảng chia biến hình từ vựng: số nhiều của danh từ, thì chia động từ (`forms[]`)
  - Định nghĩa tóm tắt tiếng Anh (`senses[].glosses`)
  - Bản dịch tiếng Việt cộng đồng nếu có (`translations[]`)
  - Từ đồng nghĩa (`synonyms[]`)

---

### 3. Tatoeba Project (Câu ví dụ ngữ cảnh & Bản dịch tiếng Việt)
- **Nguồn:** [Tatoeba.org](https://tatoeba.org/) - Cơ sở dữ liệu câu ví dụ và bản dịch đa ngôn ngữ mở.
- **Giấy phép:** [Creative Commons Attribution 2.0 France (CC BY 2.0 FR)](https://creativecommons.org/licenses/by/2.0/fr/).
- **Quy chuẩn ghi nhận tác giả:**
  - Mọi câu ví dụ đều lưu giữ `tatoeba_id`, nguồn `source: "tatoeba"`.
  - Tác giả đóng góp câu tiếng Đức và bản dịch tiếng Việt được ghi nhận theo trường `owner` từ dữ liệu gốc Tatoeba (ví dụ: `Babelball`, `dotheduyet1999`, `Waldelfe`, `leucammieuvu`, v.v.).

