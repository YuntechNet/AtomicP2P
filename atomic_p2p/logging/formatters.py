from logging import Formatter


class StdoutFormatter(Formatter):
    def __init__(self):
        fmt = "%(asctime)s - %(name)12s - %(levelname)5s - %(message)s"
        super().__init__(fmt)

    def format(self, record):
        record.name = record.name.replace("atomic_p2p.", "").upper()[:12]
        return super().format(record)
