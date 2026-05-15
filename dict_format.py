from typing import TypedDict


# 1. نعرف شكل القاموس الخاص بالمنطقة الواحدة
class ZoneDict(TypedDict, total=False):
    key: str
    name: str
    x: str
    y: str
    color: str
    zone: str


# 2. نعرف شكل القاموس الخاص بالاتصال
class ConnectionDict(TypedDict):
    zon1: str
    zon2: str


# 3. أخيراً، نعرف شكل الخريطة الكلية التي استخرجتها أنت!
class ParsedMap(TypedDict):
    zones: list[ZoneDict]
    connections: list[ConnectionDict]
    nb_drones: str

# ---------------------------------------------
# الآن، عندما تعرّف المتغير الخاص بك، تكتبه هكذا: