def test_register_success(client, register_data):
    response = client.post('/account/register', json=register_data)

    assert response.status_code == 201

    data = response.json()
    
    assert 'id' in data, 'В ответе должен быть id пользователя'
    assert data['email'] == register_data['email'], 'Почты не совадают'
    assert data['login'] == register_data['login'], 'Логины не совпадают'
    assert 'password' not in data, 'Пароль не должен возвращаться клиенту'
    assert 'hashed_password' not in data, 'Пароль не должен возвращаться клиенту'


def test_register_validation_weak_password(client, register_data):
    response = client.post('/account/register', json={
        'email': register_data['email'],
        'login': register_data['login'],
        'password': 'weak'
    })

    # Ошибка 422 - Unprocessable entity - должен быть по умолчанию
    # при ошибке валидации в FastAPI Pydantic,
    # исправить тест, если это не так
    assert response.status_code == 422