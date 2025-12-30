"""
/hello エンドポイントのユニットテスト
正常系のレスポンス検証を含む
"""

from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_hello_endpoint():
    """
    /hello エンドポイントが正しいレスポンスを返すことを確認
    
    正常系:
    - ステータスコードが200であること
    - レスポンスボディに"message"キーが含まれること
    - メッセージの内容が期待通りであること
    """
    response = client.get("/hello")
    
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json() == {"message": "hello, world!"}


def test_hello_endpoint_response_structure():
    """
    /hello エンドポイントのレスポンス構造を検証
    
    正常系:
    - レスポンスがJSON形式であること
    - Content-Typeが正しく設定されていること
    """
    response = client.get("/hello")
    
    assert response.status_code == 200
    # 大文字小文字を区別しないヘッダー比較
    content_type = response.headers.get("content-type", "")
    assert "application/json" in content_type
    
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) == 1
