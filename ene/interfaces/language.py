from abc import ABCMeta, abstractmethod


class LanguageManager:
    def __init__(self, load_all=True):
        self.languages = []

    def load(self, language):
        pass

    def unload(self, language):
        pass


class LanguageAbstract(metaclass=ABCMeta):
    @abstractmethod
    def get_reply(self, message, client, groups=None):
        pass

    @abstractmethod
    def load_file(self, file_path):
        pass

    @abstractmethod
    def load_directory(self, dir_path):
        pass

    @property
    @abstractmethod
    def file_extensions(self):
        pass
