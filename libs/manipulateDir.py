# -*- coding:utf-8 -*-
# 若此模組的某一方法被引用，該方法中所需要的『其他模組』功能必須在此引用。
# 例如，儘管直接定義  _BASE_PATH = "/home/bluevc/2019/iSelect3C"，要是沒有import os ，也是無法執行函式mkdirForRawData。


import os
import sys
import json
import shutil #high level os


_BASE_PATH = "/".join(os.path.abspath(__file__).split("/")[:-2]) 
# sys.path.append(_BASE_PATH) # 因為此行生效，所以才能引用他處的module

class folderDataManipulate(object):
    _BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def __init__(self, **kwargs):
        self.origin = kwargs.get("origin", "")
        self.ultimate = kwargs.get("ultimate", "")
        self.transfer = kwargs.get("transfer", "")

    

    def writeOutFile(self, directory, fileName, fileReadyToWriteOut, writeOutType="w", encodingWay="utf-8"):

        with open(f"{directory}/{fileName}", writeOutType, encoding=encodingWay)as f:
            if not isinstance(fileReadyToWriteOut, str):
                f.write(str(fileReadyToWriteOut))
            else:
                f.write(fileReadyToWriteOut) #writelines作用在errorMessage是list時
    

    def writeOutMediaFile(self, directory, fileName, fileReadyToWriteOut, writeOutType="wb"):

        with open(f"{directory}/{fileName}", writeOutType)as f:
            f.write(fileReadyToWriteOut) #res.content
        
    

    def mkdirForRawData(self, mission, keyword=""):
        dirRoute = f"{self._BASE_PATH}/{mission}"
        
        try:
            if not os.path.isdir(dirRoute):
                os.makedirs(dirRoute)
                print(f"create folder success: {mission}.")
            else:
                print(f"{mission} folder already exists.")
        except OSError as e:   
            raise

    def copyFile(self, srcFilepath, dstFilepath, keyword=""):
        src = f"{self._BASE_PATH}/{srcFilepath}"
        dst = f"{self._BASE_PATH}/{dstFilepath}"
        shutil.copy(src, dst)
