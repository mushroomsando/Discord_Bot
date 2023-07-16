import requests
from datetime import datetime, timedelta
from collections import defaultdict
import json

today = datetime.today()
today_date = today.strftime("%Y%m%d")

def load_api_key():
    with open('Wether_Function\\api_code.txt', 'r') as file:
        return file.read().strip()

def get_base_time():
    current_time = datetime.now()
    current_hour = current_time.hour

    if current_hour < 2:
        base_time = "2300"
    elif current_hour < 5:
        base_time = "0200"
    elif current_hour < 8:
        base_time = "0500"
    elif current_hour < 11:
        base_time = "0800"
    elif current_hour < 14:
        base_time = "1100"
    elif current_hour < 17:
        base_time = "1400"
    elif current_hour < 20:
        base_time = "1700"
    else:
        base_time = "2000"

    return base_time

def get_current_base_time():
    now = datetime.now()
    hour = now.hour
    minute = now.minute

    update_time = "0030 0130 0230 0330 0430 0530 0630 0730 0830 0930 1030 1130 1230 1330 1430 1530 1630 1730 1830 " \
                  "1930 2030 2130 2230 2330".split()

    if (hour < 1) and (minute < 30):
        base_time = update_time[23]
    elif (hour >= 1) and (minute < 30):
        base_time = update_time[hour - 1]
    else:
        base_time = update_time[hour]

    return base_time

def get_weather_Forecast_data(api_key):
    # 현재 시간 설정
    now = datetime.now()
    base_time = get_base_time()
    hour = now.hour - 1
    yesterday = today - timedelta(days=1)
    yesterday_date = yesterday.strftime("%Y%m%d")

    # 현재로부터 6시간 후의 시간 계산
    forecast_time = now + timedelta(hours=5)
    forecast_date = forecast_time.strftime("%Y%m%d")
    forecast_hour = forecast_time.hour

    # 내일의 날짜 계산
    tomorrow = now + timedelta(days=1)
    tomorrow_date = tomorrow.strftime("%Y%m%d")

    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
    params = {
        'serviceKey': api_key,
        'pageNo': '1',
        'numOfRows': '1000',
        'dataType': 'JSON',
        'base_date': today_date if hour >= 2 else yesterday_date,
        'base_time': base_time,
        'nx': 102,
        'ny': 84
    }

    # API 호출
    res = requests.get(url, params=params)
    res_json = json.loads(res.content)

    # 필요한 데이터 추출
    items = res_json['response']['body']['items']['item']
    forecast_data = defaultdict(dict)  # 예보 데이터 저장용 딕셔너리

    for item in items:
        fcst_date = item['fcstDate']
        fcst_time = item['fcstTime'][:2]
        category = item['category']
        value = item['fcstValue']

        if (fcst_date == today_date and hour <= int(fcst_time) <= forecast_hour) or (fcst_date == forecast_date and int(fcst_time) <= forecast_hour):
            forecast_data[fcst_time][category] = value

    return forecast_data

def get_now_weather(api_key):
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'
    params = {
        'serviceKey': api_key,
        'pageNo': '1',
        'numOfRows': '1000',
        'dataType': 'JSON',
        'base_date': today_date,
        'base_time': get_current_base_time(),
        'nx': 102,
        'ny': 84
    }

    response = requests.get(url, params=params)
    data = json.loads(response.content)

    return data