import pandas as pd

# === 設定 ===
input_file = "/home/j23096om/data/Tuesday-WorkingHours.pcap_ISCX.csv"
output_file = "/home/j23096om/data/wednesday_subset.csv"

# === データ読み込み ===
df = pd.read_csv(input_file)

print(f"[読み込み完了] {df.shape[0]}行, {df.shape[1]}列")

# === 1. 定数列を削除 ===
const_cols = [col for col in df.columns if df[col].nunique() <= 1]
if const_cols:
    print(f"[定数列削除] {const_cols}")
    df = df.drop(columns=const_cols)

# === 2. 欠損率80%以上の列を削除 ===
missing_ratio = df.isnull().mean()
drop_missing = missing_ratio[missing_ratio >= 0.8].index.tolist()
if drop_missing:
    print(f"[欠損率80%以上削除] {drop_missing}")
    df = df.drop(columns=drop_missing)

# === 3. メタ情報列を削除（分類に使わない列） ===
meta_cols = ["Flow ID", "Source IP", "Destination IP", "Timestamp"]
drop_meta = [col for col in meta_cols if col in df.columns]
if drop_meta:
    print(f"[メタ列削除] {drop_meta}")
    df = df.drop(columns=drop_meta)

# === 4. 欠損を0で補完 ===
df = df.fillna(0)

# === 保存 ===
df.to_csv(output_file, index=False)
print(f"[保存完了] {output_file} -> {df.shape[0]}行, {df.shape[1]}列")

