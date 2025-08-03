import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import numpy as np

# 1 CSV読み込み
csv_path = '/home/j23096om/data/Tuesday-WorkingHours.pcap_ISCX.csv'
df = pd.read_csv(csv_path)

# 2. 列名の空白削除（もし空白がある場合）
df.columns = df.columns.str.strip()

# 3. 不要な行削除（ここではBENIGNを除く）
df = df[df['Label'] != 'BENIGN']

# 4. NaNやinfの処理（infをNaNに置換して0埋め）
df.replace([np.inf, -np.inf], np.nan, inplace=True)
df = df.fillna(0)

# 5. ラベルエンコード（目的変数の加工）
le = LabelEncoder()
df['Label'] = le.fit_transform(df['Label'])

# 6. 説明変数と目的変数に分割
X = df.drop(columns=['Label'])
y = df['Label']

# 7. 学習・評価データに分割
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 8. モデル学習など続く
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)


# 予測
y_pred = model.predict(X_test)

# 正解率を表示
acc = accuracy_score(y_test, y_pred)
print(f"Random Forest Accuracy: {acc:.4f}")

# 重要度の上位10件を表示
importances = model.feature_importances_
indices = importances.argsort()[::-1]

print("\nFeature Importances (Top 10):")
for i in indices[:10]:
    print(f"{X.columns[i]}: {importances[i]:.4f}")

