# Kết quả kiểm chứng

Đã chạy notebook từ kernel Python mới trên Windows, Python 3.11.6 và scikit-learn 1.6.1: 88 ô tổng cộng, 47 ô code được thực thi, không có output lỗi. Phiên bản và SHA-256 của CSV nằm trong `run_manifest.json`.

| Mô hình | Train CV F1 | Test F1 | Test Log Loss |
|---|---:|---:|---:|
| KNN | 0,984402354 | 0,985035578 | 0,031872436 |
| Random Forest | 0,985621971 | 0,980092984 | 0,056399482 |
| GaussianNB | 0,983105002 | 0,985044117 | 0,055514249 |
| AdaBoost | 0,985627754 | 0,980072651 | 1,152596749 |
| SVM | 0,983155832 | 0,987547534 | 0,045064201 |

Kết quả khớp các số cũ ở độ chính xác hiển thị. AdaBoost đứng đầu CV theo số chưa làm tròn, nhưng chênh lệch với RF rất nhỏ, không đủ tuyên bố vượt trội. SVM có F1 test cao nhất; KNN có Log Loss test thấp nhất. Chọn mô hình theo CV, không đổi sang SVM chỉ vì đã xem test.

## Phân cụm

- K-Means K=4: ARI 0,818236886.
- DBSCAN chọn theo ARI: eps=0,7, min_samples=5, 15 cụm, 865 nhiễu, ARI 0,290393340.
- DBSCAN chọn theo Silhouette với độ phủ >=50%: eps=1,5, min_samples=15, 2 cụm, độ phủ 97,45%, Silhouette 0,415521188. ARI đối chiếu sau khi chọn khoảng 0,0027.

Độ tách biệt hình học theo Silhouette không bảo đảm tái hiện bốn phòng. Không thay số này vào kết quả khảo sát theo ARI: đó là hai quy tắc chọn tham số khác nhau. Cả hai khảo sát vẫn dùng cùng dữ liệu, chưa kiểm định tổng quát hóa sang môi trường mới.

## Bằng chứng và giới hạn

- Kiểm tra CSV đủ schema, số mẫu, nhãn, giá trị hữu hạn và không trùng dòng.
- Kiểm tra train/test không giao chỉ số, đủ 7 đầu vào, 10 fold, xác suất dự đoán hợp lệ của cả năm mô hình.
- So sánh trước/sau dùng cùng fold; baseline được clone từ estimator trước tìm kiếm.
- PDF xuất trực tiếp từ HTML của notebook đã chạy: 92 trang, có mã PDF hợp lệ. Đã xem preview HTML về chữ tiếng Việt; chưa kiểm tra thủ công toàn bộ 92 trang PDF. Nhóm cần rà ngắt trang trước khi nộp.
- Bản gốc ở `.verification/original.ipynb` để đối chiếu, không phải file nộp.
- `requirements-reproducible.txt` lưu môi trường lúc chạy. `.venv` ở thư mục cha không phải thành phần bài nộp; nếu không còn đầy đủ, tạo môi trường mới rồi cài lại file này.
