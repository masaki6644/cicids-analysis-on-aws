# Level 1: ETL + Dashboard プロジェクト

## 概要
CICIDS2017データセットをETL処理し、攻撃種別ごとの傾向を可視化するダッシュボードを構築するプロジェクト。

- 技術スタック: Python, AWS (S3, Lambda, Glue, Athena), Streamlit
- 目的: セキュリティログ分析の基礎を学習

## プロジェクト構成

```
project-root/projects/level1_etl_dashboard/
│
├── lambda/ # CSVフィルタリング処理（Python　on AWS）
├── streamlit_app/ # 可視化ダッシュボード
└── README.md 
```

## 実行手順

1. **データ準備**  
   CICIDS2017のCSVをダウンロードし、`data/processed/` に保存。

2. **S3環境構築**  
   `cicids-etl-bucket` を作成し、CSVをアップロード。

3. **Lambda関数作成**  
   - `lambda/handler.py` をデプロイ。  
   - S3トリガーで攻撃種別ごとにデータを振り分け。  

4. **Athena設定**  
   - Glue Crawlerでカタログ作成。  
   - AthenaでSQLクエリ実行。  

5. **可視化**  
   - `streamlit_app/app.py` を実行  
   - `streamlit run app.py`  
   - 攻撃分布を棒グラフ・円グラフで表示。  

6. **成果物**  
   - ETLパイプライン（S3 + Lambda + Athena）  
   - 可視化ダッシュボード（Streamlit）
