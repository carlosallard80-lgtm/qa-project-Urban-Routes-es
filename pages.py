from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    order_taxi_button = (By.XPATH,"//button[contains(normalize-space(.), 'Pedir un taxi')]")
    comfort_rate = (By.XPATH, "//div[contains(@class,'tcard')][.//div[text()='Comfort']]")
    phone_button = (By.XPATH, "//div[text()='Número de teléfono']")
    phone_field = (By.ID, "phone")
    next_button = (By.XPATH, "//button[text()='Siguiente']")
    phone_code_field = (By.ID, "code")
    confirm_sms_code_button = (By.XPATH, "//button[text()='Confirmar']")
    payment_method = (By.XPATH,"//div[contains(@class,'pp-button') and contains(@class,'filled')]")
    add_card_option = (By.XPATH, "//div[text()='Agregar tarjeta']")
    card_number_field = (By.ID, "number")
    card_code_field = (By.XPATH, "//input[@id='code' and @class='card-input']")
    add_card_button = (By.XPATH, "//button[text()='Agregar']")
    close_card_modal_button = (By.CSS_SELECTOR,"button.close-button.section-close")
    message_field = (By.ID, "comment")
    blanket_switch = (By.XPATH,"//div[text()='Manta y pañuelos']/following-sibling::div[@class='r-sw']")
    ice_cream_plus = (By.CLASS_NAME, "counter-plus")
    ice_cream_count = (By.CLASS_NAME, "counter-value")
    final_order_taxi_button = (By.CLASS_NAME, "smart-button")
    search_taxi_modal = (By.XPATH, "//div[contains(text(),'Buscar')]")
    driver_name = (By.XPATH,"//div[contains(text(), 'driver.name')]")

    def __init__(self, driver):
        self.driver = driver

    def wait_for_element(self, locator):
        return WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located(locator))

    def wait_for_click(self, locator):
        return WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(locator))

    def set_from(self, from_address):
        self.wait_for_element(self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.wait_for_element(self.to_field).send_keys(to_address)

    def get_from(self):
        return self.wait_for_element(self.from_field).get_property("value")

    def get_to(self):
        return self.wait_for_element(self.to_field).get_property("value")

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)
        self.click_order_taxi()

    def click_order_taxi(self):
        button = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.order_taxi_button))
        button.click()

    def select_comfort(self):
        self.wait_for_click(self.comfort_rate).click()

    def is_comfort_selected(self):
        return "active" in self.wait_for_element(self.comfort_rate).get_attribute("class")

    def open_phone_modal(self):
        self.wait_for_click(self.phone_button).click()

    def set_phone(self, phone_number):
        self.wait_for_element(self.phone_field).send_keys(phone_number)

    def click_next(self):
        self.wait_for_click(self.next_button).click()

    def set_phone_code(self, code):
        self.wait_for_element(self.phone_code_field).send_keys(code)

    def confirm_sms_code(self):
        self.wait_for_click(self.confirm_sms_code_button).click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located(self.confirm_sms_code_button))

    def is_payment_method_visible(self):
        return self.wait_for_element(self.payment_method).is_displayed()

    def open_payment_method(self):
        self.wait_for_click(self.payment_method).click()

    def open_add_card(self):
        self.wait_for_click(self.add_card_option).click()

    def set_card_number(self, card_number):
        self.wait_for_element(self.card_number_field).send_keys(card_number)

    def set_card_code(self, card_code):
        field = self.wait_for_element(self.card_code_field)
        field.send_keys(card_code)
        field.send_keys(Keys.TAB)

    def click_add_card(self):
        self.wait_for_click(self.add_card_button).click()

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.payment-picker.open")))

    def close_card_modal(self):
        buttons = self.driver.find_elements(
            By.CSS_SELECTOR,
            "button.close-button.section-close")

        for button in buttons:
            if button.is_displayed():
                button.click()
                break

    def set_message(self, message):
        self.wait_for_element(self.message_field).send_keys(message)

    def get_message(self):
        return self.wait_for_element(self.message_field).get_property("value")

    def is_message_field_visible(self):
        return self.wait_for_element(self.message_field).is_displayed()

    def request_blanket_and_tissues(self):
        self.wait_for_click(self.blanket_switch).click()

    def order_ice_cream(self, quantity):
        plus_button = self.wait_for_click(self.ice_cream_plus)
        for _ in range(quantity):
            plus_button.click()

    def get_ice_cream_count(self):
        return self.wait_for_element(self.ice_cream_count).text

    def order_taxi(self):
        self.wait_for_click(self.final_order_taxi_button).click()

    def is_search_modal_visible(self):
        return self.wait_for_element(self.search_taxi_modal).is_displayed()

    def wait_for_driver_info(self):
        return WebDriverWait(self.driver, 45).until(EC.visibility_of_element_located(self.driver_name))

    def is_driver_info_visible(self):
        return self.wait_for_driver_info().is_displayed()