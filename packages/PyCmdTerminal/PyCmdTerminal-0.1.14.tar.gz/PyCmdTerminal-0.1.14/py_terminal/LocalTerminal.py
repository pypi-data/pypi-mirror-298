import logging

from ._base import _Terminal


class LocalTerminal(_Terminal):
    def __init__(self, logger=logging.getLogger('LocalTerminal'), log_level=None):
        _Terminal.__init__(self, logger=logger, log_level=log_level)
