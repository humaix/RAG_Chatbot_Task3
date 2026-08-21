import logging
from pathlib import Path

def get_logger(name):
    log_folder = Path("storage/logs")
    log_folder.mkdir(parents=True,exist_ok=True)
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        file = logging.FileHandler(log_folder / "application.log",encoding="utf-8")
        file.setFormatter(formatter)
        logger.addHandler(console)
        logger.addHandler(file)
    return logger

