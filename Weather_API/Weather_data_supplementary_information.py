# TODO : API 구조 조정

# import math
# from datetime import datetime
# import Weather_data as Wd

# def get_visual_data(raw_data, data_type = 0):
#     """
#     데이터를 시각화 하는 함수
    
#     Args:
#         raw_data (dic) : 초단기 실황 데이터를 포함한 딕셔너리.
#         return_type (int) : 1 또는 2 중 택

#     Retruns:
#         str : 시각화 데이터
#     """
#     pty_code = raw_data
#     wind = raw_data
#     if data_type == 0:
#         for item in raw_data['response']['body']['items']['item']:
#             if item['category'] == 'PTY':
#                 pty_code = item['obsrValue']
#             elif item['category'] == 'VEC':
#                 wind = item['obsrValue']
#                 wind = str(math.trunc((int(wind) + 22.5 * 0.5) / 22.5))
#                 break
#     else:
#         wind = str(math.trunc((int(wind) + 22.5 * 0.5) / 22.5))

#     wind_emoji = {
#         '0' : '↑ 북',
#         '1' : '↗ 북동',
#         '2' : '↗ 북동',
#         '3' : '→ 동',
#         '4' : '→ 동',
#         '5' : '↘ 남동',
#         '6' : '↘ 남동',
#         '7' : '↓ 남',
#         '8' : '↓ 남',
#         '9' : '↙ 남서',
#         '10' : '↙ 남서',
#         '11' : '← 서',
#         '12' : '← 서',
#         '13' : '↖ 북서',
#         '14' : '↖ 북서',
#         '15' : '↑ 북',
#         '16' : '↑ 북'
#     }
    
# def get_sky_emoji(sky_code, pty_code):
#     if sky_code == '1':
#         return '☀️ 맑음'
#     elif sky_code == '3':
#         return '⛅ 구름많음'
#     elif sky_code == '4':
#         if pty_code == '1':
#             return '☔ 비'
#         elif pty_code == '2':
#             return '❄️/☔ 눈/비'
#         elif pty_code == '3':
#             return '❄️ 눈'
#         elif pty_code == '4':
#             return '🌦️ 소나기'
#         else:
#             return '☁️ 흐림'