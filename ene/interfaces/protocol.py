import logging
import threading
from abc import ABCMeta, abstractmethod


class ProtocolManager:
    pass


class ProtocolFactory:
    pass


class ProtocolAbstract(metaclass=ABCMeta):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass
