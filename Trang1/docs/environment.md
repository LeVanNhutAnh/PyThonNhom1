## 4.1. Môi trường phát triển và công cụ

### 4.1.1. Cấu hình hệ thống

Để đảm bảo quá trình phát triển và kiểm thử diễn ra ổn định, hệ thống được triển khai trên máy tính cá nhân với cấu hình phần cứng và phần mềm như sau:

- Hệ điều hành: Windows 10 hoặc Windows 11
- Bộ nhớ RAM: Tối thiểu 8GB (khuyến nghị 16GB để xử lý tốt các tác vụ AI)
- Vi xử lý: Intel Core i5 thế hệ thứ 8 trở lên
- Ổ cứng: SSD dung lượng tối thiểu 10GB để đảm bảo tốc độ truy xuất dữ liệu nhanh

Môi trường làm việc:

- Thư mục dự án: `D:\WebCGNTVB&AI\Trang1`
- Công cụ lập trình chính: Visual Studio Code phiên bản 1.85 trở lên, hỗ trợ các tiện ích mở rộng như Python, Django, Prettier và GitLens

### 4.1.2. Công nghệ sử dụng

Hệ thống được xây dựng dựa trên mô hình kiến trúc ba lớp (MVT – Model, View, Template) của Django, kết hợp với các công nghệ web hiện đại để đảm bảo tính tương tác và hiệu suất.

Phía máy chủ (Backend):

- Ngôn ngữ lập trình: Python 3.13.7
- Framework: Django 5.2.6 – sử dụng kiến trúc MVT để tách biệt logic, giao diện và dữ liệu
- Cơ sở dữ liệu: SQLite3 – phù hợp với ứng dụng quy mô nhỏ và dễ triển khai

Phía trình duyệt (Frontend):

- Ngôn ngữ và công nghệ: HTML5, CSS3, JavaScript ES6+

Tính năng nổi bật:

- Giao diện tương tác theo phong cách ChatGPT
- Thiết kế responsive, tương thích với nhiều thiết bị
- Tích hợp Web Speech API để hỗ trợ ghi âm và chuyển giọng nói thành văn bản theo thời gian thực

---

## Hướng dẫn tích hợp Web Speech API (ghi âm & Speech-to-Text)

Tài liệu này mô tả cách Web Speech API được tích hợp vào giao diện `home.html` để hỗ trợ ghi âm và chuyển giọng nói thành văn bản theo thời gian thực, cùng các lưu ý cần thiết khi triển khai.

1) Kiến trúc & ý tưởng

- Tính năng chính hoạt động hoàn toàn ở phía client (trình duyệt) sử dụng Web Speech API (`SpeechRecognition` / `webkitSpeechRecognition`) để nhận diện giọng nói theo thời gian thực (interim + final results).
- Khi trình duyệt không hỗ trợ Web Speech API (ví dụ: một số phiên bản Firefox hoặc các trình duyệt không phải Chromium), ứng dụng chứa fallback dùng `MediaRecorder` để ghi audio và gửi file audio lên endpoint server (ví dụ: `/whisper-transcribe/`) để xử lý bằng mô hình Whisper hoặc dịch vụ tương đương.

2) Yêu cầu trình duyệt và bảo mật

- Web Speech API (SpeechRecognition) hiện được hỗ trợ tốt trên trình duyệt Chromium (Chrome/Edge) trên desktop; trên mobile hỗ trợ khác nhau tùy phiên bản.
- Trình duyệt thường yêu cầu kết nối an toàn (HTTPS) để truy cập micro; localhost được coi là ngoại lệ (cho phát triển cục bộ).
- Người dùng phải cho phép quyền truy cập micro; ứng dụng phải xử lý lỗi quyền và cung cấp hướng dẫn rõ ràng.

3) Các thành phần chính đã có trong `templates/home.html`

- Giao diện: nút micro (`#micBtn`), textarea (`#messageInput`), và các toggle trong Cài đặt để bật/tắt ghi âm liên tục (`continuous`) và tự động gửi (`autoSend`).
- Logic JS: lớp `AIAssistant` đã chứa:
  - Khởi tạo `SpeechRecognition` (nếu có) với `continuous` và `interimResults`.
  - `onresult` để cập nhật transcript tạm thời vào textarea và gửi tự động khi là kết quả cuối nếu `autoSend` bật.
  - Fallback với `MediaRecorder` và gửi audio blob đến endpoint `/whisper-transcribe/`.
  - Chức năng xử lý lỗi, thông báo và trạng thái (recording/stop).

4) Endpoint server cần có (tùy lựa chọn triển khai)

- `/ai-chat/` — endpoint POST để gửi text và nhận phản hồi AI (đã tham chiếu trong mã client).
- `/whisper-transcribe/` — endpoint POST (FormData: audio file + language) để server chạy Whisper hoặc dịch vụ chuyển speech->text và trả về JSON { transcription: string }.

5) Cách kiểm thử nhanh (local)

- Chạy server Django: `python manage.py runserver`
- Mở trình duyệt Chrome (phiên bản mới) đến `http://127.0.0.1:8000/` (hoặc `localhost`) để dùng micro mà không cần HTTPS.
- Khi bấm micro lần đầu, cho phép truy cập micro khi trình duyệt hỏi. Kiểm tra:
  - Transcript hiện trong textarea theo thời gian thực (interim results).
  - Nếu bật `Tự động gửi`, tin nhắn được gửi khi kết quả cuối cùng ghi nhận.
  - Nếu trình duyệt không hỗ trợ SpeechRecognition, thử bấm micro để sử dụng fallback (ghi audio và gửi lên `/whisper-transcribe/`).

6) Hạn chế & lưu ý

- Chính xác phụ thuộc vào engine: Web Speech API của trình duyệt có thể hoạt động tốt nhưng hạn chế độ chính xác so với mô hình chuyên sâu (ví dụ Whisper hoặc cloud STT). Nên cung cấp tùy chọn server-side transcription cho kết quả tốt hơn khi cần.
- Việc gửi audio lên server tiêu tốn băng thông và có yêu cầu về xử lý/chi phí (nếu dùng cloud).
- Trường hợp cần độ riêng tư cao, cần thông báo rõ người dùng về việc gửi audio đến server và có lựa chọn tắt upload.

7) Gợi ý cải tiến

- Thêm indicator hiển thị trạng thái mạng khi gửi audio/fallback.
- Lưu transcript tạm thời vào localStorage để tránh mất khi tải lại.
- Hỗ trợ chọn input device (nhiều mic) trong Settings.
- Nếu dùng OpenAI/Whisper, thêm queue và retry logic cho yêu cầu ngoại vi.

---

Tôi đã thêm file này vào `Trang1/docs/environment.md`. Nếu bạn muốn, tôi có thể:

- Chèn hành lang mô tả ngắn gọn (test steps) trực tiếp vào `templates/home.html` như comment cho người vận hành.
- Tạo endpoint demo `/whisper-transcribe/` đơn giản trong Django views để thử nghiệm (yêu cầu quyết định triển khai: local Whisper binary, Docker, hoặc cloud API).

Hãy cho biết bạn muốn tôi tiếp tục với phần nào (ví dụ: tạo view server-side demo cho Whisper, hoặc thêm README test steps vào `home.html`).
