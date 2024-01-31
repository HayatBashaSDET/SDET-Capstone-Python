from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

@pytest.fixture()
def driver():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.implicitly_wait(10)
    driver.delete_all_cookies()
    driver.maximize_window()
    driver.get("http://webdriveruniversity.com/index.html")
    yield driver
    driver.quit()

def wait_and_scroll_into_view(driver, by, value):
    element = driver.find_element(by, value)
    driver.execute_script("arguments[0].scrollIntoView();", element)

def switch_to_window_by_title(driver, title):
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        if driver.title == title:
            break

def select_dropdown_option(driver, dropdown_id, option_value):
    element_dropdown = driver.find_element(By.ID, dropdown_id)
    dropdown = Select(element_dropdown)
    dropdown.select_by_value(option_value)

def click_checkbox(driver, checkbox_xpath):
    checkbox = driver.find_element(By.XPATH, checkbox_xpath)
    checkbox.click()

def count_checked_and_unchecked_checkboxes(driver, checkboxes_id):
    checkbox_list = driver.find_elements(By.ID, checkboxes_id)
    checked_count = sum(1 for checkbox in checkbox_list if checkbox.is_selected())
    unchecked_count = len(checkbox_list) - checked_count
    return checked_count, unchecked_count

def click_radio_button(driver, radio_button_xpath):
    radio_button = driver.find_element(By.XPATH, radio_button_xpath)
    radio_button.click()

def count_selected_and_unselected_radio_buttons(driver, radio_buttons_id):
    radio_button_list = driver.find_elements(By.ID, radio_buttons_id)
    selected_count = sum(1 for radio_button in radio_button_list if radio_button.is_selected())
    unselected_count = len(radio_button_list) - selected_count
    return selected_count, unselected_count

def test_webdriveruniversity(driver):
    wait_and_scroll_into_view(driver, By.XPATH, "//a[@class='navbar-brand']")
    
    element_dropdown_etc = driver.find_element(By.ID, "dropdown-checkboxes-radiobuttons")
    element_dropdown_etc.click()

    switch_to_window_by_title(driver, "WebDriver | Dropdown Menu(s) | Checkboxe(s) | Radio Button(s)")

    wait_and_scroll_into_view(driver, By.XPATH, "//a[@class='navbar-brand']")

    select_dropdown_option(driver, "dropdowm-menu-1", "sql")

    checked_count, unchecked_count = count_checked_and_unchecked_checkboxes(driver, "checkboxes")
    print("Checked checkboxes:", checked_count)
    print("UnChecked checkboxes:", unchecked_count)

    click_checkbox(driver, "//input[@type='checkbox' and @value='option-1']")
    click_checkbox(driver, "//input[@type='checkbox' and @value='option-4']")

    selected_count, unselected_count = count_selected_and_unselected_radio_buttons(driver, "radio-buttons")
    print("Selected radioButtons:", selected_count)
    print("Unselected radioButtons:", unselected_count)

    click_radio_button(driver, "//input[@type='radio' and @value='green']")
    click_radio_button(driver, "//input[@type='radio' and @value='blue']")
    click_radio_button(driver, "//input[@type='radio' and @value='yellow']")
    click_radio_button(driver, "//input[@type='radio' and @value='orange']")
