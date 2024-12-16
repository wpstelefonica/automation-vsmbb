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
            -1,
            "Carregamento do filtro SIG REGIONAL":
            -1,
            "Carregamento do filtro UF":
            -1,
            "Carregamento do filtro Município":
            -1,
            "Carregamento do filtro CellName":
            -1,
            "Carregamento do filtro Technology":
            -1,
            "Carregamento do filtro Band":
            -1,
            "Carregamento total dos dados":
            -1,
            "Tempo total da validação":
            -1,
            "Requisições com erro":
            0,
            "Cell Map":
            False,
            "Top Cells With Users Affected by Connection without Navigation":
            False,
            "% Users Affected by Connection without Navigation (Evolution)":
            False,
            "Top Cells ordered by Low Data Volume - KBs":
            False,
            "Total Data Volume (Evolution) - KBs":
            False,
            "Top Cells With Users Affected by InterRAT Handover Use Cases":
            False,
            "Top Cells 4G Data Volume Proportion and Retention":
            False,
            "% 4G Data Volume Escoamento (Evolution)":
            False,
            "% 4G Retention (Evolution)":
            False,
            "Tempo de resposta Top Cells With Users Affected by Connection without Navigation":
            False,
            "Tempo de resposta % Users Affected by Connection without Navigation (Evolution)":
            False,
            "Tempo de resposta Top Cells ordered by Low Data Volume - KBs":
            False,
            "Tempo de resposta Total Data Volume (Evolution) - KBs":
            False,
            "Tempo de resposta Top Cells With Users Affected by InterRAT Handover Use Cases":
            False,
            "Tempo de resposta Top Cells 4G Data Volume Proportion and Retention":
            False,
            "Tempo de resposta % 4G Data Volume Escoamento (Evolution)":
            False,
            "Tempo de resposta % 4G Retention (Evolution)":
            False,
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
            **self.tools.tables_and_charts_status(report="cells",
                                                  date_from=period_from,
                                                  date_to=period_to,
                                                  sig_regional=sig_regional,
                                                  uf=uf,
                                                  city=city,
                                                  cell_name=cell_name,
                                                  tecnology=tecnology,
                                                  band=band)
        }

        if XHRRequestsFinishedWithError:
            print(f"{XHRRequestsFinishedWithError} finish with errors")
