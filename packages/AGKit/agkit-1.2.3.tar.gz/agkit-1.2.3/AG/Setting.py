import configparser

from AG.Logger import Logger
from AG.Singleton import Singleton
from AG.FileUtil import FileUtil


class Setting(Singleton):
    data = None

    def __init__(self):
        self.file_name = ""

    def Get(self, section, key):
        result = self.data.get(section, key)
        return result

    def Init(self, file_name):
        self.file_name = file_name
        if not FileUtil.Exists(self.file_name):
            Logger.Instance.Info(f"没有找到配置文件：{self.file_name}")
            return
        self.data = configparser.ConfigParser()
        self.data.read(self.file_name, encoding="utf8")
