import json
import logging

# ログ設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    AWS Lambda ハンドラー関数
    LINE プラットフォームからの Webhook イベントを受け取ります。
    """
    logger.info("Event: %s", json.dumps(event))

    # LINE プラットフォームへのレスポンス
    # 署名検証ロジックをここに追加してください

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
