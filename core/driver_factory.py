from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
# from webdriver_manager.microsoft import EdgeChromiumDriverManager
# from selenium.webdriver.edge.service import Service
# from selenium.webdriver.edge.options import Options
import os


class DriverFactory():

    def __init__(self) -> None:
        os.environ['WDM_SSL_VERIFY'] = '0'  # Ignorar verificação SSL

        options = Options()
        # chrome_options.add_argument("--headless")
        options.add_argument('--log-level-3')  # Disable console log
        # chrome_options.add_experimental_option("detach", True)
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)

        # options = Options()
        # service = Service(EdgeChromiumDriverManager().install())
        # self.driver = webdriver.Edge(service=service, options=options)

    def get_driver(self) -> webdriver.Edge:
        return self.driver

    def kill_driver(self) -> None:
        if self.driver:
            self.driver.quit()
            self.driver = None
