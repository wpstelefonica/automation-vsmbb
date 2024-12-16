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
            "Carregamento da página":
            -1,
            "Carregamento total dos dados":
            -1,
            "Tempo total da validação":
            -1,
            "Requisições com erro":
            0,
            "Tempo das requisições User and Device Information":
            -1,
            "Tempo das requisições Summary of Failure Quantities by UC":
            -1,
            "Tempo das requisições Indicator Percentage by Technology":
            -1,
            "Tempo das requisições Downlink Data Volume by Technology (Evolution) - KBs":
            -1,
            "Tempo das requisições Uplink Data Volume by Technology (Evolution) - KBs":
            -1,
            "Tempo das requisições Uplink Data Volume by Technology (Evolution) - KBs":
            -1,
            "Tempo das requisições (%) Data Flow - Data Volume Proportion by Technology (Evolution)":
            -1,
            "Tempo das requisições (%) Retention by Technology (Evolution)":
            -1,
            "Tempo das requisições Cells Used by The User during Selected Time Period - KBs":
            -1,
            "Tempo das requisições Map of Cells Used by The User":
            -1,
            "Tempo das requisições Distribution of Sessions by Technology by hour - KBs":
            -1,
            "Tempo das requisições Detailed User Sessions during Selected Time Period - KBs":
            -1,
            "Tempo das requisições Resume Sessions by Technology and Cause for Reclosing":
            -1,
            "User and Device Information":
            False,
            "Summary of Failure Quantities by UC":
            False,
            "Indicator Percentage by Technology":
            False,
            "Downlink Data Volume by Technology (Evolution) - KBs":
            False,
            "Uplink Data Volume by Technology (Evolution) - KBs":
            False,
            "Uplink Data Volume by Technology (Evolution) - KBs":
            False,
            "(%) Data Flow - Data Volume Proportion by Technology (Evolution)":
            False,
            "(%) Retention by Technology (Evolution)":
            False,
            "Cells Used by The User during Selected Time Period - KBs":
            False,
            "Map of Cells Used by The User":
            False,
            "Distribution of Sessions by Technology by hour - KBs":
            False,
            "Detailed User Sessions during Selected Time Period - KBs":
            False,
            "Resume Sessions by Technology and Cause for Reclosing":
            False,
            "Data":
            datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
        self.tools = Tools(self.driver)
        self.URL = "https://cem-connection-mf-telco-webapplications-prod.apps.ocp-01.tdigital-vivo.com.br/#/cem/cem-dashboard/assinantes"

    def get_data_report_collection(self) -> dict[str, float]:
        return self._report_data

    def start_validation(self, msisdn, period_from: str,
                         period_to: str) -> dict:
        """
            This function begins the data collection of report
        """

        #! Start page load counting
        start_validation_time = time.time()
        self.driver.get(self.URL)

        self.tools.request_tracker()

        # * Validanting page load time until ready to use by user
        self.tools.wait_all_requests_done()

        #! Get page load time
        self._report_data["Carregamento da página"] = time.time() - \
            start_validation_time

        self.tools.insert_text_on_text_input("//input[@name='msisdnInput']",
                                             msisdn)

        self.tools.insert_date_on_date_field(
            "//input[@formcontrolname='fromDateInput']",
            "//input[@formcontrolname='toDateInput']", period_from, period_to)

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
            "return window.pendingXHRRequests.size + window.XHRRequestsFinishedWithError.size"
        )
        self._report_data[
            "Requisições com erro"] = XHRRequestsFinishedWithError

        self._report_data = {
            **self._report_data,
            **self.tools.tables_and_charts_status(report="subscribers",
                                                  msisdn=msisdn,
                                                  date_from=period_from,
                                                  date_to=period_to)
        }

        if XHRRequestsFinishedWithError:
            print(f"{XHRRequestsFinishedWithError} finish with errors")

        #! Frontend tests
        '''
            This validations are done by checking the data displayed on the page
            Is calculated the response status with data displayed on page status
        '''
        # User and Device Information table
        self._report_data["User and Device Information"] = self._report_data[
            "User and Device Information"] and self.tools.check_table_user_and_device_information(
            )

        # Summary of Failure Quantities by UC table
        self._report_data[
            "Summary of Failure Quantities by UC"] = self._report_data[
                "Summary of Failure Quantities by UC"] and self.tools.check_table_summary_of_failure_quantities_by_uc(
                )

        # Cells Used by The User during Selected Time Period - KBs table
        self._report_data[
            "Cells Used by The User during Selected Time Period - KBs"] = self._report_data[
                "Cells Used by The User during Selected Time Period - KBs"] and self._report_data[
                    "User and Device Information"] and self.tools.check_table_data(
                        "Cells Used by The User during Selected Time Period - KBs"
                    )

        # Map of Cells Used by The User
        self._report_data["Map of Cells Used by The User"] = self._report_data[
            "Map of Cells Used by The User"] and self._report_data[
                "Map of Cells Used by The User"] and self.tools.check_map_data(
                )

        # Distribution of Sessions by Technology by hour - KBs table
        self._report_data[
            "Distribution of Sessions by Technology by hour - KBs"] = self._report_data[
                "Distribution of Sessions by Technology by hour - KBs"] and self.tools.check_table_data(
                    "Distribution of Sessions by Technology by hour - KBs")

        # Detailed User Sessions during Selected Time Period - KBs table
        self._report_data[
            "Detailed User Sessions during Selected Time Period - KBs"] = self._report_data[
                "Detailed User Sessions during Selected Time Period - KBs"] and self.tools.check_table_data(
                    "Detailed User Sessions during Selected Time Period - KBs")

        print("STOP")
