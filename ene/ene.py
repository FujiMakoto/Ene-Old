#!/usr/bin/env python3.4
import logging
# from ene.models import ProtocolIrcNetwork as IrcNetwork
from ene.interfaces.language import LanguageFactory
from ene.interfaces.protocols.irc.connection import Irc


class Ene:
    def __init__(self, language='agentml'):
        self._log = logging.getLogger('ene')
        self.language = LanguageFactory.get(language)
        # self.network = IrcNetwork()
        self.start()

    def start(self):
        irc = Irc()
        irc.run()
