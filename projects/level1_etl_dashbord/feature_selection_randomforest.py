import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.feature_selection import SelectFromModel
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report

# 1. CSV読み込み（パスは適宜変更）
df = pd.read_csv("/home/j23096om/data/Tuesday-WorkingHours.pcap_ISCX.csv")

# 2. 前処理
df.columns = df.columns.str.strip()  # 先頭・末尾の空白削除
df = df[df['Label'] != 'BENIGN']    # BENIGN除外（必要に応じて）
le = LabelEncoder()
df['Label'] = le.fit_transform(df['Label'])

X = df.drop(columns=['Label'])
y = df['Label']

# 無限大などをNaNに置換し、NaNを0埋め
X = X.replace([np.inf, -np.inf], np.nan).fillna(0)

# 3. 学習・テスト分割
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42)

# 4. ランダムフォレストで全部特徴量で学習
model_full = RandomForestClassifier(n_estimators=100, random_state=42)
model_full.fit(X_train, y_train)

# 5. 精度確認
y_pred = model_full.predict(X_test)
print("=== 全特徴量モデル ===")
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print(classification_report(y_test, y_pred))

# 6. 特徴量重要度確認
importances = model_full.feature_importances_
indices = np.argsort(importances)[::-1]

print("Top 10 Feature Importances:")
for i in indices[:10]:
    print(f"{X.columns[i]}: {importances[i]:.4f}")

# 7. SelectFromModel + CV で特徴量選択
thresholds = np.linspace(0.01, 0.1, 10)  # 重要度の閾値を色々試す
best_score = 0
best_thresh = None
best_model = None

print("\n=== SelectFromModel + CVで特徴量選択 ===")
for thresh in thresholds:
    selector = SelectFromModel(model_full, threshold=thresh, prefit=True)
    X_train_sel = selector.transform(X_train)
    if X_train_sel.shape[1] == 0:
        continue  # 特徴量0個はスキップ
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scores = cross_val_score(rf, X_train_sel, y_train, cv=cv, scoring='accuracy')
    mean_score = scores.mean()
    print(f"Threshold={thresh:.3f}, Selected Features={X_train_sel.shape[1]}, CV Accuracy={mean_score:.4f}")
    if mean_score > best_score:
        best_score = mean_score
        best_thresh = thresh
        best_model = rf
        best_selector = selector

# 8. ベスト閾値で選択した特徴量で再学習・評価
X_train_best = best_selector.transform(X_train)
X_test_best = best_selector.transform(X_test)
best_model.fit(X_train_best, y_train)
y_pred_best = best_model.predict(X_test_best)

print("\n=== 特徴量削減後モデル ===")
print(f"Selected Features: {X_train_best.shape[1]}")
print(f"Accuracy: {accuracy_score(y_test, y_pred_best):.4f}")
print(classification_report(y_test, y_pred_best))

