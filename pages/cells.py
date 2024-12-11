from selenium import webdriver
from selenium.webdriver.common.by import By

import datetime
import time

from utils.tools import Tools


class Cells():

    def __init__(self, driver: webdriver.Chrome) -> None:
        if not driver:
            raise ValueError("The Driver is not avaliable")
        self.driver = driver
        self._report_data = {
            "Carregamento da página":
            None,
            "Carregamento do filtro SIG REGIONAL":
            None,
            "Carregamento do filtro UF":
            None,
            "Carregamento do filtro Município":
            None,
            "Carregamento do filtro CellName":
            None,
            "Carregamento do filtro Technology":
            None,
            "Carregamento do filtro Band":
            None,
            "Carregamento total dos dados":
            None,
            "Tempo total da validação":
            None,
            "Requisições com erro":
            None,
            "Cell Map":
            None,
            "Top Cells With Users Affected by Connection without Navigation":
            None,
            "% Users Affected by Connection without Navigation (Evolution)":
            None,
            "Top Cells ordered by Low Data Volume - KBs":
            None,
            "Total Data Volume (Evolution) - KBs":
            None,
            "Top Cells With Users Affected by InterRAT Handover Use Cases":
            None,
            "Top Cells 4G Data Volume Proportion and Retention":
            None,
            "% 4G Data Volume Escoamento (Evolution)":
            None,
            "% 4G Retention (Evolution)":
            None,
            "Tempo de resposta Top Cells With Users Affected by Connection without Navigation":
            None,
            "Tempo de resposta % Users Affected by Connection without Navigation (Evolution)":
            None,
            "Tempo de resposta Top Cells ordered by Low Data Volume - KBs":
            None,
            "Tempo de resposta Total Data Volume (Evolution) - KBs":
            None,
            "Tempo de resposta Top Cells With Users Affected by InterRAT Handover Use Cases":
            None,
            "Tempo de resposta Top Cells 4G Data Volume Proportion and Retention":
            None,
            "Tempo de resposta % 4G Data Volume Escoamento (Evolution)":
            None,
            "Tempo de resposta % 4G Retention (Evolution)":
            None,
            "Data":
            datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
        self.tools = Tools(self.driver)
        self.URL = "https://cem-connection-mf-telco-webapplications-prod.apps.ocp-01.tdigital-vivo.com.br/#/cem/cem-dashboard/celulas"

    def get_data_report_collection(self):
        return self._report_data

    def start_data_report_collection(self,
                                     period_from: str,
                                     period_to: str,
                                     sig_regional: str,
                                     uf: str,
                                     city: str,
                                     cell_name: str = "TODO",
                                     tecnology: str = "TODO",
                                     band: str = "TODO") -> dict:
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
            "//input[@formcontrolname='toDateInput']", period_from, period_to)

        start_time = time.time()

        # * Validanting page load time until ready to use by user
        self.tools.wait_all_requests_done()

        #! Get time to load filter Sig Regional field data
        self._report_data["Carregamento do filtro SIG REGIONAL"] = time.time(
        ) - start_time

        # Insert Sig Regional data
        self.tools.insert_text_on_text_input_and_click_in_option_selection(
            "//input[@formcontrolname='sigRegionalInput']", sig_regional)

        start_time = time.time()

        # * Validanting page load time until ready to use by user
        self.tools.wait_all_requests_done()

        #! Get time to load filter UF field data
        self._report_data["Carregamento do filtro UF"] = time.time() - \
            start_time

        # Insert UF data
        self.tools.insert_text_on_text_input_and_click_in_option_selection(
            "//input[@formcontrolname='ufInput']", uf)

        start_time = time.time()

        # * Validanting page load time until ready to use by user
        self.tools.wait_all_requests_done()

        #! Get time to load filter City field data
        self._report_data["Carregamento do filtro Município"] = time.time(
        ) - start_time

        # Insert City data
        self.tools.insert_text_on_text_input_and_click_in_option_selection(
            "//input[@formcontrolname='countryInput']", city)

        start_time = time.time()

        # * Validanting page load time until ready to use by user
        self.tools.wait_all_requests_done()

        #! Get time to load filter CellName field data
        self._report_data["Carregamento do filtro CellName"] = time.time(
        ) - start_time

        # Insert City data
        self.tools.insert_text_on_text_input_and_click_in_option_selection(
            "//input[@formcontrolname='nameInput']", cell_name)

        start_time = time.time()

        # * Validanting page load time until ready to use by user
        self.tools.wait_all_requests_done()

        #! Get time to load filter Technology field data
        self._report_data["Carregamento do filtro Technology"] = time.time(
        ) - start_time

        # Insert City data
        self.tools.insert_text_on_text_input_and_click_in_option_selection(
            "//input[@formcontrolname='technologyInput']", tecnology)

        start_time = time.time()

        # * Validanting page load time until ready to use by user
        self.tools.wait_all_requests_done()

        #! Get time to load filter Band field data
        self._report_data["Carregamento do filtro Band"] = time.time(
        ) - start_time

        # Insert Band data
        self.tools.insert_text_on_text_input_and_click_in_option_selection(
            "//input[@formcontrolname='bandInput']", band)

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
            "return window.pendingXHRRequests.size + window.XHRRequestsFinishedWithError.size"
        )
        self._report_data[
            "Requisições com erro"] = XHRRequestsFinishedWithError

        self._report_data = {
            **self._report_data,
            **self.tools.cells_tables_and_charts_status(
                period_from, period_to, sig_regional, uf, city, cell_name, tecnology, band)
        }

        if XHRRequestsFinishedWithError:
            print(f"{XHRRequestsFinishedWithError} finish with errors")
