import requests
from typing import Optional, Dict, Any, List
import time

#клиент для взаимодействия с REST API
class APIClient:
    
    URL = "https://jsonplaceholder.typicode.com" 
    
    def __init__(self, base_url: str = URL, timeout: int = 10):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    #установка токена авторизации
    def set_auth_token(self, token: str):
        self.session.headers.update({'Authorization': f'Bearer {token}'})
    
    #очистка заголовков авторизации
    def clear_auth(self):
        if 'Authorization' in self.session.headers:
            del self.session.headers['Authorization']
    
    #GET методы

    #получение списка постов
    def get_posts(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        try:
            response = self.session.get(
                f"{self.base_url}/posts", 
                params=params, 
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return self._handle_error(e)
    
    #получение поста по id
    def get_post(self, post_id: int) -> Dict[str, Any]:
        try:
            response = self.session.get(
                f"{self.base_url}/posts/{post_id}", 
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return self._handle_error(e)
    
    #получение комментариев
    def get_comments(self, post_id: Optional[int] = None) -> Dict[str, Any]:
        try:
            url = f"{self.base_url}/comments"
            params = {'postId': post_id} if post_id else None
            response = self.session.get(
                url, 
                params=params, 
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return self._handle_error(e)
    
    #получение списка пользователей
    def get_users(self) -> Dict[str, Any]:
        try:
            response = self.session.get(
                f"{self.base_url}/users", 
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return self._handle_error(e)
    
    #получение пользователя по id
    def get_user(self, user_id: int) -> Dict[str, Any]:
        try:
            response = self.session.get(
                f"{self.base_url}/users/{user_id}", 
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return self._handle_error(e)
    
    #POST методы

    #создание нового поста
    def create_post(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            response = self.session.post(
                f"{self.base_url}/posts", 
                json=data, 
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return self._handle_error(e)
    
    #создание нового комментария
    def create_comment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            response = self.session.post(
                f"{self.base_url}/comments", 
                json=data, 
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return self._handle_error(e)
    
    #создание нового пользователя
    def create_user(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            response = self.session.post(
                f"{self.base_url}/users", 
                json=data, 
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return self._handle_error(e)
    
    #PUT методы

    #полное обновление поста
    def update_post(self, post_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            response = self.session.put(
                f"{self.base_url}/posts/{post_id}", 
                json=data, 
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return self._handle_error(e)
    

    #полное обновление пользователя
    def update_user(self, user_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            response = self.session.put(
                f"{self.base_url}/users/{user_id}", 
                json=data, 
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return self._handle_error(e)
    
    #PATCH метод

    #частичное обновление поста
    def patch_post(self, post_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            response = self.session.patch(
                f"{self.base_url}/posts/{post_id}", 
                json=data, 
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return self._handle_error(e)
    
    #DELETE методы

    #удаление поста
    def delete_post(self, post_id: int) -> Dict[str, Any]:
        try:
            response = self.session.delete(
                f"{self.base_url}/posts/{post_id}", 
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return self._handle_error(e)
    
    #удаление пользователя
    def delete_user(self, user_id: int) -> Dict[str, Any]:
        try:
            response = self.session.delete(
                f"{self.base_url}/users/{user_id}", 
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return self._handle_error(e)
    
    #доп.методы

    #получение постов пользователя
    def get_posts_by_user(self, user_id: int) -> Dict[str, Any]:
        try:
            response = self.session.get(
                f"{self.base_url}/posts", 
                params={'userId': user_id}, 
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return self._handle_error(e)
    
    #получение списка альбомов
    def get_albums(self) -> Dict[str, Any]:
        try:
            response = self.session.get(
                f"{self.base_url}/albums", 
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return self._handle_error(e)
    
    #получение фотографий
    def get_photos(self, album_id: Optional[int] = None) -> Dict[str, Any]:
        try:
            url = f"{self.base_url}/photos"
            params = {'albumId': album_id} if album_id else None
            response = self.session.get(
                url, 
                params=params, 
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return self._handle_error(e)
    
    #получение списка задач
    def get_todos(self, user_id: Optional[int] = None) -> Dict[str, Any]:
        try:
            url = f"{self.base_url}/todos"
            params = {'userId': user_id} if user_id else None
            response = self.session.get(
                url, 
                params=params, 
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            return self._handle_error(e)
    
    #обработка ответа от сервера
    #возвращение словаря с данными ответа и мета-информацией
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        try:
            data = response.json() if response.content else None
        except ValueError:
            data = None
        
        return {
            'status_code': response.status_code,
            'data': data,
            'headers': dict(response.headers),
            'url': response.url,
            'ok': response.ok,
            'error': None
        }
    
    #обработка ошибок запроса
    def _handle_error(self, error: Exception) -> Dict[str, Any]:
        return {
            'status_code': 500,
            'data': None,
            'headers': {},
            'url': '',
            'ok': False,
            'error': str(error)
        }