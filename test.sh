#!/bin/bash
# Lambda Hello テストスクリプト

set -e

# API URLを取得
API_URL=$(aws cloudformation describe-stacks \
  --stack-name lambda-hello \
  --query 'Stacks[0].Outputs[?OutputKey==`ApiUrl`].OutputValue' \
  --output text 2>/dev/null)

if [ -z "$API_URL" ]; then
  echo "❌ エラー: lambda-helloスタックが見つかりません"
  echo "   先に 'sam deploy' を実行してください"
  exit 1
fi

echo "================================"
echo "Lambda Hello - 動作確認"
echo "================================"
echo "API URL: $API_URL"
echo ""

# Test 1: /health
echo "🧪 Test 1: GET /health"
response=$(curl -s -w "\n%{http_code}" "${API_URL}health")
body=$(echo "$response" | head -n -1)
status=$(echo "$response" | tail -n 1)

echo "Status: $status"
echo "Body: $body"

if [ "$status" = "200" ]; then
  echo "✅ PASS"
else
  echo "❌ FAIL (expected 200, got $status)"
fi
echo ""

# Test 2: /
echo "🧪 Test 2: GET /"
response=$(curl -s -w "\n%{http_code}" "${API_URL}")
body=$(echo "$response" | head -n -1)
status=$(echo "$response" | tail -n 1)

echo "Status: $status"
echo "Body: $body"

if [ "$status" = "200" ]; then
  echo "✅ PASS"
else
  echo "❌ FAIL (expected 200, got $status)"
fi
echo ""

# Test 3: 404
echo "🧪 Test 3: GET /not-found (404確認)"
response=$(curl -s -w "\n%{http_code}" "${API_URL}not-found")
body=$(echo "$response" | head -n -1)
status=$(echo "$response" | tail -n 1)

echo "Status: $status"
echo "Body: $body"

if [ "$status" = "404" ]; then
  echo "✅ PASS"
else
  echo "❌ FAIL (expected 404, got $status)"
fi
echo ""

echo "================================"
echo "テスト完了"
echo "================================"

