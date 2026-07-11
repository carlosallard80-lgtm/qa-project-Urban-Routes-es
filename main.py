import data
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


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


class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        options = Options()
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        cls.driver = webdriver.Chrome(options=options)

    def prepare_order(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.select_comfort()
        routes_page.open_phone_modal()
        routes_page.set_phone(data.phone_number)
        routes_page.click_next()
        code = retrieve_phone_code(self.driver)
        routes_page.set_phone_code(code)
        routes_page.confirm_sms_code()
        routes_page.open_payment_method()
        routes_page.open_add_card()
        routes_page.set_card_number(data.card_number)
        routes_page.set_card_code(data.card_code)
        routes_page.click_add_card()
        routes_page.close_card_modal()
        return routes_page

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        assert routes_page.get_from() == data.address_from
        assert routes_page.get_to() == data.address_to

    def test_select_comfort(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.select_comfort()
        assert routes_page.is_comfort_selected()

    def test_add_phone_number(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.select_comfort()
        routes_page.open_phone_modal()
        routes_page.set_phone(data.phone_number)
        routes_page.click_next()
        code = retrieve_phone_code(self.driver)
        routes_page.set_phone_code(code)
        routes_page.confirm_sms_code()
        routes_page.open_payment_method()

    def test_add_card(self):
        self.prepare_order()

    def test_driver_message(self):
        routes_page = self.prepare_order()
        routes_page.set_message(data.message_for_driver)
        assert routes_page.get_message() == data.message_for_driver

    def test_request_blanket_and_tissues(self):
        routes_page = self.prepare_order()
        routes_page.set_message(data.message_for_driver)
        routes_page.request_blanket_and_tissues()

    def test_order_ice_cream(self):
        routes_page = self.prepare_order()
        routes_page.set_message(data.message_for_driver)
        routes_page.request_blanket_and_tissues()
        routes_page.order_ice_cream(2)
        assert routes_page.get_ice_cream_count() == "2"

    def test_order_taxi(self):
        routes_page = self.prepare_order()
        routes_page.set_message(data.message_for_driver)
        routes_page.request_blanket_and_tissues()
        routes_page.order_ice_cream(2)
        assert routes_page.get_ice_cream_count() == "2"
        routes_page.order_taxi()
        assert routes_page.is_search_modal_visible()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
