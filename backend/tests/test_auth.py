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

async def test_register_same_email(client, register_data):
    first_response = await client.post('/auth/register', json=register_data)

    assert first_response.status_code == 200

    second_response = await client.post('/auth/register', json=register_data)

    assert second_response.status_code != 201, 'Нельзя создавать два аккаунта на один email'
    assert second_response.status_code == 409, 'Должен возвращаться код 409 (Conflict)'


async def test_login_valid(client, register_data):
    response_register = await client.post('/auth/register', json=register_data)
    response_login = await client.post('/auth/login', json={
        'email': register_data['email'],
        'password': register_data['password']
    })
    
    assert response_login.status_code == 200
    assert 'application/json' in response_login.headers['content-type'], 'Ответ должен быть формата json'

    data = response_login.json()
    
    assert 'access_token' in data, 'В ответе должен быть access_token'
    assert 'token_type' in data, 'В ответе должен быть указан тип токена token_type'


async def test_login_invalid(client, register_data):
    response_register = await client.post('/auth/register', json=register_data)
    response_login = await client.post('/auth/login', json={
        'email': register_data['email'],
        'password': 'invalid_password'
    })

    assert response_login.status_code == 401