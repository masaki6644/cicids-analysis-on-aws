import boto3
import pandas as pd
from io import StringIO

s3 = boto3.client("s3")

bucket_name = "masaki-ids-etl-bucket"
object_key = "wednesday_subset.csv"

def lambda_handler(event, context):
    # S3からオブジェクト取得
    response = s3.get_object(Bucket=bucket_name, Key=object_key)

    # CSVをDataFrameに読み込み
    csv_data = response["Body"].read().decode("utf-8")
    df = pd.read_csv(StringIO(csv_data))

    print(df.head())
    return {"status": "success", "rows": len(df)}
