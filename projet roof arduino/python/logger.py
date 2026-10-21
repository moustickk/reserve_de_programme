import logging
import os

DATA_DIR = os.path.join(
    os.path.dirname(__file__),
    "data"
)

os.makedirs(DATA_DIR, exist_ok=True)

LOG_FILE = os.path.join(
    DATA_DIR,
    "roof.log"
)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s %(message)s"
)


def log(message):

    logging.info(message)