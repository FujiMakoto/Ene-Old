from abc import ABCMeta, abstractmethod
from pkg_resources import load_entry_point


class LanguageFactory:
    @staticmethod
    def get(language):
        return load_entry_point('ene', 'ene.interfaces.languages', language)()


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
