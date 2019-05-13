from logging import Formatter


class StdoutFormatter(Formatter):

    def __init__(self):
        fmt = '%(asctime)s - %(name)12s - %(levelname)s - %(message)s'
        super(StdoutFormatter, self).__init__(fmt)

    def format(self, record):
        record.name = record.name.replace('atomic_p2p.', '').upper()[:12]
        return super(StdoutFormatter, self).format(record)
