import data
from helpers import retrieve_phone_code
from pages import UrbanRoutesPage
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        options = Options()
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        cls.driver = webdriver.Chrome(options=options)

    def prepare_order(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.select_comfort()
        routes_page.open_phone_modal()
        routes_page.set_phone(data.PHONE_NUMBER)
        routes_page.click_next()
        code = retrieve_phone_code(self.driver)
        routes_page.set_phone_code(code)
        routes_page.confirm_sms_code()
        routes_page.open_payment_method()
        routes_page.open_add_card()
        routes_page.set_card_number(data.CARD_NUMBER)
        routes_page.set_card_code(data.CARD_CODE)
        routes_page.click_add_card()
        routes_page.close_card_modal()
        return routes_page

    def test_set_route(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        assert routes_page.get_from() == data.ADDRESS_FROM
        assert routes_page.get_to() == data.ADDRESS_TO

    def test_select_comfort(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.select_comfort()
        assert routes_page.is_comfort_selected()

    def test_add_phone_number(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.select_comfort()
        routes_page.open_phone_modal()
        routes_page.set_phone(data.PHONE_NUMBER)
        routes_page.click_next()
        code = retrieve_phone_code(self.driver)
        routes_page.set_phone_code(code)
        routes_page.confirm_sms_code()
        routes_page.open_payment_method()
        assert routes_page.is_payment_method_visible()

    def test_add_card(self):
        routes_page = self.prepare_order()
        assert routes_page.is_message_field_visible()

    def test_driver_message(self):
        routes_page = self.prepare_order()
        routes_page.set_message(data.MESSAGE_FOR_DRIVER)
        assert routes_page.get_message() == data.MESSAGE_FOR_DRIVER

    def test_request_blanket_and_tissues(self):
        routes_page = self.prepare_order()
        routes_page.set_message(data.MESSAGE_FOR_DRIVER)
        routes_page.request_blanket_and_tissues()
        assert routes_page.get_message() == data.MESSAGE_FOR_DRIVER

    def test_order_ice_cream(self):
        routes_page = self.prepare_order()
        routes_page.set_message(data.MESSAGE_FOR_DRIVER)
        routes_page.request_blanket_and_tissues()
        routes_page.order_ice_cream(2)
        assert routes_page.get_ice_cream_count() == "2"

    def test_order_taxi(self):
        routes_page = self.prepare_order()
        routes_page.set_message(data.MESSAGE_FOR_DRIVER)
        routes_page.request_blanket_and_tissues()
        routes_page.order_ice_cream(2)
        assert routes_page.get_ice_cream_count() == "2"
        routes_page.order_taxi()
        assert routes_page.is_search_modal_visible()

    def test_driver_information(self):
        routes_page = self.prepare_order()
        routes_page.set_message(data.MESSAGE_FOR_DRIVER)
        routes_page.request_blanket_and_tissues()
        routes_page.order_ice_cream(2)
        routes_page.order_taxi()
        assert routes_page.is_driver_info_visible()


    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
