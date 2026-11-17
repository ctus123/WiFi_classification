# 03 — Quy trình Machine Learning

## Phần 1 — EDA

Đọc CSV bằng pandas; báo cáo số dòng/cột, kiểu dữ liệu, số lượng lớp, phân bố nhãn, min/max/mean của từng đặc trưng. Có thể bổ sung boxplot/heatmap tương quan nếu giúp giải thích dữ liệu.

## Phần 2 — PCA

- Chọn 7 cột RSSI, chuẩn hóa với `StandardScaler`.
- PCA xuống 2 chiều; vẽ scatter PC1–PC2 tô màu theo `Room`.
- Báo cáo tỷ lệ phương sai giải thích (`explained_variance_ratio_`).
- PCA dùng để **trực quan hóa**, không mặc nhiên thay 7 đặc trưng trong mọi mô hình phân loại.

## Phần 3 — Phân loại có giám sát

5 thuật toán bắt buộc:

1. **KNN** — dựa trên láng giềng gần nhất.
2. **Random Forest** — tập hợp nhiều cây quyết định.
3. **Gaussian Naive Bayes** — phân loại xác suất với giả định độc lập có điều kiện.
4. **AdaBoost** — kết hợp nhiều bộ phân loại yếu.
5. **SVM** — tìm ranh giới phân loại, có thể dùng kernel.

### Đánh giá công bằng

1. Chia stratified train/test (gợi ý 80/20).
2. Với mỗi thuật toán, xây `Pipeline` gồm các bước tiền xử lý cần thiết và classifier.
3. Dùng `StratifiedKFold(n_splits=10, shuffle=True, random_state=42)` và `GridSearchCV` trên train.
4. Chọn theo **F1-macro** trung bình CV, ghi lại tham số tối ưu và độ lệch chuẩn.
5. Đánh giá một lần trên test: F1-macro, confusion matrix và loss đã định nghĩa.

**Lưu ý về loss:** đề bài yêu cầu so sánh loss và F-score nhưng chưa xác định loss cụ thể. Nếu chọn **log loss**, cần xác suất dự đoán hợp lệ (`predict_proba`); SVM cần `probability=True` và thời gian chạy có thể tăng. Cần ghi rõ định nghĩa loss và áp dụng nhất quán. Không gọi `1 - accuracy` là log loss.

**Gợi ý grid nhỏ để tránh quá tải:**

- KNN: `n_neighbors` = 3, 5, 7, 11; `weights` = uniform/distance.
- RF: `n_estimators` = 100, 200; `max_depth` = None, 10.
- GaussianNB: `var_smoothing` = 1e-9, 1e-8, 1e-7.
- AdaBoost: `n_estimators` = 50, 100; `learning_rate` = 0.5, 1.0.
- SVM: `C` = 0.1, 1, 10; `kernel` = linear/rbf (nếu cần giảm tải, thử rbf trước).

Các grid trên chỉ là gợi ý khởi đầu, không phải kết quả tối ưu.

## Phần 4 — Phân cụm không giám sát

- Dùng `X` (không có cột `Room`), chuẩn hóa 7 đặc trưng.
- **K-Means:** thử `n_clusters=4` và ghi rõ đây là giả thuyết dựa trên số lớp đã biết.
- **DBSCAN:** thử các giá trị `eps` và `min_samples`; ghi nhận số cụm và số điểm nhiễu.
- Sau khi phân cụm, dùng nhãn thật **chỉ để đánh giá** bằng `adjusted_rand_score(y, labels)`.
- ARI = 1: trùng khớp; gần 0: gần mức ngẫu nhiên; có thể âm.

## Phân tích kết quả

- Mô hình nào F1-macro cao nhất và có ổn định qua 10 folds không?
- Confusion matrix cho thấy phòng nào dễ nhầm lẫn?
- PCA cho thấy các lớp tách biệt hay chồng lấn?
- ARI có ủng hộ giả thuyết dữ liệu tự chia thành các nhóm tương ứng phòng không?
- Giới hạn: chỉ 4 phòng trong môi trường dữ liệu D08, không suy ra hiệu năng ở nơi khác.

## Chống lỗi thường gặp

- Không đọc CSV sai header làm mất dòng đầu.
- Không chuẩn hóa toàn bộ trước train/test cho phần phân loại.
- Không dùng test để chọn tham số.
- Không đưa nhãn `Room` vào PCA/clustering như một đặc trưng.
- Không coi chỉ số ARI là độ chính xác phân loại.
- Không báo cáo điểm số giả định như kết quả thực nghiệm.
