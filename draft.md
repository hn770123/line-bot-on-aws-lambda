aws lambda で line bot を作成するリポジトリ

1. ログ機能：CloudWatch Logs　（保存期間を有限にしておく）
2. トリガー：関数 URL (Function URLs)　　API を作る場合、API Gateway ではなく Lambda 関数 URL を使います。
3. データベース：DynamoDB (オンデマンドではなくプロビジョニング)

AWS Budgets で「想定外の課金を防ぐアラート」

