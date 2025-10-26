#!/bin/bash
# Lambda Hello デプロイスクリプト

set -e

echo "================================"
echo "Lambda Hello - デプロイ開始"
echo "================================"

# SAM ビルド
echo ""
echo "📦 SAM ビルド中..."
sam build

# デプロイ
echo ""
echo "🚀 デプロイ中..."
sam deploy

# 出力確認
echo ""
echo "✅ デプロイ完了！"
echo ""
echo "📝 API URLを確認してください:"
echo "   aws cloudformation describe-stacks --stack-name lambda-hello --query 'Stacks[0].Outputs[?OutputKey==\`ApiUrl\`].OutputValue' --output text"
echo ""
echo "🧪 テスト実行例:"
echo "   export API_URL=\$(aws cloudformation describe-stacks --stack-name lambda-hello --query 'Stacks[0].Outputs[?OutputKey==\`ApiUrl\`].OutputValue' --output text)"
echo "   curl \$API_URL/health"


