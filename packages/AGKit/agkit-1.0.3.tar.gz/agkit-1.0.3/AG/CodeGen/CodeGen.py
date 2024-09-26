import os

from AG.Base.Singleton import Singleton
from AG.Util.DirUtil import DirUtil


class CodeGen(Singleton):
    root = "Template"
    templateDict = {}

    def __init__(self):
        DirUtil.Check(self.root)

    def Init(self):
        for _, dirs, _ in os.walk(self.root):
            for dir in dirs:
                dir_path = "%s/%s" % (self.root, dir)
                for _, _, files in os.walk(dir_path):
                    for file in files:
                        file_path = "%s/%s" % (dir_path, file)
                        with open(file_path, 'r', encoding='utf8') as f:
                            content = f.read()
                            if dir not in self.templateDict.keys():
                                self.templateDict[dir] = {}
                            self.templateDict[dir][file] = content

    def Get(self, dir, file):
        return self.templateDict[dir][file]
