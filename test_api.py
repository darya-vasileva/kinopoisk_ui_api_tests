import requests
import allure
from config import base_url_api, api_token
from test_data import movie_id, negative_id


@allure.epic('Расширенный поиск, раздел "Искать фильм"')
@allure.severity('normal')
@allure.story('Позитивные проверки')
@allure.feature('''Поиск id и названий фильмов 1999 года,
              с рейтингом КП от 8 до 10, жанр фантастика, страна США''')
def test_get_by_filters():
    my_params = {
        'page': '1',
        'limit': '10',
        'selectFields': ['id', 'name'],
        'year': '1999',
        'rating.kp': '8-10',
        'genres.name': 'фантастика',
        'countries.name': 'США'
    }
    response = requests.get(f"{base_url_api}/v1.4/movie?",
                            params=my_params, headers={"X-API-KEY": api_token})

    with allure.step('Проверяем статус-код и содержимое ответа'):
        assert response.status_code == 200
        data = response.json()

        assert 'docs' in data, "В ответе отсутствует ключ 'docs'"
        assert isinstance(data['docs'], list), '''
                                Ответ не содержит списка фильмов'''


@allure.feature('Вывод информации о фильме по id {movie_id}')
def test_get_movie_info_by_id():
    response = requests.get(f"{base_url_api}/v1.4/movie/{movie_id}",
                            headers={"X-API-KEY": api_token})

    with allure.step('Проверяем статус-код и наличие "id" в ответе'):
        assert response.status_code == 200
        data = response.json()
        assert 'id' in data, "Ответ не содержит id"


@allure.feature(
        'Вывод негативных рецензий пользователей на фильм {negative_id}')
def test_get_negative_review():
    my_params = {
        'page': '1',
        'limit': '10',
        'movieId': negative_id,
        'type': "Негативный"
    }
    response = requests.get(f"{base_url_api}/v1.4/review?", params=my_params,
                            headers={"X-API-KEY": api_token})

    with allure.step('Проверяем статус-код и содержимое ответа'):
        assert response.status_code == 200

        data = response.json()
        assert 'docs' in data, "В ответе отсутствует ключ 'docs'"
        assert isinstance(data['docs'], list), '''
                                Ответ не содержит списка фильмов'''

        for review in data['docs']:
            assert review.get('type') == 'Негативный', '''f"Найдена рецензия с
                    типом '{review.get('type')}', ожидался 'Негативный'"'''


@allure.story('Негативные проверки')
@allure.feature('Вывод информации о фильме через POST')
def test_get_movie_info_by_POST():
    response = requests.post(f"{base_url_api}/v1.4/movie/{movie_id}",
                             headers={"X-API-KEY": api_token})

    with allure.step('Проверяем статус-код'):
        assert response.status_code == 404


@allure.feature('Отправка запроса к API без токена авторизации')
def test_get_request_with_no_token():
    response = requests.get(f"{base_url_api}/v1.4/movie/{movie_id}")

    with allure.step('Проверяем статус-код'):
        assert response.status_code == 401
