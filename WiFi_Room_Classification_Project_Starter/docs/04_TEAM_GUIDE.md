# 04 — Hướng dẫn thành viên và làm việc nhóm

## Thành viên mới cần đọc

1. `README.md` — mục tiêu và cấu trúc dự án.
2. `docs/01_PROJECT_OVERVIEW.md` — bài toán, phạm vi.
3. `docs/02_DATA_GUIDE.md` — cách đọc và hiểu dữ liệu.
4. `docs/03_ML_WORKFLOW.md` — các phần phải triển khai.
5. `docs/05_DELIVERABLES.md` — tiêu chí hoàn thành.

## Quy tắc Git/GitHub đề xuất

- `main`: phiên bản ổn định; `develop`: tích hợp các phần đang làm.
- Mỗi thành viên tạo nhánh riêng từ `develop`, ví dụ `feature/eda-pca`, `feature/classifiers`, `feature/clustering`, `docs/report`.
- Không code trực tiếp lên `main` hoặc `develop` nếu nhóm đã thống nhất làm qua Pull Request.
- Pull mới nhất từ `develop` trước khi bắt đầu; tạo PR để thành viên khác review trước khi merge.
- Commit mô tả rõ thay đổi: `feat: add PCA visualization`, `docs: clarify dataset schema`.

```bash
git clone <REPOSITORY_URL>
cd wifi-room-classification-starter
git switch develop
git pull origin develop
git switch -c feature/eda-pca
# làm việc, lưu file
git add .
git commit -m "feat: add exploratory data analysis"
git push -u origin feature/eda-pca
```

`<REPOSITORY_URL>` là chỗ thay bằng link GitHub thực tế của nhóm. Nếu nhánh `develop` chưa tồn tại, nhóm trưởng tạo trước.

## Làm việc với notebook

- Chọn **một notebook chính** để tích hợp cuối cùng (`notebooks/wifi_room_classification.ipynb`).
- Để tránh xung đột Git khi nhiều người sửa một `.ipynb`, các thành viên có thể làm trên notebook riêng rồi tích hợp vào notebook chính theo phân công.
- Mọi mô hình dùng cùng train/test split, random_state và chỉ số đánh giá.
- Trước khi merge, chạy lại toàn bộ cell theo thứ tự, không để lỗi hoặc đường dẫn chỉ chạy được trên máy cá nhân.
- Nếu làm trên Colab, lưu bản `.ipynb` về repo và đảm bảo hướng dẫn nạp CSV rõ ràng.

## Phân công gợi ý (điều chỉnh theo số thành viên)

| Vai trò | Phần việc |
|---|---|
| A | Dữ liệu, EDA, PCA |
| B | KNN, Random Forest, Naive Bayes |
| C | AdaBoost, SVM, Cross-Validation và bảng so sánh |
| D | K-Means, DBSCAN, ARI, báo cáo tổng hợp |

Cả nhóm cùng đọc hiểu toàn bộ quy trình, kiểm tra kết quả và chuẩn bị bảo vệ; không chỉ hiểu phần mình viết.

## Quy tắc chất lượng

- Không đưa API key, token hoặc dữ liệu nhạy cảm vào repo.
- Không commit file mô hình `joblib` không rõ nguồn; chỉ nạp file do nhóm tự tạo và tin cậy.
- Code có comment cho các bước quan trọng, tên biến dễ hiểu.
- Mọi số liệu trong báo cáo phải đến từ lần chạy thực tế và tái lập được.
