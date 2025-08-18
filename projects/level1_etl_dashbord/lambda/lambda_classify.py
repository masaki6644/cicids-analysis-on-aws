import boto3
import pandas as pd
from io import StringIO

s3 = boto3.client("s3")

bucket_name = "masaki-ids-etl-bucket"
object_key = "Wednesday-workingHours.pcap_ISCX.csv"

def lambda_handler(event, context):
    # S3からオブジェクト取得
    response = s3.get_object(Bucket=bucket_name, Key=object_key)

    # CSVを読み込む
    csv_stream = StringIO(response["Body"].read().decode("utf-8"))

    df = pd.read_csv(csv_stream)

    # 列名のクリーンアップ
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.replace(" ", "_")


    # Label列ごとに分割
    for label, group in df.groupby("Label"):
        # 攻撃種別ごとに保存先フォルダを作る
        safe_label = label.replace(" ", "_").replace("/", "_")  # フォルダ名に使えない文字を置換
        output_key = f"processed/{safe_label}/data.csv"

        # DataFrameをCSVに変換
        csv_buffer = StringIO()
        group.to_csv(csv_buffer, index=False)

        # S3へアップロード
        s3.put_object(
            Bucket=bucket_name,
            Key=output_key,
            Body=csv_buffer.getvalue()
        )
        print(f"Uploaded {len(group)} rows to s3://{bucket_name}/{output_key}")

    return {"status": "success", "labels": df["Label"].unique().tolist()}
