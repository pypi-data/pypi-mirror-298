from dataclasses import dataclass, asdict
import xml.etree.ElementTree as ET
import json

@dataclass
class BaseModel:
    def to_json(self) -> str:
        """Convert the instance to a JSON string."""
        return json.dumps(asdict(self), indent=4)
    
    def to_xml(self) -> str:
        """Convert the instance to an XML string."""
        root = ET.Element(self.__class__.__name__)
        for field, value in asdict(self).items():
            child = ET.SubElement(root, field)
            child.text = str(value)
        return ET.tostring(root, encoding='unicode', method='xml')

@dataclass
class EquityInfo(BaseModel):
    symbol: str
    nameOfCompany: str
    series: str
    dateOfListing: str
    isinNumber: str
    faceValue: int
    marketLot: int
    paidUpValue: int


@dataclass
class IndexInfo(BaseModel):
    key: str
    index: str
    indexSymbol: str
    last: float
    variation: float
    percentChange: float
    open: float
    high: float
    low: float
    previousClose: float
    yearHigh: float
    yearLow: float
    indicativeClose: int
    pe: str
    pb: str
    dy: str
    declines: str
    advances: str
    unchanged: str
    perChange365d: float
    date365dAgo: str
    chart365dPath: str
    date30dAgo: str
    perChange30d: float
    chart30dPath: str
    chartTodayPath: str
    previousDay: float
    oneWeekAgo: float
    oneMonthAgo: float
    oneYearAgo: float
