

class Translator(object):

    def __init__(self, __addon__):

        self.__addon__ = __addon__

    def lang(self, id):
        return self.__addon__.getLocalizedString(id).encode('utf-8', 'ignore')
