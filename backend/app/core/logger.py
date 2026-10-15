from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent.parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(module)s.%(funcName)s:%(lineno)d | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class FunctionDateErrorFileHandler(logging.Handler):
    """
    Кастомний обробник для запису помилок (ERROR та вище)
    у структуру: logs/<назва_функції>/<YYYY-MM-DD>.log
    """
    def __init__(self, base_dir: Path, level=logging.ERROR):
        super().__init__(level=level)
        self.base_dir = base_dir

    def emit(self, record: logging.LogRecord) -> None:
        try:
            if record.levelno < logging.ERROR:
                return

            func_name = record.funcName or "root"
            date_str = datetime.now().strftime("%Y-%m-%d")

            # Папка з назвою функції: logs/<назва_функції>/
            func_dir = self.base_dir / func_name
            func_dir.mkdir(parents=True, exist_ok=True)

            log_file = func_dir / f"{date_str}.log"
            msg = self.format(record)

            with open(log_file, "a", encoding="utf-8") as f:
                f.write(msg + "\n")
        except Exception:
            self.handleError(record)


def setup_logger(name: str = "diia_test_task_app") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if logger.handlers:
        return logger

    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)

    # Загальний лог роботи застосунку (макс. 5 МБ, зберігаємо 10 файлів)
    info_handler = RotatingFileHandler(
        LOG_DIR / "app.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=10,
        encoding="utf-8",
    )
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(formatter)

    # Логування помилок за структурою: logs/<назва_функції>/<YYYY-MM-DD>.log
    error_handler = FunctionDateErrorFileHandler(LOG_DIR, level=logging.ERROR)
    error_handler.setFormatter(formatter)

    # Вивід у консоль Docker
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(info_handler)
    logger.addHandler(error_handler)
    logger.addHandler(console_handler)

    return logger


logger = setup_logger()