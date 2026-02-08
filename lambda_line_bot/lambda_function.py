import json
import os
import logging
import sys

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

# ログ設定
# Logging configuration
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 環境変数からチャンネルシークレットを取得
# Get Channel Secret from environment variables
CHANNEL_SECRET = os.getenv('CHANNEL_SECRET')
CHANNEL_ACCESS_TOKEN = os.getenv('CHANNEL_ACCESS_TOKEN')

# Webhook Handlerの初期化
# Initialize Webhook Handler
if CHANNEL_SECRET is None:
    logger.error('CHANNEL_SECRET is not defined.')
    sys.exit(1)

handler = WebhookHandler(CHANNEL_SECRET)

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    """
    メッセージイベントを処理する関数
    Process message event
    """
    logger.info(f"受信したメッセージイベント: {event}")
    # ここにメッセージ処理のロジックを追加できます
    # You can add message processing logic here

def lambda_handler(event, context):
    """
    AWS Lambdaハンドラー関数
    AWS Lambda handler function
    """
    # ヘッダーから署名を取得
    # Get signature from headers
    headers = event.get('headers', {})
    # API GatewayやLambda Function URLによってヘッダーのキーが大文字小文字異なる場合があるため対応
    # Handle case-insensitive header keys
    signature = headers.get('x-line-signature') or headers.get('X-Line-Signature')

    if signature is None:
        logger.error('x-line-signature header is missing.')
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Missing x-line-signature'})
        }

    # リクエストボディを取得
    # Get request body
    body = event.get('body', '')

    # ログにボディを記録
    # Log the body
    logger.info(f"Request body: {body}")

    try:
        # 署名を検証し、イベントをハンドリング
        # Verify signature and handle event
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error('Invalid signature. Please check your channel secret.')
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Invalid signature'})
        }
    except Exception as e:
        logger.error(f"Error handling event: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal Server Error'})
        }

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'OK'})
    }
