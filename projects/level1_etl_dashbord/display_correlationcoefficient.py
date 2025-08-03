import pandas as pd
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns

# CSV読み込みと前処理
csv_path = '/home/j23096om/data/Tuesday-WorkingHours.pcap_ISCX.csv'
df = pd.read_csv(csv_path, low_memory=False)
df = df[df['Label'] != 'BENIGN']
le = LabelEncoder()
df['Label'] = le.fit_transform(df['Label'])
df = df.fillna(0)

# 相関係数計算
corr = df.corr(numeric_only=True)

# ヒートマップ表示
plt.figure(figsize=(12, 10))
sns.heatmap(
    corr[['Label']].sort_values(by='Label', ascending=False),
    annot=True,
    cmap='coolwarm'
)
plt.title("Correlation with Label")
plt.tight_layout()
plt.show()

