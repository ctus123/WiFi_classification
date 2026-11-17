# 02 — Hướng dẫn dữ liệu D08

## Sơ đồ dữ liệu

| Cột | Kiểu | Vai trò |
|---|---|---|
| WiFi_1 ... WiFi_7 | Số | Cường độ RSSI (dBm), 7 đặc trưng |
| Room | Số nguyên | Nhãn phòng 1, 2, 3, 4 |

Theo file đã kiểm tra: **2.000 mẫu, 500 mẫu mỗi phòng**. Sheet dữ liệu `wifi_localization` không có header. Cần xác minh lại khi nhận file thực tế.

## Đọc file Excel đúng cách và xuất CSV

```python
import pandas as pd

cols = [f"WiFi_{i}" for i in range(1, 8)] + ["Room"]
df = pd.read_excel("D08 - wifi_localization.xlsx", sheet_name="wifi_localization", header=None)
assert df.shape == (2000, 8), f"Unexpected shape: {df.shape}"
df.columns = cols
assert df["Room"].isin([1, 2, 3, 4]).all()
df.to_csv("data/wifi_localization.csv", index=False)
```

Sau đó trong notebook dùng:

```python
df = pd.read_csv("data/wifi_localization.csv")
print(df.shape, df.dtypes)
print(df["Room"].value_counts().sort_index())
print(df.describe().T)
```

Nếu CSV được xuất **không có header**, phải đọc `pd.read_csv(path, header=None, names=cols)` thay vì lệnh mặc định.

## Những kiểm tra bắt buộc

- `shape`, `head`, `info`, `dtypes`, `isna().sum()`.
- `Room.value_counts()` và biểu đồ phân bố lớp.
- `describe()` hoặc `agg(['min','max','mean'])` cho 7 đặc trưng.
- Kiểm tra nhãn hợp lệ, trùng lặp, giá trị ngoại lệ (nếu có).
- Không đưa `Room` vào tập đặc trưng `X`.

## Phân chia dữ liệu

```python
from sklearn.model_selection import train_test_split
X = df.drop(columns="Room")
y = df["Room"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)
```

**Tránh rò rỉ dữ liệu:** chỉ fit scaler trên train (hoặc bên trong từng fold CV). Không fit scaler toàn bộ dữ liệu trước khi chia train/test trong phần đánh giá phân loại.
