def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200, 'Healthcheck должен возвращать статус 200'
    assert 'application/json' in response.headers['content-type'], "Healthcheck должен возвращать json"
    assert response.json() == {"status": "ok"}, 'Healthcheck должен возвращать json {"status": "ok"}'