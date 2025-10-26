import json

def lambda_handler(event, context):
    """
    Lambda関数のエントリーポイント
    
    Args:
        event: API Gatewayから渡されるイベントデータ
        context: Lambdaランタイム情報
    
    Returns:
        HTTPレスポンス形式の辞書
    """
    # API Gateway HTTP API (v2) の形式でパスとメソッドを取得
    path = event.get("rawPath", event.get("path", ""))
    method = event.get("requestContext", {}).get("http", {}).get("method", 
              event.get("httpMethod", ""))
    
    print(f"[Lambda] Received: {method} {path}")
    print(f"[Lambda] Full event: {json.dumps(event)}")
    
    # /health エンドポイント
    if path == "/health" and method == "GET":
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "status": "ok",
                "message": "Lambda is running!",
                "path": path,
                "method": method
            })
        }
    
    # ルートパス
    elif path == "/" and method == "GET":
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": "Welcome to Lambda Hello!",
                "endpoints": ["/health"]
            })
        }
    
    # 404
    else:
        return {
            "statusCode": 404,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "error": "not found",
                "path": path,
                "method": method
            })
        }


