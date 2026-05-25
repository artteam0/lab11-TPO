import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def driver():
    # Настройка Chrome для работы в GitHub Actions (без графического окна)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    # Открываем локальный файл index.html
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = f"file://{current_dir}/index.html"
    driver.get(file_path)
    
    yield driver
    driver.quit()

# Тест 1: Проверка заголовка страницы
def test_title(driver):
    assert "CI/CD" in driver.title

# Тест 2: Проверка наличия основных элементов формы
def test_form_elements(driver):
    username_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")
    submit_button = driver.find_element(By.ID, "submitBtn")
    
    assert username_input.is_displayed()
    assert password_input.is_displayed()
    assert submit_button.is_displayed()

# Тест 3: Проверка успешной отправки формы
def test_successful_login(driver):
    driver.find_element(By.ID, "username").send_keys("admin")
    driver.find_element(By.ID, "password").send_keys("12345")
    driver.find_element(By.ID, "submitBtn").click()
    
    message = driver.find_element(By.ID, "message").text
    assert message == "Успешный вход"