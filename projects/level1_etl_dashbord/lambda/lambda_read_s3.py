import boto3
import pandas as pd
from io import StringIO

s3 = boto3.client("s3")

bucket_name = "masaki-ids-etl-bucket"
object_key = "wednesday_subset.csv"

def lambda_handler(event, context):
    # S3からオブジェクト取得
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    
    # CSVを少しずつ読み込む
    csv_stream = StringIO(response["Body"].read().decode("utf-8"))
    chunk_iter = pd.read_csv(csv_stream, chunksize=100)  # 100行ずつ読み込む
    
    # 最初のチャンクだけ処理
    first_chunk = next(chunk_iter)
    print(first_chunk.head())  # 最初の数行だけ表示
    
    return {
        "status": "success",
        "rows_in_chunk": len(first_chunk)
    }

