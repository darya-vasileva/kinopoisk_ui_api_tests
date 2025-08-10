# kinopoisk_ui_api_tests

## Финальный проект по автоматизации тестирования сайта Кинопоиск

### Шаги:
1. Склонировать проект 'git clone https://github.com/darya-vasileva/kinopoisk_ui_api_tests.git'
2. Установить все зависимости 'pip install > -r requirements.txt'
3. Запустить все тесты 'python -m pytest'
4. Запустить тесты в allure:
 - ui-тесты 'pytest --alluredir=allure_results test_ui.py'
 - api-тесты 'pytest --alluredir=allure_results test_api.py'
5. Сгенерировать и открыть отчет в браузере'allure serve allure_results'

### Стек:
- selenium
- requests
- pytest
- allure
- webdriver manager
- json

### Структура:
- ./config.py - настройки для тестов
- ./test_data.py - провайдер тестовых данных
- ./MainPage.py - методы для упрощения тестов
- ./requirements.txt - зависимости для установки
- ./test_api.py - api-тесты
- ./test_ui.py - ui-тесты

### Полезные ссылки:
- [Финальный проект по ручному тестированию сайта Кинопоиск] https://dariavslv.yonote.ru/share/105d7ad6-571b-425d-937b-cf6badfc8774
- [APi-документация] https://api.kinopoisk.dev/documentation

### Инструкция для получения токена API:
1. Перейти по адресу https://kinopoisk.dev/
2. Нажать на кнопку "Получить доступ к API"
3. Перейти в телеграм-бот "KinopoiskDev" (@kinopoiskdev_bot)
4. Выполнить указанные ботом условия
5. Бот получен, можно использовать его для дальнейших действий
