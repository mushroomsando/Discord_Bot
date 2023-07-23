import math
from datetime import datetime

def get_visual_data(raw_data, return_type):
    """
    데이터를 시각화 하는 함수
    
    Args:
        raw_data (dic) : 초단기 실황 데이터를 포함한 딕셔너리.
        return_type (int) : 1 또는 2 중 택

    Retruns:
        str : 시각화 데이터
    """
    pty_code = raw_data
    wind = raw_data
    for item in raw_data['response']['body']['items']['item']:
        if item['category'] == 'PTY':
            pty_code = item['obsrValue']
        elif item['category'] == 'VEC':
            wind = item['obsrValue']
            wind = str(math.trunc((int(wind) + 22.5 * 0.5) / 22.5))
            break

    weather_emoji = {
        '0': '🔍',   # 없음
        '1': '🌧️',   # 비
        '2': '🌨️',   # 비/눈
        '3': '❄️',   # 눈
        '5': '🌦️',   # 빗방울
        '6': '🌧️❄️',  # 빗방울눈날림
        '7': '🌨️💨',   # 눈날림 (눈으로 대체)
    }

    wind_emoji = {
        '0' : '↑ 북',
        '1' : '↑↗ 북북동',
        '2' : '↗ 북동',
        '3' : '→↗  동북동',
        '4' : '→  동',
        '5' : '→↘  동남동',
        '6' : '↘ 남동',
        '7' : '↓↘ 남남동',
        '8' : '↓ 남',
        '9' : '↓↙ 남남서',
        '10' : '↙ 남서',
        '11' : '←↙  서남서',
        '12' : '←  서',
        '13' : '←↖ 서북서',
        '14' : '↖ 서북',
        '15' : '↑↖ 북북서',
        '16' : '↑ 북'
    }

    if return_type == 1:
        return weather_emoji.get(pty_code, '⚠️')
    elif return_type == 2:
        return wind_emoji.get(wind, "E")
    else:
        return None

def discomfort_index(Ta, RH, V):
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

    if 5 <= month <= 9:
        Tw = Ta * math.atan(0.151977 * math.sqrt(RH + 8.313659)) + math.atan(Ta + RH) - math.atan(RH - 1.67633) + 0.00391838 * math.pow(RH, 1.5) * math.atan(0.023101 * RH) - 4.686035
        discomfort_index = -0.2442 + 0.55399 * Tw + 0.45535 * Ta - 0.0022 * math.pow(Tw, 2) + 0.00278 * Tw * Ta + 3.0
        return discomfort_index # 여름철 체감온도
    else:
        if Ta <= 10 and V >= 1.3:
            discomfort_index = 13.12 + 0.6215 * Ta - 11.37 * math.pow(V, 0.16) + 0.3965 * math.pow(V, 0.16) * Ta
            return discomfort_index # 겨울철 체감온도
        else:
            return None # 겨울철 체감온도는 기온 10도 이하 풍속 1.3m/s 이상일 때만 산출