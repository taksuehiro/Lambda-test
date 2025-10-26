#!/usr/bin/env python3
"""
ローカルテスト用スクリプト
Lambdaハンドラをローカルで直接実行して動作確認
"""

import json
from app import lambda_handler


def test_handler():
    """各エンドポイントをテスト"""
    
    print("=" * 60)
    print("Lambda Handler ローカルテスト")
    print("=" * 60)
    
    # テストケース1: /health
    print("\n[Test 1] GET /health")
    event1 = {
        "rawPath": "/health",
        "requestContext": {
            "http": {
                "method": "GET",
                "path": "/health"
            }
        }
    }
    response1 = lambda_handler(event1, None)
    print(f"Status: {response1['statusCode']}")
    print(f"Body: {response1['body']}")
    assert response1['statusCode'] == 200
    print("✅ PASS")
    
    # テストケース2: /
    print("\n[Test 2] GET /")
    event2 = {
        "rawPath": "/",
        "requestContext": {
            "http": {
                "method": "GET",
                "path": "/"
            }
        }
    }
    response2 = lambda_handler(event2, None)
    print(f"Status: {response2['statusCode']}")
    print(f"Body: {response2['body']}")
    assert response2['statusCode'] == 200
    print("✅ PASS")
    
    # テストケース3: 404
    print("\n[Test 3] GET /not-found (404エラー)")
    event3 = {
        "rawPath": "/not-found",
        "requestContext": {
            "http": {
                "method": "GET",
                "path": "/not-found"
            }
        }
    }
    response3 = lambda_handler(event3, None)
    print(f"Status: {response3['statusCode']}")
    print(f"Body: {response3['body']}")
    assert response3['statusCode'] == 404
    print("✅ PASS")
    
    print("\n" + "=" * 60)
    print("全てのテストが成功しました！")
    print("=" * 60)


if __name__ == "__main__":
    test_handler()

