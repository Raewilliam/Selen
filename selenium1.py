import os
import shutil
import urllib.request
from distutils import spawn

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class DriverFinder:
    @staticmethod
    def get_path(service, options):
        """
        Get the path to the ChromeDriver executable.

        :param service: the Service object for ChromeDriver
        :param options: the Options object for ChromeDriver
        :return: the path to the ChromeDriver executable
        """
        path = options.chrome_driver_path or service.path
        return shutil.which(path) or path


class SeleniumManager:
    CHROMEDRIVER_VERSION = '91.0.4472.19'

    def __init__(self):
        self.binary_location = None
        self.download_location = os.path.join(os.path.dirname(__file__), 'downloads')
        if not os.path.exists(self.download_location):
            os.makedirs(self.download_location)

    def get_binary(self):
        """
        Get the path to the Chrome binary.

        :return: the path to the Chrome binary
        """
        if self.binary_location is None:
            self.binary_location = spawn.find_executable('google-chrome-stable')
            if self.binary_location is None:
                self.binary_location = spawn.find_executable('google-chrome')
            if self.binary_location is None:
                self.binary_location = '/usr/bin/google-chrome'
        return self.binary_location

    def download_driver(self):
        """
        Download the ChromeDriver executable.

        :return: the path to the downloaded ChromeDriver executable
        """
        driver_file = 'chromedriver_linux64.zip'
        driver_url = 'https://chromedriver.storage.googleapis.com/{}/{}'.format(self.CHROMEDRIVER_VERSION, driver_file)
        driver_path = os.path.join(self.download_location, driver_file)
        if not os.path.exists(driver_path):
            urllib.request.urlretrieve(driver_url, driver_path)
            os.chmod(driver_path, 0o755)
        return driver_path

    def driver_location(self, options):
        """
        Get the path to the ChromeDriver executable.

        :param options: the Options object for ChromeDriver
        :return: the path to the ChromeDriver executable
        """
        service = webdriver.chrome.service.Service(self.download_driver())
        path = DriverFinder.get_path(service, options)
        return path

    def get_driver(self):
        """
        Get a new instance of the ChromeDriver.

        :return: a new instance of the ChromeDriver
        """
        chrome_options = Options()
        chrome_options.binary_location = self.get_binary()
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1280,720')
        chrome_options.add_argument('--disable-popup-blocking')
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins-discovery')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--allow-insecure-localhost')
        chrome_options.add_argument('--user-data-dir=/tmp/user-data')
        chrome_options.add_argument('--data-path=/tmp/data-path')
        chrome_options.add_argument('--homedir=/tmp')
        chrome_options.add_argument('--disk-cache-dir=/tmp/cache-dir')
        chrome_options.add_argument('--disable-application-cache')
        chrome_options.add_argument('--disable-offline-load-stale-cache')
        chrome_options.add_argument('--log-level
