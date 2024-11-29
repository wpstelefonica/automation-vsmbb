from selenium import webdriver
from selenium.webdriver.common.by import By

import datetime
import time

from utils.tools import Tools


class AffectedCells():
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
            "Data": datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
        }
        self.tools = Tools(self.driver)
        self.URL = "https://cem-connection-mf-telco-webapplications-prod.apps.ocp-01.tdigital-vivo.com.br/#/cem/cem-dashboard/affectedcells"

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
        self.tools.insert_text_on_text_input_and_click_in_onption_selection(
            "//input[@formcontrolname='sigRegionalInput']", sig_regional
        )

        start_time = time.time()

        # * Validanting page load time until ready to use by user
        self.tools.wait_all_requests_done()

        #! Get time to load filter UF field data
        self._report_data["Carregamento do filtro UF"] = time.time() - \
            start_time

        # Insert UF data
        UF_FIELD = self.driver.find_element(
            By.XPATH, "//input[@formcontrolname='ufInput']")
        # Removing disabled attribute to add or change value on field without error
        self.driver.execute_script(
            "arguments[0].removeAttribute('disabled')", UF_FIELD)
        UF_FIELD.send_keys(uf)
        time.sleep(0.5)
        OPTION_SELECTION = self.driver.find_element(
            By.XPATH, f"//span[contains(@class, 'mat-option-text') and contains(text(),'{uf}')]")
        # *  //span[contains(@class, 'mat-option-text') and contains(text(),'SP')]
        OPTION_SELECTION.click()

        self.tools.insert_text_on_text_input_and_click_in_onption_selection(
            "//input[@formcontrolname='ufInput']", uf
        )

        start_time = time.time()

        # * Validanting page load time until ready to use by user
        self.tools.wait_all_requests_done()

        #! Get time to load filter City field data
        self._report_data["Carregamento do filtro Município"] = time.time(
        ) - start_time

        # Insert City data
        self.tools.insert_text_on_text_input_and_click_in_onption_selection(
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
