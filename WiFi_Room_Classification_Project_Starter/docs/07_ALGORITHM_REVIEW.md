# Rà soát thuật toán và hướng dẫn bảo vệ

## 1. Điều kiện dữ liệu

CSV phải có header `WiFi_1,...,WiFi_7,Room`, 2.000 dòng dữ liệu và 8 cột. Mỗi phòng có 500 mẫu. Notebook kiểm tra kiểu số, NaN/vô cực, nhãn và dòng trùng trước khi huấn luyện. Các điều kiện này dành riêng cho dữ liệu D08, không phải bộ nạp dữ liệu tổng quát.

Bảy tín hiệu RSSI là đại lượng đo lường, dù được ghi bằng số nguyên. Nhãn Room là biến phân loại. Không đưa Room vào khoảng cách KNN, scaler, PCA, K-Means hoặc DBSCAN.

Không tự xóa ngoại lệ RSSI chỉ vì boxplot đánh dấu điểm nằm xa: điểm đó có thể là phép đo hợp lệ. Không cần imputation khi CSV không thiếu dữ liệu. Nếu thay bộ dữ liệu, phải thiết kế lại quy trình xử lý thiếu/trùng trước khi chia tập.

## 2. Luồng đánh giá phân loại

1. Chia stratified 80/20, seed 42: train 1.600, test 400; kiểm tra chỉ số không giao nhau.
2. Dùng cùng StratifiedKFold 10 fold, shuffle và seed 42 cho cả năm thuật toán.
3. Scaler của KNN, GaussianNB và SVM ở trong Pipeline, được fit lại trong từng fold. Random Forest/AdaBoost dùng cây, không bắt buộc chuẩn hóa.
4. GridSearchCV chọn theo F1-macro; `error_score="raise"` khiến cấu hình lỗi dừng rõ ràng thay vì bị che bằng NaN.
5. `refit=True` fit cấu hình thắng trên toàn train. Mỗi mô hình được đánh giá trên cùng test. Không dùng kết quả test để sửa grid.
6. Bảng trước/sau dùng cùng 10 fold train; điểm sau được lấy từ GridSearchCV. So sánh này phục vụ khảo sát tối ưu, chưa phải nested CV.
7. Chọn mô hình bằng điểm CV đầy đủ chữ số. Nếu hòa chính xác, phá hòa theo thứ tự tên để tái lập. Không dùng điểm test để chọn.

PCA fit trên toàn dữ liệu chỉ dùng mô tả hình học. Code phân loại quay lại X gốc, do đó PCA này không gây rò rỉ vào bộ phân loại. Nếu sau này đưa PCA vào phân loại, phải đưa PCA vào Pipeline trước GridSearchCV.

Test đã xuất hiện trong quá trình phát triển báo cáo, nên dù code không tối ưu trên test, không nên mô tả nó là dữ liệu chưa từng được con người xem. Muốn đánh giá triển khai, cần một tập dữ liệu mới độc lập.

## 3. Kiểm tra từng thuật toán

| Thuật toán | Grid hiện có | Nhận xét |
|---|---|---|
| KNN | 6 giá trị K × 2 trọng số = 12 cấu hình | Hợp lý cho tập nhỏ. Mặc định Minkowski p=2 tương đương Euclidean. Có thể mở rộng p=1 nhưng không bắt buộc. |
| Random Forest | 2 số cây × 3 độ sâu × 2 min_samples_split = 12 | Đã khảo sát độ phức tạp. `max_depth=None` không có nghĩa mô hình chắc chắn quá khớp; phải xét CV/test. |
| GaussianNB | 6 mức var_smoothing | Tham số làm trơn ổn định phương sai. Điểm không đổi giữa vài mức là bình thường. RSSI tương quan không chứng minh giả định độc lập có điều kiện đúng. |
| AdaBoost | 3 số cây × 3 learning_rate × 3 độ sâu = 27 | Mặc định thư viện ảnh hưởng thuật toán boosting/xác suất; cố định scikit-learn 1.6.1 khi tái lập. Log Loss cao cần giải thích bằng xác suất, không tự kết luận nhiều lỗi nhãn. |
| SVM | 4 C linear + 4 C × 4 gamma RBF = 20 | Linear không cần gamma. C và gamma điều khiển độ phức tạp khác nhau. Bật probability để có Log Loss; `predict_proba` không nhất thiết có argmax trùng `predict`. |

Tổng 77 cấu hình × 10 fold = 770 lần fit CV, cộng 5 lần refit và 50 lần fit baseline. Giới hạn hai tiến trình để tránh chiếm hết RAM/CPU. Không cần tăng grid chỉ để có nhiều thí nghiệm hơn.

## 4. Diễn giải chỉ số

- F1-macro: trung bình F1 của bốn lớp, cao tốt; phù hợp so sánh cân bằng vai trò các phòng.
- Accuracy: tỷ lệ dự đoán đúng; không đánh giá chất lượng xác suất.
- Log Loss: âm trung bình log xác suất lớp thật, thấp tốt. Mốc xác suất đều bốn lớp là ln(4) ≈ 1,3863. Chênh lệch Log Loss không đồng nghĩa chênh lệch Accuracy.
- Std CV: độ dao động giữa fold, không phải khoảng tin cậy. Các fold có tập train giao nhau nên không xem chúng là mười thí nghiệm hoàn toàn độc lập.
- Thứ hạng với chênh lệch vài mẫu trên test chưa đủ khẳng định vượt trội có ý nghĩa thống kê. Chưa cần thêm kiểm định nếu chỉ báo cáo mô tả đúng giới hạn.

Notebook kiểm tra xác suất hữu hạn, không âm, mỗi dòng tổng bằng 1, đủ 400 × 4 giá trị; kiểm tra khoảng hợp lệ của các chỉ số và đủ năm mô hình.

## 5. Phân cụm

K-Means chạy trên bảy RSSI chuẩn hóa; `n_init=10`, seed 42. K=4 dựa vào số phòng đã biết, còn Elbow hỗ trợ khảo sát. Không tuyên bố Elbow chứng minh nghiệm tối ưu duy nhất.

DBSCAN gốc khảo sát 21 cấu hình và chọn ARI cao nhất. Nhãn không tham gia fit_predict nhưng có tham gia chọn tham số: đó là khảo sát có tham chiếu nhãn. ARI này không phải đánh giá độc lập của một quy trình chọn tham số hoàn toàn không giám sát.

Notebook bổ sung đồ thị 5-distance và cách chọn bằng Silhouette trên điểm không nhiễu, với độ phủ ít nhất 50% và ít nhất hai cụm. Quy tắc này được công bố trong code, không dò ngưỡng theo ARI. Nếu không có cấu hình hợp lệ, in rõ thay vì ép chọn. ARI được tính sau khi chọn, trên mọi mẫu gồm nhiễu. Silhouette và ARI có thể xếp hạng khác nhau vì đo hai khía cạnh khác nhau.

Độ phủ và số cụm phải được đọc cùng Silhouette: điểm cao trên một phần nhỏ dữ liệu có thể gây hiểu nhầm. Không coi nhiễu là một phòng riêng. ID cụm là tùy ý; dùng ARI/bảng chéo thay vì Accuracy trực tiếp.

## 6. Những gì chưa cần bổ sung để đạt đề

Không bắt buộc app, WiFi thời gian thực, deep learning, nested CV, calibration riêng hoặc tự thu dữ liệu. Các phần đó chỉ nên làm nếu có mục tiêu nghiên cứu rõ. Cần ưu tiên notebook chạy từ đầu tới cuối, bảng tham số hiển thị đầy đủ và PDF có code/kết quả/biểu đồ.

## 7. Tái lập và đầu ra

Notebook hỗ trợ tìm CSV local hoặc Colab upload/Drive; có thể đặt `WIFI_DATA_FILE` để chỉ định file. Chạy từ thư mục project hoặc notebooks. Trước khi nộp, khởi động kernel mới và chạy toàn bộ.

`reports/run_manifest.json` ghi Python, thư viện, SHA-256 dữ liệu và mô hình chọn theo CV. Các bảng CSV trong reports được sinh từ biến thực nghiệm; không nhập lại số bằng tay. Notebook còn giữ một số nhận xét/bảng tổng kết bằng văn bản: nếu đổi dữ liệu hay thư viện, phải đối chiếu lại chúng với output mới.

Chạy lại bằng môi trường đã cài dependencies:

```powershell
python scripts/verify_and_export.py
python scripts/export_pdf.py
```

Script thứ hai cần Playwright và Microsoft Edge. PDF được in từ HTML xuất trực tiếp từ notebook đã chạy. Cần xem lại bố cục PDF trước khi nộp.
