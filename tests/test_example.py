import pytest
# Импортируем тип Page для аннотации и expect для проверок
from playwright.sync_api import Page, expect
# аллюр
import allure

# Добавляем название в отчет
@allure.title('Проверка открытия главной страницы Edversemovie')

@allure.feature('Навигация') #Группируем по функциональности
def test_open_edversemovie(page: Page): # page автоматически придет из фикстуры
    # Проверяем что открывается edversemovie

    with allure.step('Открываем сайт'): # Шаг для отчета
        page.goto("https://edversemovie.ru") # Команда Playwright: открыть URL
    
    with allure.step('Проверяем заголовок'): # Еще один шаг
        expect(page).to_have_title('Cinescope') # Ждем что заголовок страницы станет Cinescope
    # expect авто-ожидание: сам ждет нужного состояния (до 5 секунд по умолчанию), поэтому тест не упадет из-за медленной загрузки страницы.
    
    
    # Добавляем скриншот в отчет
    allure.attach(
        page.screenshot(),
        name="Скриншот страницы",
        attachment_type=allure.attachment_type.PNG
    )
    
# pytest tests/test_example.py --headed --slowmo 5000  slowmo 5000 — замедлить действия, чтобы увидеть, как тест работает с сайтом
# page.pause()  Добавить в конец кода, чтобы открылся инспектор Playwright


# Запуск с генерацией Allure результатов
# pytest tests/test_example.py --headed --slowmo 5000 --alluredir=allure-results


# Просмотр отчета
# allure serve allure-results
# Отчет мы как бы хостим, поэтому что бы отключить отчет и дальше пользоваться терминалом нужно использовать команду ctrl + c и написать y=yes. Если терминал зависает чаще всего эта команда помогает.


# Запустите PowerShell от администратора, но можно прямо в проектном терминале
# Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
# irm get.scoop.sh | iex
# scoop install allure