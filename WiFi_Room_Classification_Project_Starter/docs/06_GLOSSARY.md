# 06 — Giải thích thuật ngữ cho thành viên mới

| Thuật ngữ | Giải thích ngắn |
|---|---|
| RSSI | Chỉ số cường độ tín hiệu thu được; trong dữ liệu thường biểu diễn bằng dBm |
| Feature (đặc trưng) | Giá trị đầu vào cho mô hình; ở đây là WiFi_1…WiFi_7 |
| Label (nhãn) | Phòng đúng của mẫu, nhận giá trị 1–4 |
| Classification | Dự đoán nhãn phòng từ các đặc trưng |
| Supervised learning | Học từ dữ liệu đã có nhãn |
| Unsupervised learning | Tìm cấu trúc/nhóm mà không dùng nhãn để huấn luyện |
| PCA | Phương pháp biến đổi tuyến tính giúp giảm số chiều, thường dùng để trực quan hóa |
| StandardScaler | Chuẩn hóa từng đặc trưng theo trung bình và độ lệch chuẩn |
| KNN | Dự đoán dựa trên các mẫu gần nhất |
| Random Forest | Kết hợp nhiều cây quyết định |
| Gaussian Naive Bayes | Mô hình xác suất với giả định phân phối Gaussian cho đặc trưng theo lớp |
| AdaBoost | Thuật toán boosting kết hợp nhiều bộ học yếu |
| SVM | Bộ phân loại dựa trên ranh giới phân tách có biên |
| Cross-Validation | Đánh giá nhiều lượt trên các phần dữ liệu khác nhau |
| 10-fold CV | Chia thành 10 phần; mỗi lượt đánh giá trên 1 phần và học từ 9 phần còn lại |
| F1-macro | Trung bình F1 của từng lớp, coi mỗi lớp có trọng số bằng nhau |
| Loss | Hàm đo sai số; phải định nghĩa cụ thể (ví dụ log loss) |
| Confusion Matrix | Bảng đếm nhãn thật so với nhãn dự đoán |
| K-Means | Phân cụm theo khoảng cách tới tâm cụm |
| DBSCAN | Phân cụm dựa trên mật độ và có thể nhận diện điểm nhiễu |
| ARI | Chỉ số so sánh hai cách phân nhóm, đã điều chỉnh yếu tố ngẫu nhiên |
| Data leakage | Thông tin từ tập đánh giá vô tình lọt vào quá trình huấn luyện/chọn mô hình |
| Pipeline | Chuỗi tiền xử lý và mô hình để fit/predict nhất quán |
