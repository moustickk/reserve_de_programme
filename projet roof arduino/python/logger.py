import os
import sys
from datetime import datetime


def get_base_path():

    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)

    return os.path.dirname(__file__)


BASE_DIR = get_base_path()

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)

os.makedirs(
    DATA_DIR,
    exist_ok=True
)

LOG_FILE = os.path.join(
    DATA_DIR,
    "roof.log"
)


def log(message):

    now = datetime.now()

    timestamp = now.strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    try:

        lines = []

        try:

            with open(
                LOG_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                for line in f:

                    try:

                        if line.startswith("["):

                            date_str = line[1:20]

                            log_date = datetime.strptime(
                                date_str,
                                "%Y-%m-%d %H:%M:%S"
                            )

                            age = (
                                now - log_date
                            ).total_seconds()

                            if age <= 48 * 3600:

                                lines.append(line)

                    except Exception:
                        pass

        except FileNotFoundError:
            pass

        lines.insert(
            0,
            f"[{timestamp}] {message}\n"
        )

        with open(
            LOG_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            f.writelines(lines)

    except Exception as ex:

        print(
            f"Erreur écriture log : {ex}"
        )