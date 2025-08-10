from selenium import webdriver
import allure
import time
from config import base_url_ui
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


@allure.epic('Вспомогательные функции для запуска автотестов')
class KinopoiskAdvancedSearch:

    def __init__(self, driver: webdriver) -> None:
        self.driver = driver

    @allure.step("Прохождение капчи(вручную, при необходимости)")
    def handle_captcha(self):
        try:
            self.driver.find_element(
                By.CLASS_NAME, "CheckboxCaptcha-Button").click()

            # время для прохождения капчи вручную, если понадобится
            time.sleep(30)

        except NoSuchElementException:
            pass

    @allure.step("Открытие страницы расширенного поиска")
    def open_advanced_search(self):
        with allure.step('Открыть главную страницу Кинопоиска'):
            self.driver.get(base_url_ui)
            self.handle_captcha()
        with allure.step('Ожидание и переход на кнопку расширенного поиска'):
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((
                    By.CLASS_NAME, "styles_advancedSearch__uwvnd"))).click()
            self.handle_captcha()

    @allure.step("Выполнение поиска по одному параметру")
    def perform_search(self, field_locator, search_value, button_locator):
        with allure.step(f'Ввести значение "{search_value}" в поле поиска'):
            field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(field_locator))
            field.clear()
            field.send_keys(search_value)

        with allure.step('Нажать кнопку "Поиск"'):
            self.driver.find_element(*button_locator).click()

    @allure.step("Выполнение поиска по двум параметрам")
    def search_by_several_parameters(self,
                                     field_locator1,
                                     field_locator2,
                                     search_value1,
                                     search_value2,
                                     button_locator):

        with allure.step(f'''Ввести значения "{search_value1}"
                         и "{search_value2}" в соответствующие поля'''):
            field1 = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(field_locator1))
            field2 = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(field_locator2))
            field1.send_keys(search_value1)
            field2.send_keys(search_value2)

        with allure.step('Нажать кнопку "Поиск"'):
            self.driver.find_element(*button_locator).click()
