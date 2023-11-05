BOT_NAME = "google"

SPIDER_MODULES = ["google.spiders"]
NEWSPIDER_MODULE = "google.spiders"

LOG_LEVEL = 'DEBUG'
# CRITICAL
# ERROR
# WARNING (default)
# INFO
# DEBUG

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    'google.pipelines.TransformDataPipeline': 300,
}


DOWNLOADER_MIDDLEWARES = {
    'google.middlewares.SeleniumMiddleware': 800,
}

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

SELENIUM_DRIVER_NAME = "firefox"

SELENIUM_DRIVER_ARGUMENTS = ["-headless"]