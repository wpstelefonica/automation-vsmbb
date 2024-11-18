from selenium import webdriver
from selenium.webdriver.common.by import By

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

        # Insert MSISDN value
        MSISDN_FIELD = self.driver.find_element(
            By.XPATH, "//input[@name='msisdnInput']")
        MSISDN_FIELD.send_keys(msisdn)

        # Insert date value
        FROM_DATE_FIELD = self.driver.find_element(
            By.XPATH, "//input[@formcontrolname='fromDateInput']")
        self.driver.execute_script(
            "arguments[0].removeAttribute('disabled')", FROM_DATE_FIELD)
        # Date format mm/dd/yyyy
        FROM_DATE_FIELD.send_keys(period_from)
        # Removing disabled attribute to add or change value on date inputs
        TO_DATE_FIELD = self.driver.find_element(
            By.XPATH, "//input[@formcontrolname='toDateInput']")
        # Removing disabled attribute to add or change value on date inputs
        self.driver.execute_script(
            "arguments[0].removeAttribute('disabled')", TO_DATE_FIELD)
        # Date format mm/dd/yyyy
        TO_DATE_FIELD.send_keys(period_to)

        # Clicking to search msisdn data
        FILTER_BUTTON = self.driver.find_element(
            By.XPATH, "//button[contains(@class, 'btnFilter')]")
        FILTER_BUTTON.click()
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
            "return window.pendingXHRRequests.size")
        self._report_data["Requisições com erro"] = XHRRequestsFinishedWithError

        status_and_queries = self.tools.get_queries_script_and_status_response()

        if XHRRequestsFinishedWithError:
            print(f"{XHRRequestsFinishedWithError} finish with errors")
