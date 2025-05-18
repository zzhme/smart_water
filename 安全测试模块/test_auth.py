def test_api_authentication():
    # 测试未授权访问
    response = client.get('/api/sensor_data')
    assert response.status_code == 401
    
    # 测试带Token访问
    headers = {'Authorization': f'Bearer {valid_token}'}
    response = client.get('/api/sensor_data', headers=headers)
    assert response.status_code == 200