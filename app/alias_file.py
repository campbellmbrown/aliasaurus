import logging
import os
import shutil
import winreg as reg
from datetime import datetime

KEY_PATH = r"Software\Microsoft\Command Processor"
VALUE_NAME = "AutoRun"
VALUE_DATA = "%APPDATA%\\aliasaurus\\alias.cmd"

ALIAS_CMD_PATH = os.path.join(os.environ["APPDATA"], "aliasaurus", "alias.cmd")


class AliasFile:
    def __init__(self):
        self.setup()

    def setup(self):
        """Set up the alias file."""
        logging.info("Setting up alias file...")
        try:
            with reg.OpenKey(reg.HKEY_CURRENT_USER, KEY_PATH, 0, reg.KEY_ALL_ACCESS) as key:
                if reg.QueryValueEx(key, VALUE_NAME)[0] == VALUE_DATA:
                    logging.info("Alias file already set up.")
                else:
                    logging.info("Alias file not set up correctly, fixing it...")
                    reg.SetValueEx(key, VALUE_NAME, 0, reg.REG_SZ, VALUE_DATA)
        except FileNotFoundError:
            logging.info("Registry key not found, creating it...")
            with reg.CreateKey(reg.HKEY_CURRENT_USER, KEY_PATH) as key:
                reg.SetValueEx(key, VALUE_NAME, 0, reg.REG_SZ, VALUE_DATA)
        logging.info("Registry key set up successfully.")

        logging.info("Checking for alias file...")
        if not os.path.exists(os.path.dirname(ALIAS_CMD_PATH)):
            os.makedirs(os.path.dirname(ALIAS_CMD_PATH), exist_ok=True)
        if not os.path.exists(ALIAS_CMD_PATH):
            logging.info("Alias file not found, creating it...")
            self._write_header()
        logging.info("Alias file set up successfully.")

    def backup(self):
        """Create a backup of the alias file."""
        logging.info("Creating backup of alias file...")
        backup_path = os.path.join(
            os.path.dirname(ALIAS_CMD_PATH), f"alias_backup_{datetime.now().strftime('%Y%m%d%H%M%S')}.cmd"
        )
        shutil.copyfile(ALIAS_CMD_PATH, backup_path)
        logging.info("Backup created successfully.")

    def open(self):
        """Open the directory containing the alias file."""
        os.startfile(os.path.dirname(ALIAS_CMD_PATH))

    def _write_header(self):
        """Write the header of the alias file."""
        with open(ALIAS_CMD_PATH, "w", encoding="utf-8") as file:
            file.write("@echo off\n")
            file.write("ECHO .----------------------------------------------.\n")
            file.write("ECHO ^|        Aliases set up using Aliasaurus       ^|\n")
            file.write("ECHO ^| https://github.com/campbellmbrown/aliasaurus ^|\n")
            file.write("ECHO '----------------------------------------------'\n")
            file.write("ECHO %date% %time%\n")
