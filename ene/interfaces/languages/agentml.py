from ene.interfaces.language import LanguageAbstract
from agentml import AgentML


class AgentMlLanguage(LanguageAbstract):
    def __init__(self):
        self._aml = AgentML()

    def get_reply(self, message, client, groups=None):
        return self._aml.get_reply(client, message, groups)

    def load_file(self, file_path):
        self._aml.load_file(file_path)

    def load_directory(self, dir_path):
        self._aml.load_directory(dir_path)

    def file_extensions(self):
        return ['aml']
