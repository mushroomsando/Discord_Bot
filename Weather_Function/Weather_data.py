import requests
from datetime import datetime, timedelta
import Weather_data_supplementary_information as Wi

#======== 계산 ========

def calculate_base_datetime(lookup_date, lookup_time):
    """
    기준 시간과 날짜를 계산하는 함수

    Args:
        lookup_date (str): 조회할 기준 날짜 (YYYYMMDD 형식).
        lookup_time (datetime.datetime): 조회할 기준 시간.

    Returns:
        tuple: 기준 시간과 날짜를 담은 튜플 (base_time, base_date)을 반환.
    """
    base_date = lookup_date
    lookup_hour = lookup_time.hour

    if lookup_hour < 2:
        base_time = "2300"
        # 전날 날짜로 설정
        base_date = str(int(lookup_date) - 1)
    elif lookup_hour < 5:
        base_time = "0200"
    elif lookup_hour < 8:
        base_time = "0500"
    elif lookup_hour < 11:
        base_time = "0800"
    elif lookup_hour < 14:
        base_time = "1100"
    elif lookup_hour < 17:
        base_time = "1400"
    elif lookup_hour < 20:
        base_time = "1700"
    else:
        base_time = "2000"

    return base_time, base_date

#========데이터 조회========

def get_ultra_short_live_check_raw_data(serviceKey,Lookup_date, Lookup_time, nx, ny):
    """
    기상청 API 에서 초단기 실황을 조회하는 함수

    Args:
        serviceKey (str): API 인증 키.
        lookup_date (str): 조회할 기준 날짜 (YYYYMMDD 형식).
        lookup_time (datetime.time): 조회할 기준 시간 (datetime.time 객체).
        nx (int): X 좌표 값.
        ny (int): Y 좌표 값.

    Returns:
        dict: 조회된 데이터를 딕셔너리 형태로 반환.
    """
    try:
        if Lookup_time.minute < 30:
            Lookup_time = Lookup_time.hour - 1
            print(Lookup_time)
        elif Lookup_time.minute >= 30:
            Lookup_time = Lookup_time.hour
            print(Lookup_time)

        url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'
        params = {
            'serviceKey': serviceKey,
            'pageNo': '1',
            'numOfRows': '8',
            'dataType': 'JSON',
            'base_date': Lookup_date,
            'base_time': str(Lookup_time) + "00",
            'nx': nx,
            'ny': ny
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        return data
    
    except requests.exceptions.RequestException as e:  # 추가: 네트워크 연결 오류 처리
        print("Error occurred during the API request:", e)
        return None
    except ValueError as e:  # 추가: JSON 디코딩 오류 처리
        print("Error occurred while decoding JSON data:", e)
        return None

def get_short_term_forecast_inquiry_raw_data(serviceKey, lookup_date, lookup_time, nx, ny):
    """
    기상청 API 에서 단기예보를 조회하는 함수

    Args:
        serviceKey (str): API 인증 키.
        lookup_date (str): 조회할 기준 날짜 (YYYYMMDD 형식).
        lookup_time (datetime.datetime): 조회할 기준 시간.
        nx (int): X 좌표 값.
        ny (int): Y 좌표 값.

    Returns:
        dict : 조회된 데이터를 딕셔너리 형태로 반환.
    """
    try:
        base_time, base_date = calculate_base_datetime(lookup_date, lookup_time)

        url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
        params = {
            'serviceKey': serviceKey,
            'pageNo': '1',
            'numOfRows': '96',
            'dataType': 'JSON',
            'base_date': base_date,
            'base_time': base_time,
            'nx': nx,
            'ny': ny
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        return data
    
    except requests.exceptions.RequestException as e:  # 추가: 네트워크 연결 오류 처리
        print("API 요청 중 오류가 발생했습니다:", e)
        return None
    except ValueError as e:  # 추가: JSON 디코딩 오류 처리
        print("JSON 데이터 디코딩 오류가 발생했습니다:", e)
        return None

# ========데이터 1차 가공========

def ultra_short_live_chek(raw_data):
    """
    초단기 실황 데이터를 가공하는 함수

    Args:
        raw_data (dic): 초단기 실황 데이터를 포함한 딕셔너리.

    Returns:
        dict: {'PTY' : 'value' ...} 식으로 데이터 반환.
    """
    obsr_values_dict = {}

    for item in raw_data['response']['body']['items']['item']:
        category = item['category']
        obsr_value = item['obsrValue']
        obsr_values_dict[category] = obsr_value
    
    return obsr_values_dict

def short_term_forecast(raw_data): # TODO 최적화
    # 현재 시간 설정
    now = datetime.now()
    today = now.date()
    today_date = today.strftime("%Y%m%d")
    hour = now.hour

    # 현재로부터 6시간 후의 시간 계산s
    forecast_time = now + timedelta(hours=6)
    forecast_date = forecast_time.date()
    forecast_hour = forecast_time.hour

    items = raw_data['response']['body']['items']['item']
    data = {}  # 예보 데이터 저장용 딕셔너리

    for item in items:
        fcst_date = item['fcstDate']
        fcst_time = item['fcstTime'][:2]
        category = item['category']
        value = item['fcstValue']
        
        # 현재 시간부터 6시간 후까지의 데이터만 저장
        if forecast_date > today or (today_date == fcst_date and hour <= int(fcst_time) <= forecast_hour):
            if fcst_time not in data:
                data[fcst_time] = {'date' : fcst_date}
            data[fcst_time][category] = value

    result = []

    for time,data in data.items():
        date = data['date'] # 날짜
        temperature = data['TMP'] # 온도
        humidity = data['REH'] # 습도
        wind_dir = data['VEC'] # 풍향
        wind_speed = data['WSD'] # 풍속
        precipitation_probability = data['POP'] # 강수확률
        precipitation_code = data['PTY'] # 강수코드 // 0:없음, 1:비, 2:비/눈, 3:눈, 4:소나기
        one_hour_precipitation = data['PCP'] # 1시간 강수량
        sky_code = data['SKY'] # 하늘코드 // 1:맑음, 3:구름많음, 4:흐림
        sky_emoji = Wi.get_sky_emoji(sky_code, precipitation_code)
        wind_dir_emji = Wi.get_visual_data(wind_dir,2,1)

        result.append({
            'time': time,
            'date': date,
            'temperature': temperature,
            'humidity': humidity,
            'wind_dir' : wind_dir,
            'wind_speed' : wind_speed,
            'precipitation_probability' : precipitation_probability,
            'precipitation_code' : precipitation_code,
            'one_hour_precipitation' : one_hour_precipitation,
            'sky_code' : sky_code,
            'sky_emoji' : sky_emoji,
            'wind_dir_emji' : wind_dir_emji
        })

    return result