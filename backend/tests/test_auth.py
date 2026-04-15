async def test_register_success(client, register_data):
    response = await client.post('/auth/register', json=register_data)

    assert response.status_code == 201, 'Должен возвращаться код 201 (Created)'
    assert 'application/json' in response.headers['content-type'], 'Ответ должен быть формата json'

    data = response.json()
    
    assert 'access_token' in data, 'В ответе должен быть access_token'
    assert 'token_type' in data, 'В ответе должен быть указан тип токена token_type'

async def test_register_validation_weak_password(client, register_data):
    response = await client.post('/auth/register', json={
        'email': register_data['email'],
        'name': register_data['name'],
        'surname': register_data['surname'],
        'password': 'weak'
    })

    # Ошибка 422 - Unprocessable entity - должен быть по умолчанию
    # при ошибке валидации в FastAPI Pydantic,
    # исправить тест, если это не так
    assert response.status_code != 201, 'Нельзя создавать аккаунт с паролем меньше 6 символов'
    assert response.status_code == 422, 'Должен возвращаться код 422 (Unprocessable Content)'