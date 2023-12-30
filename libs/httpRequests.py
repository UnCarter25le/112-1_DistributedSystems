# -*- coding:utf-8 -*-
# 若此模組的某一方法被引用，該方法中所需要的『其他模組』功能必須在此引用。


import os 
import sys
import requests
from bs4 import BeautifulSoup
import json

_BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(_BASE_PATH)



class httpClientBuild(object):
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9", "Connection": "close"}
    resencoding = "big5"
    targetUrl = "https://www.cartoonmad.com"
    hotComicToday = "https://www.cartoonmad.com"#"https://www.cartoonmad.com/hotrank.html"


    # def getHotComicList(self):
    #     # https://tw.manhuagui.com/rank/ 漫畫櫃
    #     res = requests.get(self.hotComicToday, headers=self.headers)
    #     res.encoding = 'utf-8'
    #     soup = BeautifulSoup(res.text, 'html.parser')
    #     comicTrList = soup.find("div", {"class":"top-cont shadow-gray"}).find("table").find_all("tr")[2:12]
    #     resJson = {}
    #     for trNode in comicTrList:
    #         no = trNode.select_one(".rank-no").text
    #         comicName = trNode.select_one(".rank-title").find("h5").text
    #         comicUrl = trNode.select_one(".rank-title").find("h5").find("a").attrs.get("href")

    #         resJson[no] = {"comic" : comicName, "comicUrl" : self.targetUrl+comicUrl}
            

    #     return resJson
    
    def getHotComicList(self):
        # https://www.cartoonmad.com/hotrank.html 動漫狂
        res = requests.get(self.hotComicToday, headers=self.headers)
        res.encoding = self.resencoding
        soup = BeautifulSoup(res.text, 'html.parser')
        
        comicTrList = soup.find_all("a", {"class" : "a1"})[:12]
        # comicTrList = [row for row in comicTrList if row.attrs.get("onmouseover", "") == ""]
        comicTrStatusList = soup.find_all("a", {"class" : "a2", "target":"_blank"})[:12]

        comicList = zip(comicTrList, comicTrStatusList)
        
        resJson = {}
        i = 1
        for row in comicList:
          no = str(i)
          i += 1
          comicName = row[0].text.replace("\xa0 \xa0", "").replace(" ", "")
          comicUrl = row[0].attrs.get("href")
          comicStatus = row[1].text.replace("\xa0 \xa0", "").replace(" ", "").replace("更新到", "")
          resJson[no] = {"comic" : comicName, "comicUrl" : f"{self.targetUrl}/{comicUrl}", "comicStatus" : comicStatus}

        return resJson    
    
    def getEpisode(self, comicUrl, latest=True):
        if latest == True:
          
          comicNumCode = comicUrl
          res = requests.get(comicUrl, headers=self.headers)
          res.encoding = self.resencoding
          soup = BeautifulSoup(res.text, 'html.parser')
          episodes = soup.find_all("fieldset", {"id":"info"})[1].find_all("tr")
          
          tmp = []
          for tds in episodes:
             for row in tds:
                if row.find("a") != None and row.find("font") != None:
                   tmp.append(row)
          tmp = [row for row in tmp if row != '\n']
          latestEpisode = tmp[-1]
          episodeUrl = self.targetUrl + latestEpisode.find("a").attrs.get("href")
          episode = latestEpisode.find("a").text.replace(" ", "")
          limitPage = latestEpisode.find("font").text.replace("(", "").replace(")", "").replace("頁", "")
          episodeJson = {"episode" : episode, "episodeUrl" : episodeUrl, "limitPage" : limitPage}
          


          return episodeJson    
    
    def downloadPage(self, pageUrl, filepath):
        dirRoute = f"{_BASE_PATH}/HotComicToday/{filepath}"
        res = requests.get(f"https://cc.fun8.us//2e5fc/{pageUrl}",  headers=self.headers)      
        with open(dirRoute, 'wb') as f:
            f.write(res.content)                    
    

# client = httpClientBuild()
# print(json.dumps(client.getHotComicList(), indent=2, ensure_ascii=False))
# print(json.dumps(client.getEpisode("https://www.cartoonmad.com/comic/3583.html"), indent=2, ensure_ascii=False))

"""getEpisode
{
  "episode": "第244話",
  "episodeUrl": "https://www.cartoonmad.com/comic/358302442016001.html",
  "limitPage": "16"
}
"""
"""getHotComicList
{
  "1": {
    "comic": "咒術回戰",
    "comicUrl": "https://www.cartoonmad.com/comic/7654.html",
    "comicStatus": "更新到第 247 話   "
  },
  "2": {
    "comic": "海賊王",
    "comicUrl": "https://www.cartoonmad.com/comic/1152.html",
    "comicStatus": "更新到第 1103 話   "
  },
  "3": {
    "comic": "一拳超人",
    "comicUrl": "https://www.cartoonmad.com/comic/3583.html",
    "comicStatus": "更新到第 244 話   "
  },
  "4": {
    "comic": "我的英雄學院",
    "comicUrl": "https://www.cartoonmad.com/comic/4085.html",
    "comicStatus": "更新到第 410 話   "
  },
  "5": {
    "comic": "王者天下",
    "comicUrl": "https://www.cartoonmad.com/comic/1122.html",
    "comicStatus": "更新到第 783 話   "
  },
  "6": {
    "comic": "電鋸人",
    "comicUrl": "https://www.cartoonmad.com/comic/8151.html",
    "comicStatus": "更新到第 151 話   "
  },
  "7": {
    "comic": "拳願奧米迦",
    "comicUrl": "https://www.cartoonmad.com/comic/8206.html",
    "comicStatus": "更新到第 242 話   "
  },
  "8": {
    "comic": "DR.STONE",
    "comicUrl": "https://www.cartoonmad.com/comic/5531.html",
    "comicStatus": "更新到第 232 話   "
  },
  "9": {
    "comic": "進擊的巨人",
    "comicUrl": "https://www.cartoonmad.com/comic/1221.html",
    "comicStatus": "更新到第 139 話   "
  },
  "10": {
    "comic": "間諜過家家",
    "comicUrl": "https://www.cartoonmad.com/comic/8223.html",
    "comicStatus": "更新到第 92 話   "
  },
  "11": {
    "comic": "平行天堂",
    "comicUrl": "https://www.cartoonmad.com/comic/5564.html",
    "comicStatus": "更新到第 244 話   "
  },
  "12": {
    "comic": "入間同學入魔了",
    "comicUrl": "https://www.cartoonmad.com/comic/5677.html",
    "comicStatus": "更新到第 329 話   "
  }
}
"""
