from enum import Enum
from pathlib import Path

# Python docs main url.
MAIN_DOC_URL = 'https://docs.python.org/3/'
# Python pep list url.
MAIN_PEP_URL = 'https://peps.python.org/'
# Project base dir.
BASE_DIR = Path(__file__).parent
# Datetime formatting template.
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
# Logging formatting template.
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
# PEP's expected statuses.
EXPECTED_STATUS = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred',),
    'F': ('Final',),
    'P': ('Provisional',),
    'R': ('Rejected',),
    'S': ('Superseded',),
    'W': ('Withdrawn',),
    '': ('Draft', 'Active'),
}
# PEP's statuses counters.
PEP_STATUS_COUNTER = {
    'Active': 0,
    'Accepted': 0,
    'Deferred': 0,
    'Final': 0,
    'Provisional': 0,
    'Rejected': 0,
    'Superseded': 0,
    'Withdrawn': 0,
    'Draft': 0,
    'Other': 0
}


# Class for output choices template
class OutputType(str, Enum):
    PRETTY = 'pretty'
    FILE = 'file'


DEFAULT_RESPONSE_ENCODING = 'utf-8'
DEFAULT_PARSE_MODE = 'lxml'


class RegexpTemplates:
    '''Class for storing regexp templates. '''
    # Template for finding CSS-class "rfc2822...".
    RFC_TEMPLATE = r'rfc2822 \w+'
    # Template for finding tag text like "Python version 3.11 (stable)".
    PYTHON_VERSION_TEMPLATE = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    # Template for finding link to download doc files in pdf format.
    DOCS_PDF_DOWNLOAD_TEMPLATE = r'.+pdf-a4\.zip$'
