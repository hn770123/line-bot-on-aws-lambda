# AWS Lambda デプロイ手順

このプロジェクトでは、GitHub Actions を使用して AWS Lambda への自動デプロイを行います。

## GitHub Actions によるデプロイ

`main` ブランチへのプッシュ、または手動実行 (workflow_dispatch) をトリガーとして、AWS Lambda 関数へのデプロイが実行されます。

### 事前準備 (GitHub Secrets の設定)

GitHub リポジトリの `Settings` > `Secrets and variables` > `Actions` に以下のシークレットを設定してください。

| Secret 名 | 説明 |
| --- | --- |
| `AWS_ACCESS_KEY_ID` | デプロイ用 IAM ユーザーのアクセスキー ID |
| `AWS_SECRET_ACCESS_KEY` | デプロイ用 IAM ユーザーのシークレットアクセスキー |
| `AWS_REGION` | AWS リージョン (例: `ap-northeast-1`) |
| `LAMBDA_FUNCTION_NAME` | デプロイ先の Lambda 関数名 |
| `CHANNEL_ACCESS_TOKEN` | LINE Messaging API のチャネルアクセストークン |
| `CHANNEL_SECRET` | LINE Messaging API のチャネルシークレット |

### デプロイの実行

1. `main` ブランチに変更をプッシュすると、自動的にデプロイが開始されます。
2. 手動で実行する場合は、GitHub の `Actions` タブから `Deploy to AWS Lambda` ワークフローを選択し、`Run workflow` をクリックします。

---

## (参考) 手動デプロイ手順

ローカル環境から手動でデプロイする場合の手順です。基本的には GitHub Actions を使用してください。

### 5.1 コードの準備
必要なライブラリ (LINE Messaging API SDK など) をインストールし、コードと一緒に zip 化します。

**例 (Python の場合):**
```bash
# プロジェクトディレクトリを作成
mkdir lambda_line_bot
cd lambda_line_bot

# ライブラリを現在のディレクトリにインストール
pip install line-bot-sdk -t .

# lambda_function.py を作成して、Bot のロジックを記述します
touch lambda_function.py

# zip ファイルを作成
zip -r function.zip .
```

### 5.2 アップロード
1. Lambda コンソールの「コード」タブを開きます。
2. 「アップロード元」ボタン → 「.zip ファイル」を選択します。
3. 作成した `function.zip` をアップロードし、「保存」をクリックします。
