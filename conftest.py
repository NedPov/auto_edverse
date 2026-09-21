# Импортируем pytest для создания фикстур
import pytest
# Отчет аллюр
import allure
# Импортируем менеджер контекста playwright
from playwright.sync_api import sync_playwright


@pytest.fixture(scope='session') #session - одна фикстура на весь прогон. Не будет создаваться заново
def browser():
    # Один браузер на весь прогон
    with sync_playwright() as p: #Открываем контекст playwright (благодаря with(помогает избегать прописания выброса ошибок) - Автоматически закроется после этого блока)
        b = p.chromium.launch(headless=False) # headless=False - браузер будет открыт, видно как выполняются действия
        yield b # Возвращаем(передаем) браузер в тест и замораживаем выполнение функции(имеется ввиду прям тут. Как с циклом тип)
        # После завершения всех тестов выполнение вернется сюда
        b.close() # Закрываем браузер (даже если тест упадет с ошибкой, он после yield перейдет сюда и закроется браузер)
        # после  b.close() мы выходим из witch и работаем метод зашитый в witch p.stop() - убиваем фоновые процессы движка playwright
        


#  Новая фикстура для каждого теста (по умолчанию)
@pytest.fixture()
def context(browser):
    # Изолированный контекст на каждый тест. Чистые куки, Local Storage
    ctx = browser.new_context() #Создаем новый контекст браузера
    yield ctx # Передаем
    ctx.close() # Закрываем
    
    
@pytest.fixture()
def page(context):
    # Новая страница (вкладка) для каждого теста
    pg = context.new_page()
    yield pg
    pg.close()
    
    

# Хук для создания скриншотов при падении теста
# hookwrapper=True - Превращает эту функцию в «обертку» (wrapper). Это значит, что функция выполнится до стандартного формирования отчета, сделает паузу, даст pytest отработать тест, а затем продолжит выполнение после формирования отчета.
# tryfirst=True: Говорит pytest: «Выполни мой хук первым, раньше всех других хуков-оберток».
@pytest.hookimpl(tryfirst=True, hookwrapper=True) 
def pytest_runtest_makereport(item, call):
    outcome = yield # Ждет пока тест выполнится и хук получит отчет
    rep = outcome.get_result() # извлекает из объекта сам отчет report
    
    # rep.when == 'call' - делаем скрин только если упал тест, а не "не открылся браузер" 
    if rep.when == 'call' and rep.failed: # статус failed
        if 'page' in item.fixturenames: # Проверка что в тесте вообще есть page - браузер (api tests)
            page = item.funcargs["page"] # достаем page из списка всех фикстур
            screenshot = page.screenshot()
            # Прикрепляем к аллюру
            allure.attach(
                screenshot,
                name="screenshot",
                attachment_type=allure.attachment_type.PNG
            )