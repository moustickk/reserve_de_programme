import logging

logging.basicConfig(
    filename="roof.log",
    level=logging.INFO,
    format="%(asctime)s %(message)s"
)


def log(message):

    logging.info(message)