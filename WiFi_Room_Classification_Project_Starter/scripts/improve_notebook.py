"""One-time revision of the supplied notebook; preserve its existing analysis."""
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = next((ROOT / 'notebooks').glob('*.ipynb'))
backup = ROOT / '.verification' / 'original.ipynb'
backup.parent.mkdir(exist_ok=True)
if not backup.exists():
    shutil.copy2(path, backup)
nb = json.loads(backup.read_text(encoding='utf-8'))

def md(s):
    return {'cell_type': 'markdown', 'metadata': {}, 'source': s.strip() + '\n'}

def code(s):
    return {'cell_type': 'code', 'metadata': {}, 'execution_count': None,
            'outputs': [], 'source': s.strip() + '\n'}

nb['cells'][2] = code('''
# Tìm CSV trong project local trước; Colab hỗ trợ upload hoặc Google Drive.
from pathlib import Path
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option("display.max_colwidth", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 180)
N_JOBS = int(os.environ.get("WIFI_N_JOBS", "2"))
CSV_NAME = "wifi_localization.csv"
override = os.environ.get("WIFI_DATA_FILE")
if override:
    DATA_FILE = Path(override).expanduser().resolve()
else:
    candidates = [Path.cwd()/"data"/CSV_NAME, Path.cwd().parent/"data"/CSV_NAME,
                  Path.cwd()/CSV_NAME, Path("/content")/CSV_NAME]
    DATA_FILE = next((p.resolve() for p in candidates if p.is_file()), None)
    if DATA_FILE is None:
        try:
            from google.colab import drive
        except ImportError:
            raise FileNotFoundError("Mở notebook từ thư mục project/notebooks hoặc đặt WIFI_DATA_FILE trỏ tới CSV.")
        drive.mount("/content/drive")
        DATA_FILE = Path("/content/drive/MyDrive/WiFi-Room-Classification/data")/CSV_NAME
if not DATA_FILE.is_file():
    raise FileNotFoundError(f"Không tìm thấy CSV: {DATA_FILE}")
file_path = str(DATA_FILE)
print("CSV:", DATA_FILE)
print("Số tiến trình CV:", N_JOBS)
''')
validation = code('''
# Dừng sớm nếu dữ liệu không đúng hợp đồng của bài D08.
expected_features = [f"WiFi_{i}" for i in range(1, 8)]
assert list(df.columns) == expected_features + ["Room"], "Sai tên/thứ tự cột hoặc CSV thiếu header."
assert df.shape == (2000, 8), "Sai số mẫu hoặc số cột."
assert all(pd.api.types.is_numeric_dtype(df[c]) for c in df.columns), "Có cột không phải số."
assert np.isfinite(df.to_numpy(dtype=float)).all(), "Có NaN hoặc vô cực."
assert set(df["Room"].unique()) == {1, 2, 3, 4}, "Sai nhãn phòng."
assert df["Room"].value_counts().eq(500).all(), "Phân bố nhãn không đúng D08."
assert not df.duplicated().any(), "Có dòng trùng: cần kiểm tra trước khi chia train/test."
print("PASS: 2.000 mẫu, 7 RSSI hữu hạn, 4 nhãn cân bằng, không có dòng trùng.")
''')
theory = md('''
### Cách đọc thuật toán và các chỉ số

RSSI là đại lượng đo lường dù CSV lưu số nguyên. `Room` là mã lớp, không phải đặc trưng liên tục; không được đưa vào scaler, PCA hay đầu vào mô hình.

| Thuật toán | Cơ chế và giả định | Tham số đang khảo sát | Vì sao tiền xử lý như vậy? |
|---|---|---|---|
| KNN | Bỏ phiếu theo láng giềng gần trong không gian RSSI; dùng khoảng cách Euclidean mặc định | Số láng giềng, trọng số đều/theo khoảng cách | StandardScaler trong từng fold tránh một cột chi phối khoảng cách |
| Random Forest | Tổng hợp cây, học quan hệ phi tuyến bằng chia ngưỡng | Số cây, độ sâu, số mẫu để tách nút | Cây không cần chuẩn hóa; đặt seed cố định |
| GaussianNB | Ước lượng phân bố Gaussian của từng đặc trưng theo lớp, giả định độc lập có điều kiện | `var_smoothing`: ổn định phương sai | Scaler nằm trong Pipeline; tương quan RSSI khiến giả định độc lập chỉ là xấp xỉ |
| AdaBoost | Tăng trọng số mẫu khó, kết hợp nhiều cây yếu | Số cây, learning rate, độ sâu cây cơ sở | Cây không cần scaler; độ sâu lớn có thể tăng nguy cơ quá khớp |
| SVM | Tìm biên phân tách; RBF mô hình hóa quan hệ phi tuyến | Kernel, C, gamma của RBF | Phải chuẩn hóa trong fold; C lớn phạt lỗi mạnh hơn, gamma lớn khiến RBF cục bộ hơn |

GridSearchCV chọn cấu hình có **F1-macro trung bình cao nhất trên 10 fold train**. `refit=True` huấn luyện lại cấu hình được chọn trên toàn bộ 1.600 mẫu train. Test 400 mẫu chỉ phục vụ báo cáo cuối cùng, không dùng đổi grid hoặc chọn tham số. Điểm CV của cấu hình thắng có thiên lệch do chọn cấu hình trên chính các fold này; nested CV là mở rộng, không phải yêu cầu bắt buộc.

Với mỗi lớp, F1 = 2PR/(P+R); F1-macro là trung bình không trọng số của bốn F1, **cao hơn tốt hơn**. Accuracy là tỷ lệ nhãn dự đoán đúng. Log Loss = -mean(log p(lớp đúng)), **thấp hơn tốt hơn**; giá trị lớn không nhất thiết đồng nghĩa nhiều nhãn sai. Các grid tối ưu F1, không tối ưu Log Loss. SVC bật `probability=True` để ước lượng xác suất bằng cơ chế hiệu chỉnh nội bộ; `predict` và lớp có xác suất lớn nhất có thể khác nhau.

PCA tối đa hóa phương sai, không tối đa hóa khả năng phân lớp. PCA toàn dữ liệu chỉ phục vụ hình minh họa; toàn bộ bộ phân loại dùng 7 đặc trưng gốc và scaler riêng trong CV. Không được lấy `X_scaled` toàn dữ liệu làm đầu vào GridSearchCV.
''')
split_check = code('''
assert set(X_train.index).isdisjoint(X_test.index)
assert list(X_train.columns) == expected_features and "Room" not in X_train
assert len(X_train) == 1600 and len(X_test) == 400
assert y_train.value_counts().eq(400).all() and y_test.value_counts().eq(100).all()
print("PASS: train/test không giao chỉ số; đúng 7 đầu vào; các lớp được giữ cân bằng.")
''')
selection = code('''
# Chốt theo CV chưa làm tròn; thứ tự tên là quy tắc phá hòa chính xác.
selected_name = sorted(grids, key=lambda name: (-grids[name].best_score_, name))[0]
selected_model = grids[selected_name].best_estimator_
print("Mô hình được chọn theo train CV:", selected_name)
print("CV F1-macro (chưa làm tròn):", grids[selected_name].best_score_)
print("Test F1 cao nhất chỉ mô tả bảng kết quả, không phải quy tắc chọn mô hình.")
''')
cluster_theory = md('''
### Logic phân cụm và giới hạn đánh giá

K-Means tối thiểu hóa tổng bình phương khoảng cách tới tâm cụm; cần biết K trước, nhạy với thang đo và khởi tạo. `n_init=10` thử nhiều khởi tạo; K=4 là lựa chọn có thông tin về số phòng, không phải kết quả khám phá hoàn toàn tự động. Elbow hỗ trợ khảo sát, không chứng minh duy nhất K=4.

DBSCAN nhóm điểm theo mật độ với khoảng cách Euclidean. `eps` quá nhỏ dễ tạo nhiều nhiễu; quá lớn dễ nối các vùng thành một cụm. `min_samples` tính cả chính điểm đang xét. Nhãn -1 là nhiễu, không phải phòng thứ năm. Nhãn cụm là mã tùy ý, nên không so trực tiếp bằng Accuracy.

ARI so sánh các cặp mẫu có cùng/khác nhóm, đã hiệu chỉnh mức trùng hợp ngẫu nhiên: 1 là trùng hoàn toàn, gần 0 là gần mức ngẫu nhiên, có thể âm. ARI ở đây tính trên **mọi mẫu, gồm cả nhiễu -1**. Báo thêm tỷ lệ nhiễu để tránh kết luận chỉ dựa vào ARI.

Phần khảo sát gốc chọn DBSCAN theo ARI: hợp yêu cầu đối chiếu nhãn nhưng có sử dụng nhãn để chọn cấu hình. Phần bổ sung bên dưới chọn một cấu hình bằng Silhouette không dùng nhãn; ARI chỉ được tính sau khi chốt. Silhouette đo độ tách biệt theo khoảng cách, không đảm bảo khớp nhãn phòng. Hai tiêu chí trả lời hai câu hỏi khác nhau.
''')
unsup = code('''
from sklearn.metrics import silhouette_score
from sklearn.neighbors import NearestNeighbors

# Đồ thị khoảng cách đến láng giềng thứ 5 (gồm chính điểm) hỗ trợ đọc eps.
distances, _ = NearestNeighbors(n_neighbors=5).fit(X_cluster_scaled).kneighbors(X_cluster_scaled)
plt.figure(figsize=(9, 4))
plt.plot(np.sort(distances[:, -1]))
plt.xlabel("Mẫu xếp tăng dần khoảng cách")
plt.ylabel("Khoảng cách tới láng giềng thứ 5")
plt.title("DBSCAN: khảo sát 5-distance, không dùng nhãn phòng")
plt.grid(alpha=.3)
plt.show()

# Chọn bằng Silhouette trên điểm không nhiễu, kèm điều kiện độ phủ >= 50%.
# Ngưỡng này là quy tắc khảo sát công bố trước, không tối ưu theo ARI.
internal_rows = []
for eps in eps_values:
    for min_samples in min_samples_values:
        labels = DBSCAN(eps=eps, min_samples=min_samples).fit_predict(X_cluster_scaled)
        mask = labels != -1
        count = len(set(labels[mask]))
        coverage = float(mask.mean())
        score = np.nan
        if coverage >= .5 and 2 <= count < int(mask.sum()):
            score = silhouette_score(X_cluster_scaled[mask], labels[mask])
        internal_rows.append(dict(eps=eps, min_samples=min_samples,
                                  clusters=count, coverage=coverage, silhouette=score))
dbscan_internal_df = pd.DataFrame(internal_rows)
valid = dbscan_internal_df.dropna(subset=["silhouette"]).sort_values(
    ["silhouette", "coverage", "eps", "min_samples"], ascending=[False, False, True, True])
display(dbscan_internal_df.round(4))
if valid.empty:
    print("Không có cấu hình thỏa quy tắc; không ép chọn cấu hình.")
else:
    choice = valid.iloc[0]
    independent_labels = DBSCAN(eps=float(choice.eps), min_samples=int(choice.min_samples)).fit_predict(X_cluster_scaled)
    print("Cấu hình chọn KHÔNG dùng nhãn:", choice.to_dict())
    print("ARI đối chiếu sau khi chốt:", round(adjusted_rand_score(y_true, independent_labels), 4))
    print("Đây vẫn là khảo sát trên cùng dữ liệu, không phải kiểm định trên tập mới.")
''')
export = code('''
# Kiểm chứng đầu ra và xuất bảng để đối chiếu báo cáo.
import hashlib
import json
from importlib.metadata import version
assert len(results_df) == 5 and results_df["Model"].nunique() == 5
assert results_df[["CV_F1_Macro", "Test_Accuracy", "Test_F1_Macro"]].apply(lambda col: col.between(0, 1).all()).all()
assert np.isfinite(results_df["Test_Log_Loss"]).all() and results_df["Test_Log_Loss"].ge(0).all()
for name, grid in grids.items():
    probabilities = grid.best_estimator_.predict_proba(X_test)
    assert probabilities.shape == (400, 4), name
    assert np.isfinite(probabilities).all() and (probabilities >= 0).all(), name
    assert np.allclose(probabilities.sum(axis=1), 1), name
    assert grid.n_splits_ == 10, name
    assert grid.best_estimator_.n_features_in_ == 7, name
assert -1 <= kmeans_ari <= 1 and -1 <= dbscan_ari <= 1
if DATA_FILE.parent.name == "data":
    REPORT_DIR = DATA_FILE.parent.parent / "reports"
else:
    REPORT_DIR = Path.cwd() / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)
for name, table in {"classification_results": results_df, "cv_summary": cv_summary,
                    "tuning_comparison": tuning_comparison_df,
                    "clustering_results": clustering_comparison,
                    "dbscan_grid": dbscan_results_df,
                    "dbscan_internal": dbscan_internal_df}.items():
    table.to_csv(REPORT_DIR / f"{name}.csv", index=False, encoding="utf-8-sig")
manifest = {"python": sys.version, "packages": {p: version(p) for p in
            ["numpy", "pandas", "scikit-learn", "matplotlib", "seaborn"]},
            "data_sha256": hashlib.sha256(DATA_FILE.read_bytes()).hexdigest(),
            "selected_by_train_cv": selected_name,
            "checks": "PASS: shape, schema, finite data, split, 10-fold, probabilities, metrics"}
(REPORT_DIR / "run_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
print("PASS: kiểm chứng đầu ra của 5 thuật toán; đã xuất bảng và thông tin tái lập vào", REPORT_DIR)
''')

cells = []
for i, c in enumerate(nb['cells']):
    if c['cell_type'] == 'code':
        source = ''.join(c['source']).replace('n_jobs=-1', 'n_jobs=N_JOBS')
        if 'GridSearchCV(' in source:
            source = source.replace('refit=True', 'error_score="raise",\n    refit=True')
        c = code(source)
    cells.append(c)
    if i == 3: cells.append(validation)
    if i == 19: cells.extend([split_check, theory])
    if i == 50: cells.append(selection)
    if i == 58: cells.append(cluster_theory)
    if i == 69: cells.extend([md('### Khảo sát DBSCAN bổ sung không chọn tham số theo nhãn'), unsup])
    if i == 76: cells.extend([md('### Kiểm chứng kết quả và xuất bảng thực nghiệm'), export])
nb['cells'] = cells
path.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding='utf-8')
print(path)
