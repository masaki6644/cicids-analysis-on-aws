import pandas as pd
import numpy as np
import json
from pathlib import Path

# === 設定 ===
input_file  = "/home/j23096om/data/Tuesday-WorkingHours.pcap_ISCX.csv"
output_file = "/home/j23096om/data/wednesday_subset.csv"
label_map_file = "/home/j23096om/data/label_map.json"  # マッピングを保存しておくと再現性が高い

# === 1. 読み込み ===
df = pd.read_csv(input_file, low_memory=False)
print(f"[読み込み完了] {df.shape[0]} 行, {df.shape[1]} 列")

# === 2. 列名トリム（先頭・末尾の空白除去） ===
df.columns = df.columns.str.strip()

# === 3. 定数列削除（情報量が無い列） ===
const_cols = [col for col in df.columns if df[col].nunique() <= 1]
if const_cols:
    print(f"[定数列削除] {const_cols}")
    df = df.drop(columns=const_cols)

# === 4. 欠損率の高い列を削除（80%以上を閾値に） ===
missing_ratio = df.isnull().mean()
drop_missing = missing_ratio[missing_ratio >= 0.8].index.tolist()
if drop_missing:
    print(f"[欠損率80%以上削除] {drop_missing}")
    df = df.drop(columns=drop_missing)

# === 5. メタ列削除（解析に直接使わないもの） ===
meta_cols = ["Flow ID", "Source IP", "Destination IP", "Timestamp"]
drop_meta = [col for col in meta_cols if col in df.columns]
if drop_meta:
    print(f"[メタ列削除] {drop_meta}")
    df = df.drop(columns=drop_meta)

# === 6. 欠損/inf の処理 ===
# inf を NaN にし、そのあと 0 で埋める（初級・中級向けの簡易処理）
df = df.replace([np.inf, -np.inf], np.nan)
print(f"[欠損合計(処理前)] {df.isnull().sum().sum()}")
df = df.fillna(0)
print(f"[欠損合計(処理後)] {df.isnull().sum().sum()}")

# === 7. ラベル列の確認・ラベル付け ===
if 'Label' not in df.columns:
    raise KeyError("Label 列が見つかりません。列名を確認してください。")

# (A) 攻撃種別の一覧（元の文字列ラベル）を取得して表示
attack_types = pd.Series(df['Label'].unique()).tolist()
print("[攻撃種別一覧（raw）]:", attack_types)

# (B) マッピング（再現性確保のため保存）
#    - AttackCategoryID: 各種攻撃と BENIGN を整数IDにマップ（BENIGN=0 を優先）
#    - BinaryLabel: BENIGN=0, 攻撃=1 の2値ラベル
# 並び替えして BENIGN を 0 に固定したい場合の例：
unique_labels = sorted([lab for lab in attack_types if lab != 'BENIGN'])
label_map = {'BENIGN': 0}
for i, lab in enumerate(unique_labels, start=1):
    label_map[lab] = i

# マッピングを DataFrame に適用
df['AttackCategoryID'] = df['Label'].map(label_map)
df['BinaryLabel'] = df['Label'].apply(lambda x: 0 if x == 'BENIGN' else 1)

# 保存用ディレクトリ作成
Path(output_file).parent.mkdir(parents=True, exist_ok=True)
# マッピングも JSON に保存
with open(label_map_file, 'w', encoding='utf-8') as f:
    json.dump(label_map, f, ensure_ascii=False, indent=2)

print(f"[ラベルマップ保存] {label_map_file}")
print("[AttackCategoryID のサンプル]")
print(df[['Label', 'AttackCategoryID', 'BinaryLabel']].head())

# === 8. 保存 ===
df.to_csv(output_file, index=False)
print(f"[保存完了] {output_file} -> {df.shape[0]} 行, {df.shape[1]} 列")

