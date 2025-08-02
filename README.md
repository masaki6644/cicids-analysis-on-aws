# cicids-analysis-on-aws
本プロジェクトは、AWSとPythonを用いたサイバー攻撃ログの可視化パイプラインです。CICIDS2017のログを元に、Lambdaで攻撃種別ごとに分類 → S3保存 → Athenaによる分析 → Streamlitで可視化、という構成を実装。  中級〜上級では、FastAPIによる機械学習判定やSlack通知など、実務に近いサーバーレスアーキテクチャも構築します。
