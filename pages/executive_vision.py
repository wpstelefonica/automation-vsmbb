from selenium import webdriver
from selenium.webdriver.common.by import By

import datetime
import time

from utils.tools import Tools


class ExecutiveVision():
    def __init__(self, driver: webdriver.Chrome) -> None:
        if not driver:
            raise ValueError("The Driver is not avaliable")
        self.driver = driver
        self._report_data = {
            "Carregamento da página": None,
            "Carregamento do filtro SIG REGIONAL": None,
            "Carregamento do filtro UF": None,
            "Carregamento do filtro Município": None,
            "Carregamento total dos dados": None,
            "Tempo total da validação": None,
            "Requisições com erro": None,
            "Data": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        }
        self.tools = Tools(self.driver)
        self.URL = "https://cem-connection-mf-telco-webapplications-prod.apps.ocp-01.tdigital-vivo.com.br/#/cem/cem-dashboard/executive-vision"

    def get_data_report_collection(self):
        return self._report_data

    def start_data_report_collection(self, period_from: str, period_to: str, sig_regional: str, uf: str, city: str) -> dict:
        """
            This function begins the data collection of report
        """

        if not sig_regional:
            """
                Em Python dessa forma que esse if foi implementado ele é inútil, pois o python não deixa executar um método sem atributo,
                o certo que nesse if os dados sejam validados, saber que estão no padrão certo e com os atributos certos.
            """
            raise ValueError("MSISDN is necessary to get report data")

        #! Start page load counting
        start_validation_time = time.time()
        self.driver.get(self.URL)

        self.tools.request_tracker()

        # * Validanting page load time until ready to use by user
        self.tools.wait_all_requests_done()

        #! Get page load time
        self._report_data["Carregamento da página"] = time.time() - \
            start_validation_time

        # Insert date value
        self.tools.insert_date_on_date_field(
            "//input[@formcontrolname='fromDateInput']",
            "//input[@formcontrolname='toDateInput']",
            period_from, period_to
        )

        start_time = time.time()

        # * Validanting page load time until ready to use by user
        self.tools.wait_all_requests_done()

        #! Get time to load filter Sig Regional field data
        self._report_data["Carregamento do filtro SIG REGIONAL"] = time.time(
        ) - start_time

        # Insert Sig Regional data
        self.tools.insert_text_on_text_input_and_click_in_option_selection(
            "//input[@formcontrolname='sigRegionalInput']", sig_regional
        )

        start_time = time.time()

        # * Validanting page load time until ready to use by user
        self.tools.wait_all_requests_done()

        #! Get time to load filter UF field data
        self._report_data["Carregamento do filtro UF"] = time.time() - \
            start_time

        # Insert UF data
        self.tools.insert_text_on_text_input_and_click_in_option_selection(
            "//input[@formcontrolname='ufInput']", uf
        )

        start_time = time.time()

        # * Validanting page load time until ready to use by user
        self.tools.wait_all_requests_done()

        #! Get time to load filter City field data
        self._report_data["Carregamento do filtro Município"] = time.time(
        ) - start_time

        # Insert City data
        self.tools.insert_text_on_text_input_and_click_in_option_selection(
            "//input[@formcontrolname='countryInput']", city
        )

        # Clicking to search cells data
        self.tools.click_on_button("//button[contains(@class, 'btnFilter')]")

        #! Start filtering to get data counting
        start_time = time.time()

        # * Validanting page load time until ready to use by user
        self.tools.wait_all_requests_done()

        #! Get filtering to get data time
        self._report_data["Carregamento total dos dados"] = time.time() - \
            start_time
        self._report_data["Tempo total da validação"] = time.time() - \
            start_validation_time

        XHRRequestsFinishedWithError = self.driver.execute_script(
            "return window.pendingXHRRequests.size")
        self._report_data["Requisições com erro"] = XHRRequestsFinishedWithError


# if __name__ == "__main__":

#     INITIAL_TIME = time.time()

#     driver = DriverFactory().get_driver()

#     TOTAL_EXECUTION_TIME_FOR_OPENING_DRIVER = time.time() - INITIAL_TIME

#     executive_vision = ExecutiveVision(driver=driver)
#     executive_vision.start_data_report_collection(
#         period_from="11/06/2024", period_to="11/07/2024", sig_regional="SP", uf="SP", city="OSASCO")

#     TOTAL_AUTOMATION_RUNTIME = time.time() - INITIAL_TIME

#     time.sleep(5)
