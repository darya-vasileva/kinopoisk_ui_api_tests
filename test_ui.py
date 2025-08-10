import pytest
from selenium import webdriver
import allure
from test_data import (movie_name,
                       actor_name,
                       release_year,
                       year,
                       country,
                       wrong_title)

from MainPage import KinopoiskAdvancedSearch
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


@allure.epic('Расширенный поиск, раздел "Искать фильм"')
@allure.severity('normal')
class TestKinopoiskSearch:

    @pytest.fixture(autouse=True)
    def driver(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(4)
        self.driver.maximize_window()
        self.search = KinopoiskAdvancedSearch(self.driver)
        yield
        self.driver.quit()

    @allure.story('Валидные проверки')
    @allure.feature('Поиск по полному названия фильма, например {movie_name}')
    def test_movie_search(self):
        self.search.open_advanced_search()
        self.search.perform_search(
            search_value=movie_name,
            field_locator=(By.ID, 'find_film'),
            button_locator=(
                By.CSS_SELECTOR, 'input[class="el_18 submit nice_button"]'))

        with allure.step('Проверяем первый фильм из списка выдачи'):
            first_result = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'info')))

            title_element = first_result.find_element(
                By.CSS_SELECTOR, "a[href*='/film/']")
            actual_title = title_element.text.strip()

            assert movie_name.lower() in actual_title.lower(), f'''
            Ожидалось {movie_name}, получено "{actual_title}"'''

    @allure.feature('Поиск по имени актера/актрисы, {actor_name}')
    def test_actor_search(self):
        self.search.open_advanced_search()
        self.search.perform_search(
            search_value=actor_name,
            field_locator=(By.ID, 'find_people'),
            button_locator=(
                By.CSS_SELECTOR, 'input[class="el_8 submit nice_button"]'))

        with allure.step('''Проверяем имя актера на открывшейся странице
                    по двум локаторам(в зависимости от выданной страницы)'''):

            def responsive_elements(self, actor_name, actor_header):
                if actor_header:
                    actor_header1 = (
                        By.CSS_SELECTOR, 'h1[data-tid="f22e0093"]')
                    actor_header2 = (
                        By.CSS_SELECTOR, '[data-type="person"]')
                else:
                    actor_header1 = (
                        By.CSS_SELECTOR, 'h1[data-tid="f22e0093"]')
                    actor_header2 = (
                        By.CSS_SELECTOR, '[data-type="person"]')

                element1 = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located(actor_header1))
                element2 = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located(actor_header2))

                assert element1.text == actor_name
                assert element2.text == actor_name

    @allure.feature('Ввод валидного года, {release_year}')
    def test_year_search(self):
        self.search.open_advanced_search()
        self.search.perform_search(
            search_value=release_year,
            field_locator=(By.ID, 'year'),
            button_locator=(
                By.CSS_SELECTOR, 'input[class="el_18 submit nice_button"]'))

        with allure.step('Проверяем год выпуска первой позиции в списке'):

            first_result = WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'info')))

            year_element = first_result.find_element(
                By.CSS_SELECTOR, "span[class='year']").text
            actual_year = year_element.split('–')[0].strip()

            assert release_year in actual_year, f"""
            Ожидался {release_year} год, получено {actual_year}"""

    @allure.feature('Поиск по двум параметрам, {year} + {country}')
    def test_two_parameters(self):
        self.search.open_advanced_search()
        self.search.search_by_several_parameters(
            field_locator1=(By.ID, 'year'),
            field_locator2=(By.ID, 'country'),
            search_value1=year,
            search_value2=country,
            button_locator=(
                By.CSS_SELECTOR, 'input[class="el_18 submit nice_button"]'))

        with allure.step('Проверяем год и страну в первой позиции списка'):
            first_result = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR, 'div[class="info"]')))

            year_text = first_result.find_element(By.CSS_SELECTOR,
                                                  "span[class='year']").text
            actual_year = year_text.split('–')[0].strip()

            country_text = first_result.find_element(
                By.XPATH,
                '//*[@id="block_left_pad"]/div/div[2]/div/div[2]/span[2]').text
            actual_country = country_text.split(',')[0].strip()

        assert year in actual_year, f"""
                            Ожидался {year} год, получено {actual_year}"""
        assert country in actual_country, f"""
                            Ожидалась {country}, получена {actual_country}"""

    @allure.story('Невалидные проверки')
    @allure.feature('Ввод некорректного названия фильма {wrong_title}')
    def test_wrong_title_search(self):
        self.search.open_advanced_search()
        self.search.perform_search(
            field_locator=(By.ID, 'find_film'),
            search_value=wrong_title,
            button_locator=(
                By.CSS_SELECTOR, 'input[class="el_18 submit nice_button"]'))

        with allure.step('''Проверяем переход на страницу
                         с информацией о ненайденном запросе'''):

            info = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((
                    By.XPATH, '//*[@id="block_left_pad"]'
                    '/div/table/tbody/tr[1]/td/h2'))).text

        assert info == "К сожалению, по вашему запросу ничего не найдено..."
