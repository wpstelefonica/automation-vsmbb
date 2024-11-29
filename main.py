import time

from pages.subscribers import Subscribers
from pages.cells import Cells
from pages.vips import Vips
from pages.executive_vision import ExecutiveVision
from pages.affected_cells import AffectedCells
from resources.report_generator import ReportGenerator
from core.driver_factory import DriverFactory

INITIAL_TIME = time.time()

driver = DriverFactory().get_driver()

TOTAL_EXECUTION_TIME_FOR_OPENING_DRIVER = time.time() - INITIAL_TIME

PERIOD_FROM = "11/28/2024"
PERIOD_TO = "11/29/2024"

subscribers_page = Subscribers(driver=driver)
subscribers_page.start_data_report_collection(
    msisdn="5511942837639", period_from=PERIOD_FROM, period_to=PERIOD_TO)
cells_page = Cells(driver=driver)
cells_page.start_data_report_collection(
    period_from=PERIOD_FROM, period_to=PERIOD_TO, sig_regional="SP", uf="SP", city="SÃO CAETANO DO SUL")
vips_page = Vips(driver=driver)
vips_page.start_data_report_collection(
    period_from=PERIOD_FROM, period_to=PERIOD_TO)
executive_vision = ExecutiveVision(driver=driver)
executive_vision.start_data_report_collection(
    period_from=PERIOD_FROM, period_to=PERIOD_TO, sig_regional="SP", uf="SP", city="SÃO CAETANO DO SUL")
affected_cells = AffectedCells(driver=driver)
affected_cells.start_data_report_collection(
    period_from=PERIOD_FROM, period_to=PERIOD_TO, sig_regional="SP", uf="SP", city="SÃO CAETANO DO SUL")

TOTAL_AUTOMATION_RUNTIME = time.time() - INITIAL_TIME

reports = {"Assinantes": subscribers_page.get_data_report_collection(),
           "Células": cells_page.get_data_report_collection(),
           "Vips": vips_page.get_data_report_collection(),
           "Células afetadas": affected_cells.get_data_report_collection(),
           "Visão executiva": executive_vision.get_data_report_collection()}
# reports = {"Visão executiva": executive_vision.get_data_report_collection()}
ReportGenerator.create_workbook(reports, "VSMBB", True)
