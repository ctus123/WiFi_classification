# WiFi Room Classification — Machine Learning Project

**Tên tiếng Việt:** Ứng dụng và đánh giá các thuật toán Machine Learning trong bài toán phân loại phòng dựa trên tín hiệu WiFi.  
**English:** Application and Evaluation of Machine Learning Algorithms for WiFi-Based Room Classification.

## 1. Dự án giải quyết vấn đề gì?

Dựa trên **7 giá trị cường độ tín hiệu WiFi (RSSI)** của một mẫu đo, dự đoán mẫu đó thuộc **phòng 1, 2, 3 hay 4**. Đây là **phân loại phòng**, không phải tìm vị trí router, định vị GPS hay suy ra tọa độ chính xác.

## 2. Dữ liệu

- Dataset: **D08 — WiFi Localization** do giảng viên cung cấp.
- **2.000 mẫu**, **7 đặc trưng số** (WiFi_1…WiFi_7), **4 nhãn phòng**, mỗi phòng 500 mẫu.
- File nguồn là Excel; cần xuất thành CSV để xử lý bằng pandas theo yêu cầu.
- **Lưu ý quan trọng:** sheet dữ liệu gốc **không có hàng tiêu đề**. Khi đọc phải đặt tên 8 cột rõ ràng, tránh vô tình mất mẫu đầu tiên.
- Chưa có dữ liệu đo trực tiếp tại trường/tòa nhà khác; mô hình không thể áp dụng nguyên trạng cho mọi nơi.

## 3. Câu hỏi nghiên cứu

1. Dữ liệu tín hiệu của 4 phòng khác nhau thế nào?
2. PCA 2 chiều cho thấy mức độ tách biệt của các phòng ra sao?
3. Trong KNN, Random Forest, Gaussian Naive Bayes, AdaBoost, SVM, mô hình nào có **F1-macro** tốt nhất?
4. K-Means và DBSCAN có tạo ra các cụm tương ứng với nhãn phòng thật không (đánh giá bằng ARI)?
5. Mô hình thường nhầm phòng nào với phòng nào (confusion matrix)?

## 4. Phạm vi bắt buộc

| Phần | Nội dung | Kết quả |
|---|---|---|
| 1 | pandas: shape, dtypes, phân bố lớp, min/max/mean | Thống kê, biểu đồ |
| 2 | Chọn đặc trưng liên tục, chuẩn hóa, PCA 2 chiều | Scatter plot tô màu theo nhãn |
| 3 | KNN, Random Forest, Naive Bayes, AdaBoost, SVM; tinh chỉnh tham số; 10-fold CV | Bảng so sánh F-score và loss |
| 4 | Bỏ nhãn, K-Means, DBSCAN, đối chiếu ARI | Bảng/nhận xét ARI |

**Không bắt buộc:** app web, thu tín hiệu WiFi thời gian thực, GPS, chọn đặc trưng mở rộng. Chỉ thực hiện khi hoàn thành phần chính.

## 5. Công nghệ

Python, pandas, NumPy, scikit-learn, Matplotlib, Seaborn, Jupyter/Google Colab. VS Code và Git/GitHub dùng để quản lý mã nguồn và cộng tác. Streamlit là tùy chọn cho demo.

## 6. Cấu trúc repository

```text
wifi-room-classification-starter/
├── README.md
├── requirements.txt
├── .gitignore
├── docs/
│   ├── 01_PROJECT_OVERVIEW.md
│   ├── 02_DATA_GUIDE.md
│   ├── 03_ML_WORKFLOW.md
│   ├── 04_TEAM_GUIDE.md
│   ├── 05_DELIVERABLES.md
│   └── 06_GLOSSARY.md
├── data/             # CSV dữ liệu (chưa kèm file dữ liệu)
├── notebooks/        # notebook .ipynb chính
├── reports/          # PDF xuất từ notebook
└── app/              # demo tùy chọn
```

## 7. Bắt đầu nhanh

1. Đọc `README.md`, sau đó đọc tài liệu trong `docs/` theo thứ tự số.
2. Clone repository, tạo nhánh riêng theo hướng dẫn tại `docs/04_TEAM_GUIDE.md`.
3. Tạo môi trường Python và cài thư viện: `pip install -r requirements.txt` (nếu chạy local).
4. Xuất sheet `wifi_localization` của Excel thành `data/wifi_localization.csv` với **8 cột, không có header**; hoặc dùng pandas đọc Excel `header=None`, gán tên cột, rồi xuất CSV có header.
5. Mở notebook `.ipynb` trên VS Code hoặc Colab. Trên Colab, cần upload CSV hoặc mount Drive và sửa đường dẫn.
6. Chạy notebook từ đầu đến cuối, kiểm tra kết quả, xuất PDF theo yêu cầu giảng viên.

## 8. Quy tắc đánh giá

- Gợi ý chia dữ liệu **stratified 80/20**; 10-fold CV **chỉ trên tập train**.
- Dùng `Pipeline` để fit scaler/biến đổi **bên trong từng fold**, tránh data leakage.
- Ưu tiên **F1-macro**; cần **định nghĩa rõ loss** trước khi so sánh (ví dụ log loss nếu mô hình xuất được xác suất hợp lệ).
- Chỉ dùng test set sau khi đã chọn mô hình/tham số bằng train/CV.
- Với phân cụm, không đưa nhãn phòng vào đầu vào thuật toán; nhãn chỉ dùng tính ARI sau đó.

## 9. Tài liệu liên quan

- [Tổng quan](docs/01_PROJECT_OVERVIEW.md)
- [Hướng dẫn dữ liệu](docs/02_DATA_GUIDE.md)
- [Quy trình Machine Learning](docs/03_ML_WORKFLOW.md)
- [Hướng dẫn thành viên/Git](docs/04_TEAM_GUIDE.md)
- [Checklist nộp bài](docs/05_DELIVERABLES.md)
- [Thuật ngữ](docs/06_GLOSSARY.md)

> Project đã có notebook và kết quả thực nghiệm được chạy kiểm chứng. Xem phần rà soát thuật toán bên dưới.


## 10. Rà soát và tái lập

- Notebook chính: `notebooks/FINAL_WiFi_Classification (2).ipynb`.
- Phân tích logic thuật toán: [07_ALGORITHM_REVIEW.md](docs/07_ALGORITHM_REVIEW.md).
- Chạy từ kernel mới; notebook tự tìm CSV local hoặc hỗ trợ Colab.
- Dùng `requirements-reproducible.txt` cho môi trường thực nghiệm đã kiểm chứng; `requirements.txt` là dải phiên bản tổng quát.
- `python scripts/verify_and_export.py` chạy toàn bộ notebook và xuất HTML.
- `python scripts/export_pdf.py` xuất PDF qua Playwright và Microsoft Edge.
- Không chạy lại `scripts/improve_notebook.py`: đây là script chuyển đổi một lần từ bản gốc trong `.verification/`, sẽ xóa output hiện tại.
