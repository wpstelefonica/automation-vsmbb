from selenium import webdriver
from selenium.webdriver.common.by import By

import datetime
import time

from utils.tools import Tools


class Vips():
    def __init__(self, driver: webdriver.Chrome) -> None:
        if not driver:
            raise ValueError("The Driver is not avaliable")
        self.driver = driver
        self._report_data = {
            "Carregamento da página": None,
            "Carregamento total dos dados": None,
            "Tempo total da validação": None,
            "Requisições com erro": None,
            "Data": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
        self.tools = Tools(self.driver)
        self.URL = "https://cem-connection-mf-telco-webapplications-prod.apps.ocp-01.tdigital-vivo.com.br/#/cem/cem-dashboard/vips"

    def get_data_report_collection(self):
        return self._report_data

    def start_data_report_collection(self, period_from: str, period_to: str) -> dict:
        """
            This function begins the data collection of report
        """

        if not period_from and not period_to:
            """
                Em Python dessa forma que esse if foi implementado ele é inútil, pois o python não deixa executar um método sem atributo,
                o certo que nesse if os dados sejam validados, saber que estão no padrão certo e com os atributos certos.
            """
            raise ValueError("MSISDN is necessary to get report data")

        #! Start page load counting
        start_validation_time = time.time()

        self.driver.get(self.URL)

        self.tools.request_tracker()

        time.sleep(2)

        # * Validanting page load time until ready to use by user
        self.tools.wait_all_requests_done()

        #! Wait show data on the table
        XHRRequestsFinishedWithError = self.driver.execute_script(
            "return window.pendingXHRRequests.size")

        #! Verify if has error on request, if no problem on request
        if not XHRRequestsFinishedWithError:
            #! wait 180 seconds to show table rows datas
            attempts = 0
            while True:
                qty_table_rows = self.driver.execute_script(
                    "return document.querySelectorAll('tbody>tr').length")
                if qty_table_rows > 0 or attempts > 180:
                    break
                time.sleep(1)
                attempts += 1

        #! Get page load time
        self._report_data["Carregamento da página"] = time.time() - \
            start_validation_time

        # Insert date value
        self.tools.insert_date_on_date_field(
            "//input[@formcontrolname='fromDateInput']",
            "//input[@formcontrolname='toDateInput']",
            period_from, period_to
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

        if XHRRequestsFinishedWithError:
            print(f"{XHRRequestsFinishedWithError} finish with errors")
