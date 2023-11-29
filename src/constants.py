from enum import Enum
from pathlib import Path


MAIN_DOC_URL = 'https://docs.python.org/3/'

MAIN_PEP_URL = 'https://peps.python.org/'

BASE_DIR = Path(__file__).parent

DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'

LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'

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


class OutputType(str, Enum):
    """Class for output choices template."""
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
