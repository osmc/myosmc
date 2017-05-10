from string_manipulation import sanitize_string

import xbmc


class Logger(object):

    def __init__(self, whodisis):

        self.whodisis = whodisis

    def log(self, raw_message, level=xbmc.LOGDEBUG):

        message = sanitize_string(raw_message)

        xbmc.log(self.whodisis + ' ' + message, level=level)
