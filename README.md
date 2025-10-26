# Lambda Hello - 最小構成検証プロジェクト

Lambdaの「基本動作＋API Gateway経由の動き」を最小構成で理解するためのプロジェクトです。

## 🎯 目的

- ✅ 純粋なPythonコードを直接Lambdaにデプロイ
- ✅ `/health` エンドポイントにcurlで動作確認
- ✅ Lambdaハンドラの呼び出しを体感
- ✅ フロント不要、CLIとcurlのみで完結

## 📁 構成

```
lambda-hello/
├── app.py              # Lambdaハンドラ
├── requirements.txt    # 依存パッケージ（今回は空）
├── template.yaml       # SAMテンプレート
└── README.md          # このファイル
```

## 🚀 デプロイ手順

### 前提条件

1. **AWS CLI** がインストール済み
   ```bash
   aws --version
   ```

2. **AWS SAM CLI** がインストール済み
   ```bash
   sam --version
   ```

3. **AWS認証情報** が設定済み
   ```bash
   aws configure
   ```

### デプロイ

```bash
# 1. プロジェクトディレクトリに移動
cd lambda-hello

# 2. SAMビルド（初回のみ）
sam build

# 3. デプロイ（初回はガイド付き）
sam deploy --guided

# 2回目以降は以下でOK
sam deploy
```

#### デプロイ時の入力例

```
Stack Name [lambda-hello]: lambda-hello
AWS Region [ap-northeast-1]: ap-northeast-1
Confirm changes before deploy [Y/n]: n
Allow SAM CLI IAM role creation [Y/n]: Y
Disable rollback [y/N]: N
HelloFunction may not have authorization defined, Is this okay? [y/N]: y
Save arguments to configuration file [Y/n]: Y
SAM configuration file [samconfig.toml]: 
SAM configuration environment [default]: 
```

## 🧪 動作確認

デプロイが完了すると、`Outputs` にAPI URLが表示されます。

```bash
# 出力例
CloudFormation outputs from deployed stack
---------------------------------------------------------------------------------
Outputs
---------------------------------------------------------------------------------
Key                 ApiUrl
Description         API Gateway endpoint URL
Value               https://xxxxxxxxxx.execute-api.ap-northeast-1.amazonaws.com/
---------------------------------------------------------------------------------
```

### curlでテスト

```bash
# 環境変数にセット
export API_URL="https://xxxxxxxxxx.execute-api.ap-northeast-1.amazonaws.com"

# 1. ヘルスチェック
curl $API_URL/health

# 期待する出力:
# {"status": "ok", "message": "Lambda is running!", "path": "/health", "method": "GET"}

# 2. ルートパス
curl $API_URL/

# 期待する出力:
# {"message": "Welcome to Lambda Hello!", "endpoints": ["/health"]}

# 3. 存在しないパス（404エラー）
curl $API_URL/not-found

# 期待する出力:
# {"error": "not found", "path": "/not-found", "method": "GET"}
```

### ログ確認

```bash
# Lambda関数のログをリアルタイム表示
sam logs -n HelloFunction --tail

# または AWS CLI で確認
aws logs tail /aws/lambda/lambda-hello-function --follow
```

## 🔍 ハンドラの挙動を理解する

### eventオブジェクトの中身

API Gatewayから渡される`event`の構造:

```python
{
    "rawPath": "/health",
    "requestContext": {
        "http": {
            "method": "GET",
            "path": "/health",
            ...
        },
        ...
    },
    "headers": { ... },
    "queryStringParameters": { ... },
    ...
}
```

### レスポンス形式

Lambda関数は以下の形式でレスポンスを返す:

```python
{
    "statusCode": 200,
    "headers": {
        "Content-Type": "application/json"
    },
    "body": "JSON文字列"
}
```

## 🧹 クリーンアップ

```bash
# スタック削除
sam delete

# または
aws cloudformation delete-stack --stack-name lambda-hello
```

## 📝 次のステップ

このプロジェクトをベースに以下を試してみましょう：

1. **POSTリクエスト処理** - `event["body"]` からJSONを読み取る
2. **環境変数** - `os.environ` で設定値を読む
3. **DynamoDB連携** - boto3を使ってデータ保存
4. **外部ライブラリ追加** - requirements.txtに追記してビルド
5. **エラーハンドリング** - try-exceptで例外処理

## 💡 トラブルシューティング

### デプロイエラー

```bash
# キャッシュクリア
sam build --use-container

# ログ確認
sam logs -n HelloFunction --tail
```

### APIが404を返す

- API URLが正しいか確認
- パスは `/health` （スラッシュ必須）
- HTTPメソッドはGETか確認

### 権限エラー

```bash
# IAMロールが正しく作成されているか確認
aws iam list-roles | grep lambda-hello
```

## 📚 参考リンク

- [AWS Lambda - Python](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python.html)
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html)
- [API Gateway - HTTP API](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api.html)

