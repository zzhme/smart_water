import pytest
from app import app

def test_sql_injection_protection():
    """测试SQL注入防护"""
    with app.test_client() as client:
        response = client.get('/api/sensor/1%20OR%201=1')
        assert response.status_code != 500  # 不应引发服务器错误
        assert "error" in response.json  # 应返回可控错误