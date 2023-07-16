import requests
import json
from datetime import datetime, timedelta

now = datetime.now()
today = now.date()
today_date = today.strftime("%Y%m%d")
hour = now.hour - 1

def load_api_key():
    with open('Wether_Function\\api_code.txtt', 'r') as file:
        return file.read().strip()

def get_weather_data():
    # 현재로부터 3시간 후의 시간 계산
    forecast_time = now + timedelta(hours=3)
    forecast_date = forecast_time.date()
    forecast_hour = forecast_time.hour

    # 요청할 날짜와 시간 설정
    if forecast_date > today:
        # 내일로 넘어간 경우
        base_date = forecast_date.strftime("%Y%m%d")
        base_time = "0200"  # 내일 2시부터 데이터 제공
    else:
        base_date = today_date
        base_time = str(hour).zfill(2) + "00"

    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
    params = {
        'serviceKey': load_api_key(),
        'pageNo': '1',
        'numOfRows': '1000',
        'dataType': 'JSON',
        'base_date': base_date,
        'base_time': base_time,
        'nx': 102, #TODO 데이더 설정
        'ny': 84 #TODO 데이터 설정
    }

    # API 호출
    res = requests.get(url, params=params)
    res_json = json.loads(res.content)

    # 필요한 데이터 추출
    items = res_json['response']['body']['items']['item']
    forecast_data = {}  # 예보 데이터 저장용 딕셔너리

    for item in items:
        fcst_date = item['fcstDate']
        fcst_time = item['fcstTime'][:2]
        category = item['category']
        value = item['fcstValue']

        # 현재 시간부터 3시간 후까지의 데이터만 저장
        if forecast_date > today or (today_date == fcst_date and hour <= int(fcst_time) <= forecast_hour):
            if fcst_time not in forecast_data:
                forecast_data[fcst_time] = {}
            forecast_data[fcst_time][category] = value

    return forecast_data

def get_now_weather():
    base_time = str(hour) + "00"
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'
    params = {
        'serviceKey': 'El5PQ9Ale6laNakJRp2x/24xBntXd3ghMdsKTGAuW1+Z5VLyIfw5eY8RwMDpklrCNw3YuffZ1ExyhA5ZLANvmg==',
        'pageNo': '1',
        'numOfRows': '1000',
        'dataType': 'JSON',
        'base_date': today_date,
        'base_time': base_time,
        'nx': 102,
        'ny': 84
    }

    response = requests.get(url, params=params)
    data = response.json()

    return data