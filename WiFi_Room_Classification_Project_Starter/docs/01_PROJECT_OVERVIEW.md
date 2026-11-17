# 01 — Tổng quan dự án

## Bài toán

Một mẫu dữ liệu chứa 7 cường độ RSSI đo từ 7 nguồn WiFi và nhãn phòng (1–4). Mô hình phân loại học từ những mẫu có nhãn, rồi dự đoán nhãn cho mẫu chưa thấy.

**Đầu vào:** `[WiFi_1, ..., WiFi_7]` (giá trị số, dBm).  
**Đầu ra:** `Room ∈ {1, 2, 3, 4}`.

Ví dụ minh họa (không lấy từ dữ liệu thật): `[-45, -60, -70, -55, -80, -75, -90] -> Room 1`.

## Mục tiêu

- Mô tả dữ liệu và phân bố nhãn.
- Quan sát cấu trúc dữ liệu sau chuẩn hóa/PCA.
- Huấn luyện, tinh chỉnh và đánh giá công bằng 5 mô hình phân loại.
- Kiểm tra khả năng phân cụm tự nhiên bằng K-Means và DBSCAN.
- Phân tích lỗi và giới hạn của mô hình.

## Câu hỏi cần trả lời trong báo cáo

- Vì sao 7 giá trị tín hiệu có thể chứa thông tin phân biệt phòng?
- Mô hình nào có F1-macro tốt nhất trên test? CV có ổn định không?
- Những cặp phòng nào dễ nhầm lẫn nhất?
- ARI của K-Means và DBSCAN nói gì về cấu trúc dữ liệu?
- Có thể dùng mô hình D08 cho một tòa nhà mới không? **Không trực tiếp**, cần dữ liệu mới và kiểm thử.

## Ngoài phạm vi

Không định vị chính xác theo tọa độ, không tìm router, không đo WiFi trực tiếp từ điện thoại, không kết hợp GPS, không tuyên bố giải pháp mới chưa từng tồn tại.

## Demo tùy chọn

Ứng dụng Streamlit nhập 7 RSSI, nạp **Pipeline đã lưu**, hiển thị phòng dự đoán. Demo chỉ phản ánh dữ liệu và 4 nhãn của D08.
