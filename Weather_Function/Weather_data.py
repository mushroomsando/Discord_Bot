import requests
import math

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
        elif Lookup_time.minute >= 30:
            Lookup_time = Lookup_time.hour

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

def get_short_term_forecast_inquiry_raw_data(serviceKey, Lookup_date, Lookup_time, nx, ny):
    """
    기상청 API 에서 단기예보를 조회하는 함수

    Args:
        serviceKey (str): API 인증 키.
        lookup_date (str): 조회할 기준 날짜 (YYYYMMDD 형식).
        lookup_time (int): 조회할 기준 시간 (0 ~ 23 사이의 정수).
        nx (int): X 좌표 값.
        ny (int): Y 좌표 값.

    Returns:
        dict: 조회된 데이터를 딕셔너리 형태로 반환.
    """
    try:
        Lookup_time = Lookup_time.hour
        if Lookup_time < 2:
            base_time = "2300"
        elif Lookup_time < 5:
            base_time = "0200"
        elif Lookup_time < 8:
            base_time = "0500"
        elif Lookup_time < 11:
            base_time = "0800"
        elif Lookup_time < 14:
            base_time = "1100"
        elif Lookup_time < 17:
            base_time = "1400"
        elif Lookup_time < 20:
            base_time = "1700"
        else:
            base_time = "2000"

        url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
        params = {
            'serviceKey': serviceKey,
            'pageNo': '1',
            'numOfRows': '96',
            'dataType': 'JSON',
            'base_date': Lookup_date,
            'base_time': base_time,
            'nx': nx,
            'ny': ny
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        return data, base_time
    
    except requests.exceptions.RequestException as e:  # 추가: 네트워크 연결 오류 처리
        print("Error occurred during the API request:", e)
        return None
    except ValueError as e:  # 추가: JSON 디코딩 오류 처리
        print("Error occurred while decoding JSON data:", e)
        return None

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

def short_term_forecast(raw_data):
    """
    단기예보 데이터를 가공하는 함수

    Args:
        raw_data (dict): 단기 예보 데이터를 포함한 딕셔너리.

    Returns:
        dict: 카테고리별로 단기예보 데이터를 저장한 딕셔너리.
            딕셔너리의 형태는 다음과 같습니다:
            {
                '카테고리1': {
                    'fcstValue': '예보값',
                    'fcstDate': '예보날짜',
                    'fcstTime': '예보시간'
                },
                '카테고리2': {
                    'fcstValue': '예보값',
                    'fcstDate': '예보날짜',
                    'fcstTime': '예보시간'
                },
                ...
            }
    """
    # 'item'에 해당하는 데이터들을 카테고리별로 저장하는 딕셔너리 생성
    forecast_data_dict = {}

    # 'item' 리스트 순회하며 카테고리별로 데이터 추가
    for item in raw_data['response']['body']['items']['item']:
        category = item['category']
        fcst_value = item['fcstValue']
        fcst_date = item['fcstDate']
        fcst_time = item['fcstTime']
        forecast_data_dict[category] = {
            'fcstValue': fcst_value,
            'fcstDate': fcst_date,
            'fcstTime': fcst_time
        }

    return forecast_data_dict