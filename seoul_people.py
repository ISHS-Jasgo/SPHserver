import time

import requests
import json
import pandas as pd
import schedule

df = pd.read_csv('./places.csv')

AREA_CD = df['AREA_CD'].tolist()
AREA_NM = df['AREA_NM'].tolist()
AREA_SIZE = df['AREA_SIZE'].tolist()


# print(AREA_CD)
# print(AREA_NM)


def send(placeNM):
    host = f"http://openapi.seoul.go.kr:8088/4e574f4441796f7537316758474875/json/citydata_ppltn/1/5/{AREA_CD[AREA_NM.index(placeNM)]}"
    res = requests.get(host)
    # print(res.text)
    data = json.loads(res.text)
    AREA_PPLTN_MIN = data['SeoulRtd.citydata_ppltn'][0]['AREA_PPLTN_MIN']
    AREA_PPLTN_MAX = data['SeoulRtd.citydata_ppltn'][0]['AREA_PPLTN_MAX']
    print(f"{placeNM}의 현재 인구는 {AREA_PPLTN_MIN} ~ {AREA_PPLTN_MAX}명 입니다.")
    return {
        "AREA_NM": placeNM,
        "AREA_PPLTN_MIN": AREA_PPLTN_MIN,
        "AREA_PPLTN_MAX": AREA_PPLTN_MAX
    }


def getPlaceSize(placeNM):
    return AREA_SIZE[AREA_NM.index(placeNM)]


def getAll():
    placeData = {
        "data": []
    }
    for placeNM in AREA_NM:
        placeData["data"].append(send(placeNM))
    return placeData


# def main():
#     schedule.every(5).minutes.do(getAll)
#     while True:
#         schedule.run_pending()
#         time.sleep(1)
#
#
# if __name__ == "__main__":
#     main()

