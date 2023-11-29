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
