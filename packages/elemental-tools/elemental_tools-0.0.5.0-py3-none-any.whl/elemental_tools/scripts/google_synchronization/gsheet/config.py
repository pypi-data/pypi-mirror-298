import os
import pathlib

from elemental_tools.api.settings import SettingsController
from elemental_tools.api.config import root_user
from elemental_tools.json import json_to_temp_file
from elemental_tools.logger import Logger
from google.oauth2.service_account import Credentials
from elemental_tools.path import Relative


relative = Relative(__file__).relative

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

logger = Logger(app_name='scripts', owner='google-sync').log
settings = SettingsController()

try:

    credentials_as_file = json_to_temp_file(settings.get(sub=root_user, name='google_api_credentials_json'))

    google_credentials = Credentials.from_service_account_file(
        credentials_as_file,
        scopes=scopes
    )

    os.rmdir(os.path.dirname(credentials_as_file))

    logger('info-error', "Google credentials has been loaded.")
except Exception as e:
    logger('critical-error', str(e))
