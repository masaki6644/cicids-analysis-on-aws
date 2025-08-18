import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report

# CSV読み込み（ファイルパスは適宜変更してください）
df = pd.read_csv('/home/j23096om/data/Tuesday-WorkingHours.pcap_ISCX.csv')

# 列名の前後の空白を削除
df.columns = df.columns.str.strip()

# Labelが 'BENIGN' を除外し、エンコード
df = df[df['Label'] != 'BENIGN']
le = LabelEncoder()
df['Label'] = le.fit_transform(df['Label'])

# 説明変数・目的変数分割
X = df.drop(columns=['Label'])
y = df['Label']

# infをnanに置換し、欠損を0で埋める
X = X.replace([np.inf, -np.inf], np.nan)
X = X.fillna(0)

# 学習・テスト分割
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# モデル作成・学習
model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='mlogloss', missing=np.nan)
model.fit(X_train, y_train)

# 予測
y_pred = model.predict(X_test)

# 正解率表示
accuracy = accuracy_score(y_test, y_pred)
print(f"XGBoost Accuracy: {accuracy:.4f}")

# 詳細な分類レポート表示
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=le.classes_))

