# -*- coding:utf-8 -*-
# 若此模組的某一方法被引用，該方法中所需要的『其他模組』功能必須在此引用。


import os 
import sys
import requests
from bs4 import BeautifulSoup
import json

_BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(_BASE_PATH)
print(_BASE_PATH)



class httpClientBuild(object):
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9", "Connection": "close"}
    targetUrl = "https://tw.manhuagui.com"
    hotComicToday = "https://tw.manhuagui.com/rank"


    def getHotComicList(self):
        res = requests.get(self.hotComicToday, headers=self.headers)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')
        comicTrList = soup.find("div", {"class":"top-cont shadow-gray"}).find("table").find_all("tr")[2:12]
        resJsonArr = []
        for trNode in comicTrList:
            no = trNode.select_one(".rank-no").text
            comicName = trNode.select_one(".rank-title").find("h5").text
            comicUrl = trNode.select_one(".rank-title").find("h5").find("a").attrs.get("href")

            resJsonArr.append({no : {"comic" : comicName, "comicUrl" : self.targetUrl+comicUrl}})

        return resJsonArr
    

# client = httpClientBuild()
# print(json.dumps(client.getHotComicList(), indent=2, ensure_ascii=False))
"""
[
  {
    "1": {
      "comic": "一拳超人",
      "comicUrl": "https://tw.manhuagui.com/comic/7580/"
    }
  },
  {
    "2": {
      "comic": "ONE PIECE航海王",
      "comicUrl": "https://tw.manhuagui.com/comic/1128/"
    }
  },
  {
    "3": {
      "comic": "成為鐵匠在異世界度過悠閒人生",
      "comicUrl": "https://tw.manhuagui.com/comic/43661/"
    }
  },
  {
    "4": {
      "comic": "香格里拉·弗隴提亞~屎作獵人向神作發起挑戰~",
      "comicUrl": "https://tw.manhuagui.com/comic/36998/"
    }
  },
  {
    "5": {
      "comic": "想當冒險者的女兒到首都當了等級S的冒險者",
      "comicUrl": "https://tw.manhuagui.com/comic/28399/"
    }
  },
  {
    "6": {
      "comic": "再構築世界",
      "comicUrl": "https://tw.manhuagui.com/comic/32868/"
    }
  },
  {
    "7": {
      "comic": "異世界Green hat man～用最強技能讓基友的女人惡墮 ～",
      "comicUrl": "https://tw.manhuagui.com/comic/34743/"
    }
  },
  {
    "8": {
      "comic": "來做吧，精靈大姐姐",
      "comicUrl": "https://tw.manhuagui.com/comic/46379/"
    }
  },
  {
    "9": {
      "comic": "異世界玩家用HP1 進行最強最快的迷宮攻略",
      "comicUrl": "https://tw.manhuagui.com/comic/31582/"
    }
  },
  {
    "10": {
      "comic": "一覺醒來坐擁神裝和飛船，我決定以買一套獨門獨戶的房子為目��作為傭兵自由地活下去",
      "comicUrl": "https://tw.manhuagui.com/comic/35598/"
    }
  }
]

"""
