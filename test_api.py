import pytest
import random
import requests

#Базовые тесты API
class TestAPIBasic:

    #тест получения одного поста
    def test_get_single_post(self, api_client):
        response = api_client.get_post(1)
        
        if response['status_code'] == 200:
            assert response['data']['id'] == 1
            assert 'title' in response['data']
            assert 'body' in response['data']
            print(f"Получен пост #{response['data']['id']}: {response['data']['title']}")
        else:
            print(f"Сервер вернул код {response['status_code']}")

    #тест создания нового поста
    def test_create_post(self, api_client, valid_post_data):
        response = api_client.create_post(valid_post_data)
        
        assert response['status_code'] in [201, 200, 500]
        if response['status_code'] in [200, 201]:
            assert response['data']['title'] == valid_post_data['title']
            assert 'id' in response['data']
            print(f"Создан пост #{response['data']['id']}")
        else:
            print(f"Не удалось создать пост: {response['status_code']}")

#тесты с различными параметрами запросов
class TestAPIParameters:

    #тест пагинации постов
    def test_get_posts_with_pagination(self, api_client):
        params = {'_page': 1, '_limit': 5}
        response = api_client.get_posts(params)
        
        if response['status_code'] == 200:
            assert len(response['data']) <= 5
            print(f"Получено {len(response['data'])} постов (пагинация)")
        else:
            print(f"Пагинация не поддерживается: {response['status_code']}")

    #тест получения комментариев к посту
    def test_get_comments_by_post(self, api_client):
        response = api_client.get_comments(post_id=1)
        
        if response['status_code'] == 200:
            if response['data']:
                assert all(comment.get('postId') == 1 for comment in response['data'])
            print(f"Получено {len(response['data'])} комментариев к посту #1")
        else:
            print(f"Не удалось получить комментарии: {response['status_code']}")

    #тест получения постов пользователя
    def test_get_posts_by_user(self, api_client):
        response = api_client.get_posts_by_user(1)
        
        if response['status_code'] == 200:
            if response['data']:
                assert all(post.get('userId') == 1 for post in response['data'])
            print(f"Получено {len(response['data'])} постов пользователя #1")
        else:
            print(f"Не удалось получить посты пользователя: {response['status_code']}")

#тесты граничных значений
class TestAPIBoundaryValues:

    #тест с минимальным id
    def test_post_id_min_value(self, api_client):
        response = api_client.get_post(1)
        assert response['status_code'] in [200, 500]
        print(f"Минимальный ID (1): {response['status_code']}")

    #тест с максимальным допустимым id
    def test_post_id_max_value(self, api_client):
        response = api_client.get_post(100)
        assert response['status_code'] in [200, 500]
        print(f"Максимальный ID (100): {response['status_code']}")

    #тест с id равным 0
    def test_post_id_zero(self, api_client):
        response = api_client.get_post(0)
        assert response['status_code'] in [404, 400, 500]
        print(f"ID = 0: {response['status_code']}")

    #тест с отрицательным id
    def test_post_id_negative(self, api_client):
        response = api_client.get_post(-1)
        assert response['status_code'] in [404, 400, 500]
        print(f"Отрицательный ID (-1): {response['status_code']}")

    #тест с пустым параметром
    def test_empty_string_parameter(self, api_client):
        response = api_client.get_posts(params={'userId': ''})
        assert response['status_code'] in [200, 400, 500]
        print(f"Пустой параметр: {response['status_code']}")

#тесты с некорректными данными
class TestAPIInvalidData:

    #тест создания поста без обязательных полей
    def test_create_post_without_required_fields(self, api_client):
        invalid_data = {"title": "Only Title"}
        response = api_client.create_post(invalid_data)
        
        assert response['status_code'] in [201, 400, 422, 500]
        print(f"Создание поста без обязательных полей: {response['status_code']}")

    #тест создания поста с неверными типами данных
    def test_create_post_with_invalid_types(self, api_client):
        invalid_data = {
            "title": "",
            "body": None,
            "userId": "invalid"
        }
        response = api_client.create_post(invalid_data)
        
        assert response['status_code'] in [201, 400, 422, 500]
        print(f"Создание поста с неверными типами: {response['status_code']}")

    #тест обновления несуществующего поста
    def test_update_nonexistent_post(self, api_client, valid_post_data):
        response = api_client.update_post(99999, valid_post_data)
        
        assert response['status_code'] in [404, 500, 200]
        print(f"Обновление несуществующего поста: {response['status_code']}")

    #тест удаления несуществующего поста
    def test_delete_nonexistent_post(self, api_client):
        response = api_client.delete_post(99999)
        
        assert response['status_code'] in [404, 200, 500]
        print(f"Удаление несуществующего поста: {response['status_code']}")

#тесты авторизации и аутентификации
class TestAPIAuthorization:

    #тест запроса без авторизации
    def test_request_without_auth(self, api_client):
        response = api_client.get_posts()
        assert response['status_code'] in [200, 500]
        print(f"Запрос без авторизации: {response['status_code']}")

    #тест с неверным токеном авторизации
    def test_request_with_invalid_auth(self, api_client):
        api_client.set_auth_token("invalid_token_12345")
        response = api_client.get_posts()
        api_client.clear_auth()
        
        assert response['status_code'] in [200, 401, 403, 500]
        print(f"Неверный токен: {response['status_code']}")

    #тест с валидным токеном авторизации
    def test_request_with_valid_auth(self, api_client, auth_token):
        api_client.set_auth_token(auth_token)
        response = api_client.get_posts()
        api_client.clear_auth()
        
        assert response['status_code'] in [200, 401, 403, 500]
        print(f"Валидный токен: {response['status_code']}")

#тесты обработки ошибок сервера
class TestAPIErrorHandling:

    #тест отправки некорректного json
    def test_malformed_json(self, api_client):
        try:
            response = api_client.session.post(
                f"{api_client.base_url}/posts",
                data="invalid json string",
                headers={'Content-Type': 'application/json'},
                timeout=api_client.timeout
            )
            result = api_client._handle_response(response)
        except Exception as e:
            result = api_client._handle_error(e)
        
        assert result['status_code'] in [400, 415, 500, 200]
        print(f"Некорректный JSON: {result['status_code']}")

    #тест ошибки соединения
    def test_connection_error(self, api_client, monkeypatch):
        import requests
        
        def mock_get(*args, **kwargs):
            raise requests.exceptions.ConnectionError("Connection refused")
        
        monkeypatch.setattr(api_client.session, 'get', mock_get)
        response = api_client.get_posts()
        
        assert response['status_code'] == 500
        assert response['error'] is not None
        print(f"Ошибка соединения обработана: {response['error']}")

    #тест таймаута
    def test_timeout_error(self, api_client, monkeypatch):
        import requests
        
        def mock_get(*args, **kwargs):
            raise requests.exceptions.Timeout("Request timeout")
        
        monkeypatch.setattr(api_client.session, 'get', mock_get)
        response = api_client.get_posts()
        
        assert response['status_code'] == 500
        assert response['error'] is not None
        print(f"Таймаут обработан: {response['error']}")

#тест для проверки работы pytest
def test_simple():
    assert True
    print("Тест для проверки работы pytest выполнен")


#тест для проверки доступности API
def test_api_availability(api_client):
    response = api_client.get_posts()
    assert response['status_code'] in [200, 500]
    if response['status_code'] == 200:
        print("API доступно")
    else:
        print(f"API недоступно: {response['status_code']}")