from selenium import webdriver
from selenium.webdriver.common.by import By

import datetime
import time

from utils.tools import Tools


class Subscribers():
    def __init__(self, driver: webdriver.Chrome) -> None:
        if not driver:
            raise ValueError("The Driver is not avaliable")
        self.driver = driver
        self._report_data = {
            "Carregamento da página": None,
            "Carregamento total dos dados": None,
            "Tempo total da validação": None,
            "Requisições com erro": None,
            "User and Device Information": None,
            "Summary of Failure Quantities by UC": None,
            "Indicator Percentage by Technology": None,
            "Downlink Data Volume by Technology (Evolution) - KBs": None,
            "Uplink Data Volume by Technology (Evolution) - KBs": None,
            "Uplink Data Volume by Technology (Evolution) - KBs": None,
            "(%) Data Flow - Data Volume Proportion by Technology (Evolution)": None,
            "(%) Retention by Technology (Evolution)": None,
            "Cells Used by The User during Selected Time Period - KBs": None,
            "Map of Cells Used by The User": None,
            "Distribution of Sessions by Technology by hour - KBs": None,
            "Detailed User Sessions during Selected Time Period - KBs": None,
            "Resume Sessions by Technology and Cause for Reclosing": None,
            "Data": datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        }
        self.tools = Tools(self.driver)
        self.URL = "https://cem-connection-mf-telco-webapplications-prod.apps.ocp-01.tdigital-vivo.com.br/#/cem/cem-dashboard/assinantes"

    def get_data_report_collection(self) -> dict[str, float]:
        return self._report_data

    def start_data_report_collection(self, msisdn, period_from: str, period_to: str) -> dict:
        """
            This function begins the data collection of report
        """

        if not msisdn:
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

        self.tools.insert_text_on_text_input(
            "//input[@name='msisdnInput']", msisdn)

        self.tools.insert_date_on_date_field(
            "//input[@formcontrolname='fromDateInput']",
            "//input[@formcontrolname='toDateInput']",
            period_from, period_from
        )

        self.tools.click_on_button("//button[contains(@class, 'btnFilter')]")
        #! Start filtering to get data counting
        start_time = time.time()

        # * Validanting page load time until ready to use by user
        self.tools.wait_all_requests_done()

        #! WAIT UNTIL SHOW DATA ON THE TABLES AND GRAPHS

        #! Get filtering to get data time
        self._report_data["Carregamento total dos dados"] = time.time() - \
            start_time
        self._report_data["Tempo total da validação"] = time.time() - \
            start_validation_time

        XHRRequestsFinishedWithError = self.driver.execute_script(
            "return window.pendingXHRRequests.size + window.XHRRequestsFinishedWithError.size")
        self._report_data["Requisições com erro"] = XHRRequestsFinishedWithError

        self._report_data = {**self._report_data, **self.tools.subscribers_tables_and_charts_status(
            msisdn, period_from, period_to)}

        if XHRRequestsFinishedWithError:
            print(f"{XHRRequestsFinishedWithError} finish with errors")

        print("STOP")
