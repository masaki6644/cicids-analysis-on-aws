import pandas as pd

df = pd.read_csv("/home/j23096om/data/Tuesday-WorkingHours.pcap_ISCX.csv")

# 欠損値の数を列ごとに確認
print(df.isnull().sum())

# 特定の列を削除（例）
df = df.drop(columns=["Flow Bytes/s"])

