import logging
import subprocess
import sys
from pathlib import Path
from typing import List
from selenium.common.exceptions import SeleniumManagerException
from selenium.webdriver.common.options import BaseOptions

logger = logging.getLogger(__name__)

class SeleniumManager:
    """Wrapper for getting information from the Selenium Manager.
    This implementation is still in beta, and may change significantly.
    """

    def __init__(self) -> None:
        pass

    @staticmethod
    def get_binary() -> Path:
        """Determines the path of the correct Selenium Manager executable.
        :Returns: The Selenium Manager executable path.
        """
        platform = sys.platform
        dirs = {
            "darwin": "macos",
            "win32": "windows",
            "cygwin": "windows",
        }
        directory = dirs.get(platform) if dirs.get(platform) else "linux"
        file = "selenium-manager.exe" if platform == "win32" else "selenium-manager"
        path = Path(__file__).parent.joinpath(directory, file)
        if not path.is_file():
            tracker = "https://github.com/SeleniumHQ/selenium-ide/issues/577"
            raise SeleniumManagerException(f"{path} is not a valid Selenium Manager executable. Please download the correct version from {tracker}")
        return path

    def driver_location(self, options: BaseOptions) -> str:
        """
        Determines the path of the correct driver.

        :Args:
         - browser: which browser to get the driver for.

        :Returns: The driver path to use
        """
        args = [str(self.get_binary()), "--driver-location", options.browser_name.lower()]
        command = " ".join(args)
        logger.info(f"Executing: {command}")
        completed_proc = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = completed_proc.stdout.decode("utf-8")
        if completed_proc.returncode:
            raise SeleniumManagerException(f"Selenium Manager failed to determine driver location: {completed_proc.stderr.decode('utf-8')}")
        else:
            # Selenium Manager exited successfully.
            for item in completed_proc.stderr.decode('utf-8').splitlines():
                if "WARN" in item:
                    logger.warning(item)
            return result
