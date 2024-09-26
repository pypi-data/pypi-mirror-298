import configparser

from AG.Base.Singleton import Singleton
from AG.Util.FileUtil import FileUtil


class Setting(Singleton):
    FILE_NAME = "config.ini"
    data = None

    def __init__(self):
        pass

    def Get(self, section, key):
        result = self.data.get(section, key)
        return result

    def Init(self):
        if not FileUtil.Exists(self.FILE_NAME):
            content = """
[TableTool]
Lang=CSharp
Log=1
Root=D:\workspace\PackageDemo\Plan\Excel
ConfigSrc=D:\workspace\PackageDemo\Plan\Excel\Configs
DataDst=D:\workspace\GameTool\Excels\Output\Data\Config
CodeDst=D:\workspace\GameTool\Excels\Output\Code\Config
ConstSrc=D:\workspace\PackageDemo\Plan\Excel\Const
ConstDst=D:\workspace\GameTool\Excels\Output\Code\Const
EnumSrc=D:\workspace\PackageDemo\Plan\Excel\Enums
EnumDst=D:\workspace\GameTool\Excels\Output\Code\Enum
ClassSrc=D:\workspace\PackageDemo\Plan\Excel\Classes
ClassDst=D:\workspace\GameTool\Excels\Output\Code\Class
[PackTool]
Lang=CSharp
Log=1
Root=D:\workspace\PackageDemo\Tools\GameTool\input\proto
TempRoot=D:\workspace\PackageDemo\Tools\GameTool\input\\temp
CodeDst=D:\workspace\PackageDemo\Tools\GameTool\output
ProtocPath=D:\workspace\PackageDemo\Tools\GameTool\protoc-25.3-win64\\bin
"""
            FileUtil.Create(self.FILE_NAME, content, 'w', "gbk")
        self.data = configparser.ConfigParser()
        self.data.read(self.FILE_NAME)
