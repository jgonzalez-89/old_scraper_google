from selenium.webdriver.firefox.service import Service as FirefoxService
# Esto se ha cambiado
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver import Firefox

from scrapy.utils.project import get_project_settings
from scrapy.http import HtmlResponse

import time


class SeleniumMiddleware:
    def __init__(self):
        # Obtiene las configuraciones del proyecto
        settings = get_project_settings()

        # Configura las opciones del navegador para Firefox
        options = FirefoxOptions()  # Esto se ha cambiado
        for argument in settings.get("SELENIUM_DRIVER_ARGUMENTS", []):
            options.add_argument(argument)

        # Configura el servicio y el navegador para Firefox
        service = FirefoxService(
            executable_path=GeckoDriverManager().install())
        self.driver = Firefox(service=service, options=options)

    def process_request(self, request, spider):
        self.driver.get(request.url)
        time.sleep(2)  # pausa de 2 segundos
        return HtmlResponse(self.driver.current_url, body=self.driver.page_source, encoding='utf-8', request=request)
