from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys                                              
from selenium.webdriver.firefox.service import Service                                      
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
import time

URL = "http://the-internet.herokuapp.com/dynamic_controls"

service = Service('/usr/bin/geckodriver')                               
options = Options()
options.add_argument("--headless")

@pytest.fixture(scope="module")
def browser():
    driver = webdriver.Firefox(service=service, options=options)   # Укажите свой путь
    driver.maximize_window()
    yield driver
    driver.quit()

def test_checkbox_removal(browser):
    browser.get(URL)
    
    # Находим чекбокс и кнопку Remove
    checkbox = browser.find_element(By.ID, "checkbox")
    remove_button = browser.find_element(By.XPATH, "//button[text()='Remove']")
    
    remove_button.click()
    
    # Ожидаем исчезновения чекбокса (максимум 10 секунд)
    WebDriverWait(browser, 10).until(
        EC.invisibility_of_element_located((By.ID, "checkbox"))
    )
    
    # Проверяем, что чекбокс пропал
    assert len(browser.find_elements(By.ID, "checkbox")) == 0, "Чекбокс не исчез!"

def test_input_field_enabled(browser):
    browser.get(URL)
    
    # Находим поле ввода и кнопку Enable
    input_field = browser.find_element(By.XPATH, "//input[@type='text']")
    enable_button = browser.find_element(By.XPATH, "//button[text()='Enable']")
    
    enable_button.click()
    
    # Ожидаем, пока поле станет активным
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@type='text']"))
    )
    
    # Проверяем, что поле доступно для ввода
    assert input_field.is_enabled(), "Поле не активировано!"

if __name__ == "__main__":
    pytest.main(["-v", "--html=report.html"])  # Генерация HTML-отчета
