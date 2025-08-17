import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
import boto3

# === S3 から CSV を読み込む ===
bucket_name = "masaki-ids-etl-bucket"

# 攻撃種別ごとの件数 CSV
key_bar = "analysis/label_counts/a4a71a79-84dc-41f8-a3d0-26a4bcae4555.csv"

# 正常 vs 攻撃 CSV
key_pie = "analysis/type_counts/63a903e7-e273-4160-96d7-a35d820911a9.csv"

s3 = boto3.client("s3")

def read_s3_csv(bucket, key):
    response = s3.get_object(Bucket=bucket, Key=key)
    csv_str = response['Body'].read().decode('utf-8')
    return pd.read_csv(StringIO(csv_str))

# データ読み込み
df_bar = read_s3_csv(bucket_name, key_bar)
df_pie = read_s3_csv(bucket_name, key_pie)

# === 1. 攻撃種別ごとの棒グラフ ===
st.title("IDS 攻撃種別別件数")

fig, ax = plt.subplots()
ax.bar(df_bar['Label'], df_bar['count'])
ax.set_xlabel("攻撃種別")
ax.set_ylabel("件数")
ax.set_xticklabels(df_bar['Label'], rotation=45, ha='right')
st.pyplot(fig)

# === 2. 正常 vs 攻撃の割合円グラフ ===
st.title("正常通信 vs 攻撃通信")

fig2, ax2 = plt.subplots()
ax2.pie(df_pie['count'], labels=df_pie['Type'], autopct="%1.1f%%", startangle=90)
st.pyplot(fig2)

