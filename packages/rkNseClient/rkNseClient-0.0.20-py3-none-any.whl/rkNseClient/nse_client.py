import re
import requests
import io
import pandas as pd
import numpy as np

from .utils import fix_invalid_json_getIndicesWeightage

from .schema import *


class NSEClient:
    def __init__(self):
        self.baseURL = "https://www.nseindia.com/"
        self.userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        self.cookies = {}
        self.equityQuotes = {}
        self.initialRequest()

    def setCookies(self, response: requests.Response):
        self.cookies.update(response.cookies.get_dict())

    def urlParser(self, url: str):
        parsed_url = url.replace("&", "%26").replace(" ", "%20")
        return parsed_url
    
    def initialRequest(self):
        response = requests.request("GET", self.baseURL, headers={
                                    "User-Agent": self.userAgent})
        if response.ok:
            self.setCookies(response=response)
        else:
            print(response.text)

    def getEquityList(self) -> list[EquityInfo]:
        url = "https://nsearchives.nseindia.com/content/equities/EQUITY_L.csv"
        response = requests.request("GET", url, headers={
                                    "User-Agent": self.userAgent}, cookies=self.cookies, timeout=30)
        self.setCookies(response=response)
        newList = []
        if response.ok:
            df = pd.read_csv(io.StringIO(response.text))
            df = df.replace({np.nan: None})
            for each in df.to_dict("records"):
                eachEquityData = EquityInfo(symbol=each["SYMBOL"],
                                            nameOfCompany=each["NAME OF COMPANY"],
                                            series=each[" SERIES"],
                                            dateOfListing=each[" DATE OF LISTING"],
                                            paidUpValue=each[" PAID UP VALUE"],
                                            marketLot=each[" MARKET LOT"],
                                            isinNumber=each[" ISIN NUMBER"],
                                            faceValue=each[" FACE VALUE"])
                newList.append(eachEquityData)
            return newList
        else:
            print(response.text)
            return None

    def getAllIndices(self) -> list[IndexInfo]:
        url = "https://www.nseindia.com/api/allIndices"
        response = requests.request("GET", url, headers={"User-Agent": self.userAgent}, cookies=self.cookies, timeout=30)
        self.setCookies(response=response)
        newList = []
        if response.ok:
            allIndices = response.json()
            for eachIndices in allIndices.get("data", []):
                eachIndexInfo = IndexInfo(key = eachIndices.get("key"),
                                    index = eachIndices.get("index"),
                                    indexSymbol = eachIndices.get("indexSymbol"),
                                    last = eachIndices.get("last"),
                                    variation = eachIndices.get("variation"),
                                    percentChange = eachIndices.get("percentChange"),
                                    open = eachIndices.get("open"),
                                    high = eachIndices.get("high"),
                                    low = eachIndices.get("low"),
                                    previousClose = eachIndices.get("previousClose"),
                                    yearHigh = eachIndices.get("yearHigh"),
                                    yearLow = eachIndices.get("yearLow"),
                                    indicativeClose = eachIndices.get("indicativeClose"),
                                    pe = eachIndices.get("pe"),
                                    pb = eachIndices.get("pb"),
                                    dy = eachIndices.get("dy"),
                                    declines = eachIndices.get("declines"),
                                    advances = eachIndices.get("advances"),
                                    unchanged = eachIndices.get("unchanged"),
                                    perChange365d = eachIndices.get("perChange365d"),
                                    date365dAgo = eachIndices.get("date365dAgo"),
                                    chart365dPath = eachIndices.get("chart365dPath"), 
                                    date30dAgo = eachIndices.get("date30dAgo"), 
                                    perChange30d = eachIndices.get("perChange30d"), 
                                    chart30dPath = eachIndices.get("chart30dPath"), 
                                    chartTodayPath = eachIndices.get("chartTodayPath"),
                                    previousDay = eachIndices.get("previousDay"), 
                                    oneWeekAgo = eachIndices.get("oneWeekAgo"), 
                                    oneMonthAgo = eachIndices.get("oneMonthAgo"), 
                                    oneYearAgo = eachIndices.get("oneYearAgo")
                                    )
                newList.append(eachIndexInfo)
            return newList
        else:
            print(response.text)
            return None

    def getIndicesWeightage(self, indicesName: str) -> list[IndexSectorWeightageInfo]:
        url = f"https://iislliveblob.niftyindices.com/jsonfiles/SectorialIndex/SectorialIndexData{self.urlParser(indicesName)}.js"
        response = requests.get(url)
        if response.ok:
            js_content = response.text
            match = re.search(r'modelDataAvailable\((.*)\)', js_content, re.DOTALL)
            if match:
                json_data_str = match.group(1)
                try:
                    json_data_str = fix_invalid_json_getIndicesWeightage(json_data_str)
                    json_data = json.loads(json_data_str)
                    new_list = []
                    for eachSector in json_data["groups"]:
                        indexStockWeightageList = []
                        for eachStock in eachSector.get("groups"):
                            indexStockWeightageList.append(IndexStockWeightageInfo(symbol="".join(eachStock.get("label").split(" ")[:-1]), weight=eachStock.get("weight")))
                        indexSectorWeightageInfo = IndexSectorWeightageInfo(sector="".join(eachSector.get("label").split(" ")[:-1]),
                                                weight=eachSector.get("weight"),
                                                stocks=indexStockWeightageList)
                        new_list.append(indexSectorWeightageInfo)
                    return new_list
                except json.JSONDecodeError:
                    print("Failed to decode JSON.")
                    return None
            else:
                print("JSON data not found in the JS content.")
                return None
