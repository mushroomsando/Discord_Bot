import json
import requests
import math
from datetime import date, timedelta, datetime
import time

#======== 계산 ========
#TODO API 구조조정
#단기예보와 초단기예보를 중점으로 사용예정. 단기예보는 현재날씨와 6시간 동안의 날씨를 당담하고, 단기예보는 그 이후의 날씨 예보를 당담함.

def get_base_time():
    """
    기상청 API 에서 단기예보를 조회하기 위해 시간을 계산하는 함수

    Args:
        null

    Returns:
        time
    """
    current_time = datetime.now()
    base_times = [200, 500, 800, 1100, 1400, 1700, 2000, 2300]
    
    # 현재 시간을 시간과 분으로 분리
    current_hour = current_time.hour
    current_minute = current_time.minute
    
    # 현재 시간의 분을 기준으로 이전과 이후 base_time을 확인
    if current_minute >= 30:
        current_hour += 1

    # 현재 시간에서 가장 가까운 이전 base_time 찾기
    for base_time in reversed(base_times):
        if current_hour >= base_time // 100:
            return datetime(current_time.year, current_time.month, current_time.day, base_time // 100, 0)

    # 현재 시간이 모든 base_time보다 작다면, 전날의 가장 뒤에 있는 base_time 반환
    return datetime(current_time.year, current_time.month, current_time.day, base_times[-1] // 100, 0) - timedelta(days=1)

# print("가장 가까운 이전 base_time:", get_base_time().strftime("%Y%m%d")) TEST

#========데이터 조회========
def short_wewather(nx, ny):
    """
    기상청 API 에서 초단기예보를 조회하는 함수

    Args:
        nx (int): X 좌표 값.
        ny (int): Y 좌표 값.

    Returns:
        dict : 조회된 데이터를 딕셔너리 형태로 반환.
    """
    servicekey = open("Weather_API\\api_code.txt", "r")
    time = datetime.now().hour
    try:
        url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst'
        params = {
            'serviceKey': servicekey.read(),
            'pageNo': '1',
            'numOfRows': '96',
            'dataType': 'JSON',
            'base_date': (datetime.now() - timedelta(days=1)).strftime("%Y%m%d") if datetime.now().hour == 0 else datetime.now().strftime("%Y%m%d"),
            'base_time': f"{(time - 1) % 24:02d}30" if time > 0 else "0030",
            'nx': nx,
            'ny': ny
        }
        print(f"호출키 : {params}" )

        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if data['response']['header']['resultCode'] == "03": # 추가 : 데이터가 없는 오류 처리리
            print("데이터가 없습니다.")
            return None
        
        return data
    
    except requests.exceptions.RequestException as e:  # 추가: 네트워크 연결 오류 처리
        print("API 요청 중 오류가 발생했습니다:", e)
        return None
    except ValueError as e:  # 추가: JSON 디코딩 오류 처리
        print("JSON 데이터 디코딩 오류가 발생했습니다:", e)
        return None

# print(short_wewather(101, 84)) #TEST

# ========데이터 가공========

def data_process(raw_data):
    """
    단기예보 데이터를 가공하는 함수

    Args:
        raw_data (dic): 단기예보 데이터를 포함한 딕셔너리

    Returns:
        list: [{'time': value, 'date': value, 'temperature':value, ... }] 식으로 데이터 반환
    """

    data = {}  # 예보 데이터 저장용 딕셔너리

    for item in raw_data['response']['body']['items']['item']:
        fcst_date = item['fcstDate']
        fcst_time = item['fcstTime'][:2]
        category = item['category']
        value = item['fcstValue']
        data.setdefault(fcst_time, {'date': fcst_date})
        data[fcst_time][category] = value

    result = []
    for time, data in data.items():
        temperature = data.get('T1H', 'N/A')
        precipitation_1h = data.get('RN1', 'N/A')
        sky_code = data.get('SKY', '1')
        humidity = data.get('REH', 'N/A')
        precipitation_type = data.get('PTY', '0')
        lightning = data.get('LGT', 'N/A')
        wind_dir = data.get('VEC', '0')
        wind_speed = data.get('WSD', 'N/A')

        result.append({
            'time': time,
            'date': data['date'],
            'temperature': temperature,
            'precipitation_1h': precipitation_1h,
            'sky_code': sky_code,
            'humidity': humidity,
            'precipitation_type': precipitation_type,
            'lightning': lightning,
            'wind_dir': wind_dir,
            'wind_speed': wind_speed,
            'sky_emoji': "작업중",
            'wind_dir_emoji': "작업중"
        })

    json_result = json.dumps(result, ensure_ascii=False)
    return json_result

# print(data_process(short_wewather(101, 84))) # TEST

def discomfort_index(Ta, RH):
    """
    체감온도를 구하는 함수
    
    Args:
        Ta(int) : 온도
        RH(int) : 습도
        V(int) : 풍속

    Retruns:
        int : 체감온도
    """
    now = datetime.now()
    month = now.month

    Tw = Ta * math.atan(0.151977 * math.sqrt(RH + 8.313659)) + math.atan(Ta + RH) - math.atan(RH - 1.67633) + 0.00391838 * math.pow(RH, 1.5) * math.atan(0.023101 * RH) - 4.686035
    discomfort_index = -0.2442 + 0.55399 * Tw + 0.45535 * Ta - 0.0022 * math.pow(Tw, 2) + 0.00278 * Tw * Ta + 3.0
    return discomfort_index

if __name__ == "__main__":
    start_time = time.time()
    pass_count = 0

    # get_base_time 함수 테스트
    try:
        base_time_result = get_base_time()
        print("가장 가까운 이전 base_time:", base_time_result.strftime("%Y%m%d-%H%M"))
        pass_count += 1
    except Exception as e:
        print(f"Error in get_base_time: {e}")

    # short_wewather 함수 테스트
    nx_sample, ny_sample = 101, 84 #테스트용 좌표. 울산광역시 중구 다운동
    weather_data = None
    try:
        weather_data = short_wewather(nx_sample, ny_sample)
        if weather_data is not None:
            print("초단기예보 데이터 조회 성공")
            pass_count += 1
        else:
            raise ValueError("데이터가 없습니다. 시간처리 과정에서 문제가 발생했을수 있습니다.")
    except Exception as e:
        print(f"Error in short_wewather: {e}")

    # data_process 함수 테스트
    try:
        if weather_data is not None:
            processed_data = data_process(weather_data)
            print("데이터 처리 성공")
            pass_count += 1
        else:
            raise ValueError("데이터가 없습니다. 시간처리 과정에서 문제가 발생했을수 있습니다.")
    except Exception as e:
        print(f"Error in data_process: {e}")

    # discomfort_index 함수 테스트
    temperature_sample, humidity_sample = 25, 60 #테스트용 데이터. 정상값은 25
    try:
        discomfort_index_value = discomfort_index(temperature_sample, humidity_sample)
        print(f"체감온도 지수: {discomfort_index_value}")
        pass_count += 1
    except Exception as e:
        print(f"Error in discomfort_index: {e}")
    
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"\n동작시간: {execution_time:.4f} seconds")
    print(f"총 4개의 API중 {pass_count}개의 API로 부터 응답을 받았습니다.")