# 05 — Checklist hoàn thành và nộp bài

Đã chạy kiểm chứng 47/47 ô code từ kernel mới và xuất PDF. Xem [kết quả kiểm chứng](../reports/VERIFICATION.md) và [rà soát thuật toán](07_ALGORITHM_REVIEW.md). Nhóm vẫn cần xem lại toàn bộ PDF về ngắt trang/bảng biểu, thống nhất cách giải thích và đối chiếu quy định nộp chính thức.

## Bắt buộc theo đề bài

- [x] CSV đọc được bằng pandas, đủ số mẫu, đúng 8 cột.
- [x] Thống kê shape, dtypes, số lớp, phân bố lớp, min/max/mean.
- [x] Chuẩn hóa đặc trưng số; PCA 2 chiều và scatter plot tô màu theo lớp.
- [x] Huấn luyện/tối ưu KNN, Random Forest, Naive Bayes, AdaBoost, SVM.
- [x] Dùng 10-fold cross-validation và ghi rõ tham số tốt nhất.
- [x] Bảng so sánh loss và F-score, ghi rõ cách tính.
- [x] Bỏ nhãn khi chạy K-Means và DBSCAN.
- [x] Tính và giải thích ARI so với nhãn thật.
- [x] Notebook `.ipynb` chạy từ đầu đến cuối không lỗi.
- [x] Xuất PDF từ notebook, chứa code/kết quả/biểu đồ cần thiết.

## Chất lượng nên có

- [ ] Tập test độc lập, không dùng để tinh chỉnh.
- [ ] Tránh data leakage qua scaler/PCA.
- [ ] Confusion matrix và nhận xét về các phòng dễ nhầm.
- [ ] Ghi rõ phiên bản thư viện, random_state, cách nạp dữ liệu.
- [ ] Nhận xét dựa trên kết quả thật, nêu hạn chế của D08.
- [ ] Thành viên đều giải thích được bài toán và quy trình.

## Tùy chọn (không ảnh hưởng phần bắt buộc)

- [ ] Demo Streamlit nhập 7 RSSI và dự đoán phòng.
- [ ] Lưu Pipeline đã huấn luyện và kiểm tra đầu vào.

## File nộp dự kiến

- `notebooks/FINAL_WiFi_Classification (2).ipynb`
- `reports/wifi_room_classification.pdf`

Tên file, phương thức nộp và hạn nộp cuối cùng cần đối chiếu thông báo chính thức của giảng viên.
