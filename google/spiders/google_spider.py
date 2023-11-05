import scrapy
import re
import random
import time
from scrapy.spiders import Spider
from scrapy import Request
import datetime
from scrapy_selenium import SeleniumRequest
from user_agent import generate_user_agent
import logging

logging.getLogger("protego").setLevel(logging.WARNING)
logging.getLogger("selenium.webdriver.remote.remote_connection").setLevel(
    logging.WARNING
)
logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)

# scrapy crawl product_scraper -a gsi=B01DS0HUK6 -o 04-05-2023.json


class GoogleSpider(scrapy.Spider):
    name = "google"

    def __init__(self, gsi=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if gsi:
            self.gsi = gsi.split(",")
        else:
            self.gsi = [
                # Davines
                "12414137775388458150",
                "8673629157721452512",
                "10623661203372066259",
                "17676435495709791514",
                "3321539125099760305",
                "6824618517849690561",
                "2667241078769520361",
                "2226848262174835689",
                "1050479297502208109",
                "813071008737609872",
                "14151175057952102237",
                "14085577273259023259",
                "14682460711794499499",
                "5632906504165503153",
                "2530150965370143429",
                "6025983038085933501",
                "6667073508218113189",
                "3476464378683291905",
                "14195707237233699508",
                "13200968603662839240",
                "9058111224963794474",
                "14144590952505956890",
                "15525290041480229573",
                "11684293362920089460",
                "10708395228749773555",
                "11206826918413678452",
                "859529077139890087",
                "9520454788893692575",
                "1939224718813679718",
                "9867941516065695162",
                "9158348605555005549",
                "11392259176749487154",
                "12276963486079426675",
                "14121226674293108990",
                "8665728360764654241",
                "10011157393115561308",
                # Comfortzone
                "16044579697508689325",
                "15238612148984975963",
                "5609447106858812911",
                "5566158548055949176",
                "1375725355290439107",
                "11291210618570818758",
                "2881059760945696401",
                "7536400739452027261",
                "1836465510167030292",
            ]

    def start_requests(self):
        for gsi in self.gsi:
            url = f"https://www.google.es/shopping/product/{gsi}/offers?hl=es&"
            print(f"URL: {url}")  # Agrega esta línea para depurar
            headers = {"User-Agent": generate_user_agent()}
            yield SeleniumRequest(
                url=url,
                callback=self.parse,
                headers=headers,
                meta={
                    "handle_httpstatus_list": [503],
                    "dont_redirect": True,
                    "original_url": url,
                    "gsi": gsi,  # Agrega el código GSI a los metadatos
                },
            )

    def parse(self, response):
        try:
            # Extraer la información usando las funciones definidas
            codigo_GSI = response.meta["gsi"]  # Obtiene el código GSI de los metadatos
            fecha = datetime.datetime.now().strftime("%d-%m-%Y")
            nombre = self.extract_nombre(response)
            imagen = self.extract_imagen(response)
            precios = self.extract_precio(response)
            vendedores = self.extract_vendedor(response)

            if nombre is None or imagen is None or precios is None:
                raise Exception("No se pudo extraer toda la información necesaria")

            yield {
                "fecha": fecha,
                # "imagen": imagen,
                "nombre": nombre,
                "vendedores": vendedores,
                "precios": precios,
                "GSI": codigo_GSI,
            }
            time.sleep(random.uniform(1, 3))

        except Exception as e:
            retry_times = response.meta.get("retry_times", 0) + 1

            if retry_times <= 10:  # Puedes ajustar el número máximo de intentos
                self.logger.info(
                    f"Reintentando {response.meta['original_url']} (intento {retry_times}) - Error: {str(e)}"
                )
                time.sleep(
                    random.uniform(1, 3)
                )  # Agrega tiempo de espera entre intentos
                headers = {"User-Agent": generate_user_agent()}  # Agrega encabezados
                yield SeleniumRequest(
                    url=response.meta["original_url"],
                    callback=self.parse,
                    headers=headers,
                    meta={
                        "handle_httpstatus_list": [503],
                        "dont_redirect": True,
                        "retry_times": retry_times,
                        "original_url": response.meta["original_url"],
                    },
                    dont_filter=True,  # Agrega esta línea
                )
                return

    @staticmethod
    def extract_precio(response):
        precios_str = response.xpath("//div[@class='drzWO']/text()").getall()
        precios = []
        for precio_str in precios_str:
            # Aquí, debemos quitar el símbolo del euro y reemplazar la coma con un punto
            precio_str = (
                precio_str.replace(",", ".")
                .replace("&nbsp;€", "")
                .replace("€", "")
                .strip()
            )
            try:
                precios.append(float(precio_str))
            except ValueError:
                continue  # Si no podemos convertir a float, saltamos el precio
        return precios

    @staticmethod
    def extract_vendedor(response):
        vendedores = response.xpath("//a[@class='b5ycib shntl']/text()").getall()
        vendedores = [v.strip() for v in vendedores]
        return vendedores

    @staticmethod
    def extract_nombre(response):
        nombre = response.xpath(
            "//a[@class='BvQan sh-t__title sh-t__title-pdp translate-content']/text()"
        ).get()
        if nombre:
            return nombre.replace('"', "").lower().strip()
        return None

    @staticmethod
    def extract_imagen(response):
        return response.xpath("//img[@class='r4m4nf']/@src").get()

    @staticmethod
    def extract_codigo(url):
        codigo_regex = r"\b\d{20}\b"  # busca una secuencia de 20 dígitos
        match = re.search(codigo_regex, url)
        if match:
            return match.group(0)
        return None
