# Tabular (Chợ Tốt xe máy cũ): kết quả trên tập test

Sinh ra bởi `tabular.ipynb`. Tập test: 2,374 tin. `final = True` là mô hình chọn theo R² validation. R2 tính trên log10(giá).

## Các mô hình

| model | final | val_R2 | test_R2 | test_median_APE_% | test_within_10_% | test_MAE_trieu |
|---|---|---|---|---|---|---|
| Baseline: giá trung bình | False | -0.0 | -0.0 | 49.6295 | 9.8147 | 15.7466 |
| Baseline: median theo dòng xe | False | 0.579 | 0.5741 | 28.3019 | 19.0817 | 9.5696 |
| Hồi quy tuyến tính | False | 0.7487 | 0.738 | 20.8565 | 26.369 | 7.4352 |
| kNN (k=10) | False | 0.768 | 0.7813 | 19.299 | 28.1803 | 6.8756 |
| Cây quyết định (sâu 12) | False | 0.788 | 0.7779 | 15.0133 | 36.3521 | 6.0388 |
| Random forest | True | 0.8579 | 0.8515 | 11.5744 | 45.4086 | 4.7171 |
| Gradient boosting | False | 0.8562 | 0.8532 | 12.6608 | 42.1651 | 4.9823 |

## Thí nghiệm: one-hot so với target encoding (validation)

| model | mã hóa | số cột | R2 | median_APE_% |
|---|---|---|---|---|
| Hồi quy tuyến tính | one-hot | 368 | 0.7505 | 20.0948 |
| Hồi quy tuyến tính | target encoding | 50 | 0.7439 | 22.9867 |
| Hồi quy tuyến tính | cả hai | 167 | 0.7487 | 21.3201 |
| Random forest | one-hot | 368 | 0.848 | 12.3396 |
| Random forest | target encoding | 50 | 0.8559 | 12.4918 |
| Random forest | cả hai | 167 | 0.8579 | 12.1333 |