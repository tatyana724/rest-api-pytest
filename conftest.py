"""
Фикстуры pytest для тестирования API
"""

import pytest
from api import APIClient


@pytest.fixture(scope="session")
def api_client():
    """Фикстура для создания клиента API"""
    client = APIClient()
    yield client


@pytest.fixture
def valid_post_data():
    """Фикстура с валидными данными для поста"""
    return {
        "title": "Test Post Title",
        "body": "This is a test post body content",
        "userId": 1
    }


@pytest.fixture
def valid_comment_data():
    """Фикстура с валидными данными для комментария"""
    return {
        "postId": 1,
        "name": "Test Comment",
        "email": "test@example.com",
        "body": "This is a test comment"
    }


@pytest.fixture
def valid_user_data():
    """Фикстура с валидными данными для пользователя"""
    return {
        "name": "Test User",
        "username": "testuser",
        "email": "testuser@example.com",
        "address": {
            "street": "Test Street",
            "suite": "Apt. 123",
            "city": "Test City",
            "zipcode": "12345"
        }
    }


@pytest.fixture
def invalid_post_data():
    """Фикстура с невалидными данными"""
    return {
        "title": "",
        "body": None,
        "userId": "invalid"
    }


@pytest.fixture
def auth_token():
    """Фикстура с тестовым токеном авторизации"""
    return "test_token_12345"