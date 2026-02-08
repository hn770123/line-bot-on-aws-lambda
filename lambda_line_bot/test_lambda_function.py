import os
import unittest
import json
from unittest.mock import patch, MagicMock

# 環境変数を設定してからインポート
# Set environment variables before import
os.environ['CHANNEL_SECRET'] = 'test_channel_secret'
os.environ['CHANNEL_ACCESS_TOKEN'] = 'test_channel_access_token'

# lambda_functionをインポート
# Import lambda_function
try:
    from lambda_line_bot import lambda_function
except ImportError:
    import lambda_function
from linebot.v3.webhooks import MessageEvent, TextMessageContent

class TestLambdaFunction(unittest.TestCase):

    @patch('lambda_line_bot.lambda_function.handler')
    def test_lambda_handler_valid_signature(self, mock_handler):
        """
        有効な署名を持つリクエストのテスト
        Test request with valid signature
        """
        event = {
            'headers': {
                'x-line-signature': 'valid_signature'
            },
            'body': json.dumps({
                'events': [
                    {
                        'type': 'message',
                        'replyToken': 'reply_token',
                        'source': {
                            'userId': 'user_id',
                            'type': 'user'
                        },
                        'timestamp': 1462629479859,
                        'message': {
                            'type': 'text',
                            'id': 'message_id',
                            'text': 'Hello, world'
                        }
                    }
                ]
            })
        }
        context = {}

        # handler.handleが正常に実行されることをモック
        # Mock handler.handle to execute successfully
        mock_handler.handle.return_value = None

        response = lambda_function.lambda_handler(event, context)

        # ステータスコードが200であることを確認
        # Verify status code is 200
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(json.loads(response['body'])['message'], 'OK')

        # handler.handleが正しい引数で呼ばれたことを確認
        # Verify handler.handle called with correct arguments
        mock_handler.handle.assert_called_once_with(event['body'], 'valid_signature')

    @patch('lambda_line_bot.lambda_function.handler')
    def test_lambda_handler_invalid_signature(self, mock_handler):
        """
        無効な署名を持つリクエストのテスト
        Test request with invalid signature
        """
        from linebot.v3.exceptions import InvalidSignatureError

        event = {
            'headers': {
                'x-line-signature': 'invalid_signature'
            },
            'body': 'test_body'
        }
        context = {}

        # handler.handleがInvalidSignatureErrorを送出することをモック
        # Mock handler.handle to raise InvalidSignatureError
        mock_handler.handle.side_effect = InvalidSignatureError('Invalid signature')

        response = lambda_function.lambda_handler(event, context)

        # ステータスコードが400であることを確認
        # Verify status code is 400
        self.assertEqual(response['statusCode'], 400)
        self.assertEqual(json.loads(response['body'])['message'], 'Invalid signature')

    def test_lambda_handler_missing_signature(self):
        """
        署名がないリクエストのテスト
        Test request with missing signature
        """
        event = {
            'headers': {},
            'body': 'test_body'
        }
        context = {}

        response = lambda_function.lambda_handler(event, context)

        # ステータスコードが400であることを確認
        # Verify status code is 400
        self.assertEqual(response['statusCode'], 400)
        self.assertEqual(json.loads(response['body'])['message'], 'Missing x-line-signature')

if __name__ == '__main__':
    unittest.main()
