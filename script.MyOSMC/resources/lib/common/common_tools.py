import xbmc


def hardware_version():

	raise NotImplementedError


def sanitize_string(string):

	try:
		return str(string)
	except UnicodeEncodeError:
		return string.encode('utf-8', 'ignore' )


class language(object):

	def __init__(self, __addon__):

		self.__addon__ = __addon__

	def lang(self, id):
	    return self.__addon__.getLocalizedString(id).encode( 'utf-8', 'ignore' ) 


class logger(object):

	def __init__(self, whodisis):

		self.whodisis = whodisis

	def log(self, raw_message, level=xbmc.LOGDEBUG):

		message = sanitize_string(raw_message)

		xbmc.log(self.whodisis + ' ' + message, level=level)

