import boto3
import pandas as pd
from io import StringIO

s3 = boto3.client("s3")

bucket_name = "masaki-ids-etl-bucket"
object_key = "wednesday_subset.csv"

def lambda_handler(event, context):
    # S3からオブジェクト取得
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    
    # CSVを読み込む
    csv_stream = StringIO(response["Body"].read().decode("utf-8"))
    
    df = pd.read_csv(csv_stream) 
    

    # Label列ごとに分割して件数を表示
    label_counts = df["Label"].value_counts()

    for label, count in label_counts.items():
        print(f"Label: {label}, Rows: {count}")

    return {
        "status": "success",
        "label_counts": label_counts.to_dict()
    }

